"""Inline every asset into standalone HTML files, for sharing preview links.
The deployable site stays as index.html / coming-soon.html + assets/."""
import base64, pathlib, re

root = pathlib.Path(__file__).parent
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}

DATA_URIS = {
    a.name: "data:%s;base64,%s" % (MIME[a.suffix.lower()],
                                   base64.b64encode(a.read_bytes()).decode())
    for a in sorted((root / "assets").iterdir())
}

# source file -> (output file, gallery title)
PAGES = {
    "index.html":       ("preview_single_file.html", "B.Broth Shop"),
    "coming-soon.html": ("preview_coming_soon.html", "B.Broth Launching Soon"),
}

for src, (dst, title) in PAGES.items():
    html = (root / src).read_text(encoding="utf-8")
    for name, uri in DATA_URIS.items():
        html = html.replace("assets/" + name, uri)

    # The artifact host supplies <!doctype>, <html>, <head> and <body>.
    html = re.sub(r"(?is)^.*?<head>", "", html)
    html = re.sub(r"(?is)</head>\s*<body>", "", html)
    html = re.sub(r"(?is)</body>\s*</html>\s*$", "", html)
    html = re.sub(r'(?i)\s*<meta charset[^>]*>', "", html)
    html = re.sub(r'(?i)\s*<meta name="viewport"[^>]*>', "", html)
    html = re.sub(r'(?i)\s*<link rel="icon"[^>]*>', "", html)
    # The gallery wants a name, not the SEO title the live site uses.
    html = re.sub(r"(?is)<title>.*?</title>", "<title>%s</title>" % title, html, count=1)

    out = root / dst
    out.write_text(html.strip(), encoding="utf-8")
    print(f"{out.name}: {out.stat().st_size/1024/1024:.2f} MB  ({title})")
