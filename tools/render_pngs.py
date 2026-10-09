import os
import subprocess
import time
from PIL import Image

repo_dir = r"c:\Users\Ashok\source\repos\edloop-legal"
assets_dir = os.path.join(repo_dir, "assets")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# HTML templates for rendering via headless browser
def make_html(svg_content, bg="transparent", width=600, height=160):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ 
    width: {width}px; 
    height: {height}px; 
    background: {bg}; 
    display: flex; 
    align-items: center; 
    justify-content: center;
    overflow: hidden; 
  }}
  svg {{ width: 100%; height: 100%; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""

# Read SVGs
with open(os.path.join(assets_dir, "edloop-logo-light.svg"), "r", encoding="utf-8") as f:
    svg_light = f.read()

with open(os.path.join(assets_dir, "edloop-logo-dark.svg"), "r", encoding="utf-8") as f:
    svg_dark = f.read()

with open(os.path.join(assets_dir, "edloop-mark.svg"), "r", encoding="utf-8") as f:
    svg_mark = f.read()

renders = [
    ("edloop-logo-light.html", make_html(svg_light, "transparent", 1040, 280), "edloop-logo-light-raw.png", 1040, 280),
    ("edloop-logo-dark.html", make_html(svg_dark, "transparent", 1040, 280), "edloop-logo-dark-raw.png", 1040, 280),
    ("edloop-mark.html", make_html(svg_mark, "transparent", 512, 512), "edloop-mark-raw.png", 512, 512),
]

for html_name, html_content, out_png, w, h in renders:
    html_path = os.path.join(assets_dir, html_name)
    out_path = os.path.join(assets_dir, out_png)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        f"--window-size={w},{h}",
        f"--screenshot={out_path}",
        html_path
    ]
    subprocess.run(cmd, check=True)
    time.sleep(1)

# Now generate optimized sizes using Pillow
# 1. Main high-res light & dark
img_light = Image.open(os.path.join(assets_dir, "edloop-logo-light-raw.png"))
img_light.save(os.path.join(assets_dir, "edloop-logo.png"), "PNG")
img_light.save(os.path.join(assets_dir, "edloop-logo-light.png"), "PNG")

img_dark = Image.open(os.path.join(assets_dir, "edloop-logo-dark-raw.png"))
img_dark.save(os.path.join(assets_dir, "edloop-logo-dark.png"), "PNG")

# 2. Email Signature size (Retina: 480x130, standard display: 240x65)
sig_img = img_light.resize((480, 129), Image.Resampling.LANCZOS)
sig_img.save(os.path.join(assets_dir, "edloop-logo-signature.png"), "PNG", optimize=True)

sig_sm = img_light.resize((320, 86), Image.Resampling.LANCZOS)
sig_sm.save(os.path.join(assets_dir, "edloop-logo-signature-sm.png"), "PNG", optimize=True)

# 3. Mark & Favicon
img_mark = Image.open(os.path.join(assets_dir, "edloop-mark-raw.png"))
img_mark.save(os.path.join(assets_dir, "edloop-mark.png"), "PNG")

fav_32 = img_mark.resize((32, 32), Image.Resampling.LANCZOS)
fav_32.save(os.path.join(repo_dir, "favicon.png"), "PNG")
fav_32.save(os.path.join(assets_dir, "favicon.png"), "PNG")

# Save as .ico
img_mark.save(os.path.join(repo_dir, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
img_mark.save(os.path.join(assets_dir, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

# Clean up raw files
for f in ["edloop-logo-light-raw.png", "edloop-logo-dark-raw.png", "edloop-mark-raw.png", 
          "edloop-logo-light.html", "edloop-logo-dark.html", "edloop-mark.html"]:
    p = os.path.join(assets_dir, f)
    if os.path.exists(p):
        os.remove(p)

print("All PNG and ICO formats generated successfully!")
