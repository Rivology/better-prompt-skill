#!/usr/bin/env python3
"""better-prompt improvement loop, v2.

The exact, boring parts: logging real uses, turning labelled bad uses into test cases, blinding rewrites, scoring
judge verdicts, the keep rule and the north-star number. The thinking (labelling, hypotheses, rewriting, judging)
is done by Claude following LOOP.md.

Private data (real prompts, cases, runs) lives in $BP_DATA (default ~/better-prompt-runs/rsi2), never in this repo:
the repo is public.
"""
import argparse, hashlib, json, os, random, re, shutil, statistics, sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = Path(os.environ.get("BP_DATA", Path.home() / "better-prompt-runs" / "rsi2")).expanduser()
USES, LABELS, CASES, HISTORY = (DATA / n for n in ("uses.jsonl", "labels.jsonl", "cases.jsonl", "history.jsonl"))
RUNS = DATA / "runs"
UNIVERSAL = ["U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8"]
BAD = {"intent", "scope", "broke", "bar"}
# Keep rule. Changing these is the user's decision, never a cycle's.
P_MAX = 0.05            # held-out paired test
CHECK_DROP_MAX = 0.10   # no universal check may lose more than 10 points of pass rate on held-out
GUARD_DROP_MAX = 0.05   # cases that went well in real use may not get worse by more than this
LENGTH_RATIO_MAX = 1.3  # median rewrite length vs baseline, a guard against judges rewarding length
AGREE_MIN = 0.70        # a check counts only if the two judges agree on it this often


def now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def jl(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()] if Path(path).exists() else []


def append(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def uid(text):
    return hashlib.sha1(text.encode()).hexdigest()[:10]


def version():
    return (REPO / "VERSION").read_text().strip() if (REPO / "VERSION").exists() else "?"


SECRET = re.compile(r"(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+)")


def redact(s):
    return SECRET.sub("[REDACTED]", s or "")


# ---------- real use ----------
def cmd_log(a):
    rough = Path(a.rough_file).read_text() if a.rough_file else a.rough
    rewrite = Path(a.rewrite_file).read_text() if a.rewrite_file else (a.rewrite or "")
    row = {"id": uid(rough + now()), "time": now(), "version": version(), "rough": redact(rough),
           "rewrite": redact(rewrite), "session": a.session, "model": a.model}
    append(USES, row)
    print("logged", row["id"])


def cmd_import(a):
    """Bring the old loop's feedback.jsonl in once. Old outcome words map to labels where they can."""
    seen = {u["id"] for u in jl(USES)}
    mapping = {"great": "accepted", "ok": "accepted", "missed": "intent", "fixes": "bar"}
    n = 0
    for r in jl(a.feedback):
        i = uid(r["rough"] + r.get("time", ""))
        if i in seen:
            continue
        append(USES, {"id": i, "time": r.get("time"), "version": str(r.get("version", "?")), "rough": r["rough"],
                      "rewrite": r.get("rewrite") or "", "session": r.get("session", ""), "model": r.get("model")})
        out = r.get("outcome")
        if out in mapping:
            append(LABELS, {"use": i, "label": mapping[out], "quote": (r.get("comment") or "")[:300],
                            "lesson": "", "check": "", "by": "import:" + str(r.get("comment_source") or "?"),
                            "provisional": True})
        n += 1
    print(f"imported {n} uses into {USES}")


def cmd_harvest(a):
    """Which uses still need a label, oldest first. The labeler (briefs/labeler.md) reads their transcripts."""
    labelled = {l["use"] for l in jl(LABELS)}
    todo = [u for u in jl(USES) if u["id"] not in labelled]
    for u in todo[: a.limit]:
        print(json.dumps({"use": u["id"], "time": u["time"], "session": u.get("session", ""),
                          "rough": u["rough"][:200]}, ensure_ascii=False))
    print(f"# {len(todo)} unlabelled", file=sys.stderr)


def cmd_label(a):
    """Apply labeler output (JSON lines). A bad label with a check becomes a case; a good one may become a guard."""
    uses = {u["id"]: u for u in jl(USES)}
    cases = {c["use"] for c in jl(CASES)}
    for row in jl(a.file):
        row.setdefault("by", "labeler")
        append(LABELS, row)
        u = uses.get(row["use"])
        if not u or row["use"] in cases:
            continue
        if row["label"] in BAD and row.get("check"):
            add_case(u, [row["check"]], "fail", row.get("situation", ""))
        elif row["label"] == "accepted" and a.guards:
            add_case(u, [], "guard", row.get("situation", ""))


def add_case(u, checks, kind, situation):
    split = "heldout" if int(hashlib.sha1(u["id"].encode()).hexdigest(), 16) % 2 else "train"
    append(CASES, {"id": "c" + u["id"][:6], "use": u["id"], "rough": u["rough"], "situation": situation,
                   "checks": checks, "kind": kind, "split": split, "added": now()})


def cmd_case_add(a):
    u = {"id": uid(a.rough), "rough": a.rough}
    add_case(u, a.check or [], a.kind, a.situation)
    print("added")


def cmd_northstar(a):
    """The number that matters: share of labelled real uses that went badly, per version."""
    labels = {}
    for l in jl(LABELS):
        labels[l["use"]] = l["label"]
    per = {}
    for u in jl(USES):
        lab = labels.get(u["id"])
        if lab in (None, "unknown", "abandoned"):
            continue
        v = per.setdefault(u["version"], [0, 0])
        v[0] += lab in BAD
        v[1] += 1
    for v, (bad, n) in sorted(per.items(), key=lambda x: x[0]):
        print(f"v{v}: {bad}/{n} went badly ({bad / n:.0%})")
    total = len(jl(USES))
    print(f"labelled {sum(n for _, n in per.values())} of {total} uses")


# ---------- a cycle ----------
def cmd_prepare(a):
    """Blind rewrite jobs for two skill folders on the chosen cases, k rewrites each."""
    cases = [c for c in jl(Path(a.cases) if a.cases else CASES) if a.split in ("all", c["split"])]
    if a.limit:
        cases = cases[: a.limit]
    run = RUNS / (a.name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    run.mkdir(parents=True)
    rng = random.Random(a.seed)
    sides = {"A": str(Path(a.baseline).resolve()), "B": str(Path(a.candidate).resolve())}
    (run / "sides.json").write_text(json.dumps(sides, indent=1))  # unblinding key; judges never open the run root
    jobs = {s: [] for s in sides}
    key = {}
    for c in cases:
        for s in sides:
            for k in range(a.k):
                rid = "r%04d" % rng.randrange(10000)
                while rid in key:
                    rid = "r%04d" % rng.randrange(10000)
                key[rid] = {"case": c["id"], "side": s, "k": k}
                jobs[s].append({"id": rid, "rough": c["rough"], "situation": c.get("situation", "")})
    (run / "key.json").write_text(json.dumps(key, indent=1))
    (run / "cases.json").write_text(json.dumps(cases, indent=1, ensure_ascii=False))
    brief = (REPO / "rsi/briefs/rewriter.md").read_text()
    for s, js in jobs.items():
        d = run / f"jobs_{s}"
        d.mkdir()
        (d / "jobs.json").write_text(json.dumps(js, indent=1, ensure_ascii=False))
        (d / "BRIEF.md").write_text(brief.format(skill_dir=sides[s], jobs_file=d / "jobs.json", out_dir=run / "rewrites"))
    (run / "rewrites").mkdir()
    print(run)
    print(f"{len(cases)} cases x 2 sides x k={a.k}: {len(key)} rewrites. Give each jobs_*/BRIEF.md to one rewriter.")


def cmd_blind(a):
    """After the rewrites exist: judge batches with shuffled items and no side labels, one set per judge."""
    run = Path(a.run)
    key = json.loads((run / "key.json").read_text())
    cases = {c["id"]: c for c in json.loads((run / "cases.json").read_text())}
    missing = [r for r in key if not (run / "rewrites" / f"{r}.md").exists()]
    if missing:
        sys.exit(f"missing rewrites: {missing[:10]} ({len(missing)})")
    ids = list(key)
    for j in range(a.judges):
        rng = random.Random(a.seed + j)
        rng.shuffle(ids)
        for b in range(0, len(ids), a.batch):
            parts = []
            for rid in ids[b: b + a.batch]:
                c = cases[key[rid]["case"]]
                checks = "\n".join(f"- C{i + 1}: {t}" for i, t in enumerate(c["checks"])) or "- (universal checks only)"
                parts.append(f"## {rid}\n\n**Request:**\n{c['rough']}\n\n**Situation:** {c.get('situation') or 'not recorded'}"
                             f"\n\n**Case checks:**\n{checks}\n\n**Rewrite:**\n\n{(run / 'rewrites' / f'{rid}.md').read_text()}\n")
            d = run / "judging" / f"j{j + 1}b{b // a.batch + 1}"  # one sealed folder per judge batch
            d.mkdir(parents=True, exist_ok=True)
            (d / "batch.md").write_text("\n---\n".join(parts))
            shutil.copy(REPO / "rsi/checks.md", d / "checks.md")
            shutil.copy(REPO / "rsi/briefs/judge.md", d / "judge.md")
    print(f"wrote {run / 'judging'}: give each folder to one judge (judge.md, checks.md, batch.md); "
          f"it writes verdict.json there and opens nothing else")


def perm_p(diffs, rng=random.Random(7), n=20000):
    """One-sided paired sign-flip test: P(mean >= observed) under no difference. Exact for n <= 16."""
    obs = statistics.mean(diffs)
    m = len(diffs)
    if m <= 16:
        hits = 0
        for mask in range(1 << m):
            s = sum(d if (mask >> i) & 1 else -d for i, d in enumerate(diffs))
            hits += s / m >= obs - 1e-12
        return hits / (1 << m)
    hits = sum(statistics.mean(d if rng.random() < .5 else -d for d in diffs) >= obs - 1e-12 for _ in range(n))
    return hits / n


def cmd_score(a):
    run = Path(a.run)
    key = json.loads((run / "key.json").read_text())
    cases = {c["id"]: c for c in json.loads((run / "cases.json").read_text())}
    if a.split != "all":  # decide on held-out only; train cases shaped the change
        key = {r: k for r, k in key.items() if cases[k["case"]]["split"] == a.split}
    verdicts = {}  # judge -> rid -> check -> pass/fail/na
    for f in sorted(run.glob("judging/j*b*/verdict.json")):
        j = re.match(r"j(\d+)b", f.parent.name).group(1)
        for rid, checks in json.loads(f.read_text()).items():
            verdicts.setdefault(j, {})[rid] = {k: (v[0] if isinstance(v, list) else v) for k, v in checks.items()}
    judges = sorted(verdicts)
    if not judges:
        sys.exit("no verdicts")
    # agreement per check between judge 1 and 2
    agree = {}
    if len(judges) >= 2:
        j1, j2 = verdicts[judges[0]], verdicts[judges[1]]
        for rid in set(j1) & set(j2):
            for ch in set(j1[rid]) & set(j2[rid]):
                g = "C" if ch.startswith("C") else ch
                agree.setdefault(g, []).append(j1[rid][ch] == j2[rid][ch])
    agree_rate = {g: sum(v) / len(v) for g, v in agree.items()}
    trusted = {g for g, r in agree_rate.items() if r >= AGREE_MIN} if agree_rate else set(UNIVERSAL) | {"C"}

    def passrate(rid, only=None):
        vals = []
        for j in judges:
            for ch, v in verdicts[j].get(rid, {}).items():
                g = "C" if ch.startswith("C") else ch
                if g not in trusted or v == "na" or (only and g != only):
                    continue
                vals.append(v == "pass")
        return sum(vals) / len(vals) if vals else None

    per_case = {}
    for rid, k in key.items():
        per_case.setdefault(k["case"], {"A": [], "B": []})[k["side"]].append(rid)
    diffs, guard_diffs, rows = [], [], []
    for cid, sides in per_case.items():
        pa = [p for p in (passrate(r) for r in sides["A"]) if p is not None]
        pb = [p for p in (passrate(r) for r in sides["B"]) if p is not None]
        if not pa or not pb:
            continue
        d = statistics.mean(pb) - statistics.mean(pa)
        rows.append((cid, cases[cid]["kind"], round(statistics.mean(pa), 2), round(statistics.mean(pb), 2)))
        (guard_diffs if cases[cid]["kind"] == "guard" else diffs).append(d)
    check_rates = {}
    for g in UNIVERSAL + ["C"]:
        if g not in trusted:
            continue
        r = {s: [p for p in (passrate(rid, g) for rid, k in key.items() if k["side"] == s) if p is not None] for s in "AB"}
        if r["A"] and r["B"]:
            check_rates[g] = (round(statistics.mean(r["A"]), 2), round(statistics.mean(r["B"]), 2))
    lens = {s: statistics.median(len((run / "rewrites" / f"{rid}.md").read_text()) for rid, k in key.items() if k["side"] == s) for s in "AB"}
    alld = diffs + guard_diffs
    mean_d = statistics.mean(alld) if alld else 0
    p = perm_p(alld) if alld else 1
    reasons = []
    if not (mean_d > 0 and p <= P_MAX):
        reasons.append(f"no clear gain (mean {mean_d:+.3f}, p={p:.3f})")
    for g, (ra, rb) in check_rates.items():
        if ra - rb > CHECK_DROP_MAX:
            reasons.append(f"{g} dropped {ra:.2f}->{rb:.2f}")
    if guard_diffs and statistics.mean(guard_diffs) < -GUARD_DROP_MAX:
        reasons.append(f"guard cases worse ({statistics.mean(guard_diffs):+.3f})")
    if lens["B"] > LENGTH_RATIO_MAX * lens["A"]:
        reasons.append(f"rewrites {lens['B'] / lens['A']:.2f}x longer")
    decision = "KEEP" if not reasons else "REJECT"
    out = {"run": run.name, "time": now(), "decision": decision, "reasons": reasons, "mean_diff": round(mean_d, 3),
           "p": round(p, 4), "n_cases": len(alld), "check_rates_A_B": check_rates, "agreement": agree_rate,
           "trusted_checks": sorted(trusted), "median_len_A_B": lens, "per_case": rows,
           "sides": json.loads((run / "sides.json").read_text())}
    (run / "result.json").write_text(json.dumps(out, indent=1))
    if not a.no_record:
        append(HISTORY, {k: out[k] for k in ("run", "time", "decision", "reasons", "mean_diff", "p", "n_cases")} | {"hypothesis": a.hypothesis})
    print(json.dumps(out, indent=1))


def cmd_lint(a):
    """Free checks before any agent is spent: every rewrite has a text block and a Done when, no shouting."""
    bad = 0
    for f in a.files:
        t = Path(f).read_text()
        probs = []
        if "```" not in t:
            probs.append("no fenced prompt")
        if not re.search(r"done when", t, re.I):
            probs.append("no Done when")
        if re.search(r"\b(IMPORTANT|CRITICAL|MUST|NEVER)\b", t):
            probs.append("shouting")
        if re.search(r"think step by step|don't be lazy", t, re.I):
            probs.append("outdated trick")
        if probs:
            bad += 1
            print(f, "; ".join(probs))
    print(f"{bad} of {len(a.files)} with problems")
    sys.exit(1 if bad else 0)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("log"); s.add_argument("--rough"); s.add_argument("--rough-file"); s.add_argument("--rewrite")
    s.add_argument("--rewrite-file"); s.add_argument("--session", default=""); s.add_argument("--model", default="")
    s = sub.add_parser("import"); s.add_argument("feedback")
    s = sub.add_parser("harvest"); s.add_argument("--limit", type=int, default=20)
    s = sub.add_parser("label"); s.add_argument("file"); s.add_argument("--guards", action="store_true")
    s = sub.add_parser("case-add"); s.add_argument("--rough", required=True); s.add_argument("--check", action="append")
    s.add_argument("--kind", choices=["fail", "guard"], default="fail"); s.add_argument("--situation", default="")
    sub.add_parser("northstar")
    s = sub.add_parser("prepare"); s.add_argument("--baseline", required=True); s.add_argument("--candidate", required=True)
    s.add_argument("--split", choices=["train", "heldout", "all"], default="heldout"); s.add_argument("--k", type=int, default=1)
    s.add_argument("--cases"); s.add_argument("--limit", type=int); s.add_argument("--name"); s.add_argument("--seed", type=int, default=1)
    s = sub.add_parser("blind"); s.add_argument("run"); s.add_argument("--judges", type=int, default=2)
    s.add_argument("--batch", type=int, default=12); s.add_argument("--seed", type=int, default=11)
    s = sub.add_parser("score"); s.add_argument("run"); s.add_argument("--hypothesis", default=""); s.add_argument("--no-record", action="store_true")
    s.add_argument("--split", choices=["train", "heldout", "all"], default="heldout")
    s = sub.add_parser("lint"); s.add_argument("files", nargs="+")
    a = p.parse_args()
    globals()["cmd_" + a.cmd.replace("-", "_")](a)


if __name__ == "__main__":
    main()
