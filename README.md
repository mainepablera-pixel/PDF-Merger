# JPG → single PDF

1. Put your JPGs in `images/` (extract the zip first; files are ordered by name, naturally: 2 before 10).
2. Commit/push. The **Build PDF** action runs automatically.
3. Open the **Actions** tab → latest run → download the `consolidated-pdf` artifact.

For a smaller PDF: Actions → Build PDF → Run workflow → pick `screen` (~150 dpi) or `print` (~300 dpi).

Notes: GitHub rejects single files over 100 MB, so upload the images, not the zip. The web uploader allows 100 files at a time, so do two batches.
