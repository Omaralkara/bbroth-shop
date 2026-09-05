"""Inline every asset into one HTML file, for sharing a preview link.
The deployable site stays as index.html + assets/."""
import base64, pathlib, re

root = pathlib.Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
for asset in sorted((root / "assets").iterdir()):
    uri = "data:%s;base64,%s" % (
        MIME[asset.suffix.lower()],
        base64.b64encode(asset.read_bytes()).decode(),
    )
    html = html.replace("assets/" + asset.name, uri)

# The artifact host supplies <!doctype>, <html>, <head> and <body>.
html = re.sub(r"(?is)^.*?<head>", "", html)
html = re.sub(r"(?is)</head>\s*<body>", "", html)
html = re.sub(r"(?is)</body>\s*</html>\s*$", "", html)
# Drop tags the host already provides or that do nothing in an artifact.
html = re.sub(r'(?i)\s*<meta charset[^>]*>', "", html)
html = re.sub(r'(?i)\s*<meta name="viewport"[^>]*>', "", html)
html = re.sub(r'(?i)\s*<link rel="icon"[^>]*>', "", html)

# The gallery wants a name, not the SEO title the live site uses.
html = html.replace("<title>B.Broth — Pure Lebanese Bone Broth</title>", "<title>B.Broth Shop</title>")

out = root / "preview_single_file.html"
out.write_text(html.strip(), encoding="utf-8")
print(f"{out.name}: {out.stat().st_size/1024/1024:.2f} MB")
