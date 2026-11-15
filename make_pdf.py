import re, subprocess, sys
from pathlib import Path
import img2pdf

mode = sys.argv[1] if len(sys.argv) > 1 else "none"  # none | screen | print

def natural(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(p))]

files = sorted(
    (p for p in Path("images").rglob("*") if p.suffix.lower() in {".jpg", ".jpeg"}),
    key=natural,
)
if not files:
    sys.exit("No JPGs found in images/")
print(f"Found {len(files)} images")

Path("out").mkdir(exist_ok=True)
full = Path("out/consolidated.pdf")
with open(full, "wb") as f:
    img2pdf.convert([str(p) for p in files], outputstream=f)  # lossless embed, no recompression
print(f"Full-quality PDF: {full.stat().st_size / 1e6:.0f} MB")

if mode in ("screen", "print"):
    setting = "/ebook" if mode == "screen" else "/printer"
    small = Path(f"out/consolidated_{mode}.pdf")
    subprocess.run(
        ["gs", "-sDEVICE=pdfwrite", f"-dPDFSETTINGS={setting}", "-dNOPAUSE",
         "-dBATCH", "-dQUIET", f"-sOutputFile={small}", str(full)],
        check=True,
    )
    print(f"Compressed PDF: {small} ({small.stat().st_size / 1e6:.0f} MB)")
