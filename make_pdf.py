import re, sys
from pathlib import Path
import img2pdf
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
mode = sys.argv[1] if len(sys.argv) > 1 else "none"  # none | screen | print

def natural(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(p))]

files = sorted(
    (p for p in Path("images").rglob("*")
     if p.suffix.lower() in {".jpg", ".jpeg"}
     and not p.name.startswith("._") and "__MACOSX" not in p.parts),
    key=natural,
)
if not files:
    sys.exit("No JPGs found in images/")
print(f"Found {len(files)} images")

Path("out").mkdir(exist_ok=True)

if mode == "none":
    sources = [str(p) for p in files]
    out = Path("out/consolidated.pdf")
else:
    max_edge, quality = {"screen": (2000, 75), "print": (3000, 85)}[mode]
    tmp = Path("tmp")
    tmp.mkdir(exist_ok=True)
    sources = []
    for i, p in enumerate(files):
        with Image.open(p) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((max_edge, max_edge), Image.LANCZOS)
            dest = tmp / f"{i:04d}.jpg"
            im.save(dest, "JPEG", quality=quality, optimize=True)
        sources.append(str(dest))
    out = Path(f"out/consolidated_{mode}.pdf")

with open(out, "wb") as f:
    img2pdf.convert(sources, outputstream=f, rotation=img2pdf.Rotation.ifvalid)
print(f"{out}: {out.stat().st_size / 1e6:.0f} MB")
