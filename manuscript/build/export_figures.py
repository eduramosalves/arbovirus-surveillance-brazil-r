"""Copy the final figures under their manuscript numbers into manuscript/figures/.

The manuscript numbers figures by order of first citation, the repository keeps its own file names
(figures/main, figures/supplementary, figures/glm). The mapping comes from build_report.json, which build.py writes.
Usage: python export_figures.py <build output folder>      (the folder given to build.py)
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
report = json.load(open(Path(sys.argv[1]) / "build_report.json", encoding="utf-8"))
dest = ROOT / "manuscript" / "figures"
dest.mkdir(exist_ok=True)
for old in dest.glob("*.png"):
    old.unlink()
n = 0
for fig in report["figures"]:
    num, files = fig["number"], fig["files"]
    for name in files:
        src = next((ROOT / "figures").rglob(name))
        # one file: Figure<N>.png; several (supplementary maps by year): Figure<N>_<suffix>.png
        target = "Figure%s.png" % num if len(files) == 1 else "Figure%s_%s.png" % (num, Path(name).stem.split("_", 1)[1])
        shutil.copyfile(src, dest / target)
        n += 1
print("copied %d figures to %s" % (n, dest))
