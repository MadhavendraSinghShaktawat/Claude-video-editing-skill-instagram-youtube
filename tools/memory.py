#!/usr/bin/env python3
"""The skill's long-term memory: brand answers, learned styles, feedback notes.

    python tools/memory.py status                 what is saved, what is still unanswered
    python tools/memory.py questions [--all]      the intake questions still to ask (JSON)
    python tools/memory.py set <id> <value>       save one answer, e.g. set brand.colors '{"accent":"#2f6bff"}'
    python tools/memory.py get <id>
    python tools/memory.py note "<feedback>"      append dated feedback (what the user liked or rejected)
    python tools/memory.py styles                 list learned styles
    python tools/memory.py use <style>            set the default style

Files live in memory/ beside this repo (or $EXPLAINER_EDITOR_HOME):
  brand.json            answers to memory/intake.json
  notes.md              dated feedback, newest last
  styles/<name>/        made by tools/learn_style.py from reference or old videos
brand.json, notes.md and styles/ of your own are git-ignored: they are yours, not the repo's.
"""
import json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
MEM = os.environ.get("EXPLAINER_EDITOR_HOME") or os.path.join(os.path.dirname(HERE), "memory")
BRAND = os.path.join(MEM, "brand.json")
INTAKE = json.load(open(os.path.join(os.path.dirname(HERE), "memory", "intake.json")))["questions"]


def load():
    return json.load(open(BRAND)) if os.path.exists(BRAND) else {}


def save(b):
    os.makedirs(MEM, exist_ok=True)
    b["_updated"] = datetime.date.today().isoformat()
    json.dump(b, open(BRAND, "w"), indent=1, ensure_ascii=False)


def get(b, path):
    for k in path.split("."):
        if not isinstance(b, dict) or k not in b: return None
        b = b[k]
    return b


def put(b, path, val):
    ks = path.split(".")
    for k in ks[:-1]: b = b.setdefault(k, {})
    if isinstance(val, dict) and isinstance(b.get(ks[-1]), dict): b[ks[-1]].update(val)
    else: b[ks[-1]] = val


def styles():
    d = os.path.join(MEM, "styles")
    return sorted(x for x in os.listdir(d) if os.path.exists(os.path.join(d, x, "style.json"))) if os.path.isdir(d) else []


cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
b = load()
if cmd in ("status", "questions"):
    every = "--all" in sys.argv
    todo = [q for q in INTAKE if every or get(b, q["id"]) in (None, "", {}) and not (q.get("optional") and get(b, "_skipped." + q["id"].replace(".", "_")))
            or q.get("per_video")]
    if cmd == "questions":
        print(json.dumps(todo, indent=1, ensure_ascii=False))
    else:
        print(f"memory: {MEM}")
        print(f"answered: {sum(get(b, q['id']) not in (None, '', {}) for q in INTAKE)}/{len(INTAKE)}   still to ask: {len(todo)}")
        print(f"styles: {', '.join(styles()) or 'none'}   default: {b.get('default_style')}")
        for q in INTAKE:
            v = get(b, q["id"])
            print(f"  [{'x' if v not in (None, '', {}) else ' '}] {q['id']:28s} {json.dumps(v, ensure_ascii=False) if v is not None else ''}")
elif cmd == "set":
    raw = sys.argv[3]
    try: val = json.loads(raw)
    except ValueError: val = raw
    put(b, sys.argv[2], val); save(b); print("saved", sys.argv[2])
elif cmd == "skip":
    put(b, "_skipped." + sys.argv[2].replace(".", "_"), True); save(b)
elif cmd == "get":
    print(json.dumps(get(b, sys.argv[2]), indent=1, ensure_ascii=False))
elif cmd == "note":
    os.makedirs(MEM, exist_ok=True)
    with open(os.path.join(MEM, "notes.md"), "a") as f:
        f.write(f"- {datetime.date.today().isoformat()}: {sys.argv[2]}\n")
    print("noted")
elif cmd == "styles":
    for s in styles():
        j = json.load(open(os.path.join(MEM, "styles", s, "style.json")))
        print(f"{s:28s} {len(j.get('sources', []))} videos  {j.get('description', '')}")
elif cmd == "use":
    if sys.argv[2] not in styles(): sys.exit("no such style; run: python tools/memory.py styles")
    b["default_style"] = sys.argv[2]; save(b); print("default style:", sys.argv[2])
else:
    sys.exit(__doc__)
