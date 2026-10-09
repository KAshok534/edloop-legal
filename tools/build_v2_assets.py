import os
import subprocess
import time
from PIL import Image

repo_dir = r"c:\Users\Ashok\source\repos\edloop-legal"
assets_dir = os.path.join(repo_dir, "assets")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
os.makedirs(assets_dir, exist_ok=True)

# Variation 2 Geometry
def get_v2_mark_svg_inner(grad_id="v2Grad", node_stroke="#ffffff", node_fill="#38bdf8"):
    return f'''
  <!-- Outer Arc: R=70, from 100,30 around to 45,130 -->
  <path d="M 100,30 A 70,70 0 1,1 45,130" fill="none" stroke="url(#{grad_id})" stroke-width="14" stroke-linecap="round" />

  <!-- Inner Arc: R=48, adjusted with clean 16px parallel clearance channel -->
  <path d="M 68,136 A 48,48 0 0,0 148,100 A 48,48 0 0,0 100,52" fill="none" stroke="url(#{grad_id})" stroke-width="11" stroke-linecap="round" opacity="0.9" />

  <!-- Focal Arrival Node at Apex -->
  <circle cx="100" cy="30" r="9" fill="{node_stroke}" stroke="{node_fill}" stroke-width="3" />
  <circle cx="100" cy="30" r="4.5" fill="{node_fill}" />
'''

# 1. Standalone Mark SVG
mark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="markV2Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="50%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#818cf8" />
    </linearGradient>
  </defs>
  {get_v2_mark_svg_inner("markV2Grad", "#ffffff", "#38bdf8")}
</svg>'''

with open(os.path.join(assets_dir, "edloop-mark.svg"), "w", encoding="utf-8") as f:
    f.write(mark_svg)


# 2. Email Signature Logo SVG (Light theme, transparent)
logo_light_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 140" width="540" height="140">
  <defs>
    <linearGradient id="sigV2Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="50%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#4f46e5" />
    </linearGradient>
    <linearGradient id="sigV2TextGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#6366f1" />
    </linearGradient>
  </defs>

  <g transform="translate(10, 0)">
    <!-- Symbol scaled to 110x110 -->
    <g transform="translate(10, 15) scale(0.55)">
      {get_v2_mark_svg_inner("sigV2Grad", "#ffffff", "#0284c7")}
    </g>

    <!-- Wordmark: Ed (solid dark) + Loop (vibrant gradient) -->
    <text x="145" y="76" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="54" letter-spacing="-2">
      <tspan fill="#0f172a">Ed</tspan><tspan fill="url(#sigV2TextGrad)">Loop</tspan>
    </text>

    <!-- Tagline -->
    <text x="147" y="104" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="13" fill="#64748b" letter-spacing="1.5">
      EDUCATION INTELLIGENCE &bull; EDLOOP.IN
    </text>
  </g>
</svg>'''

with open(os.path.join(assets_dir, "edloop-logo-light.svg"), "w", encoding="utf-8") as f:
    f.write(logo_light_svg)


# 3. Dark Theme Logo SVG
logo_dark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 140" width="540" height="140">
  <defs>
    <linearGradient id="darkV2Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="50%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#818cf8" />
    </linearGradient>
    <linearGradient id="darkV2TextGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#c084fc" />
    </linearGradient>
  </defs>

  <g transform="translate(10, 0)">
    <g transform="translate(10, 15) scale(0.55)">
      {get_v2_mark_svg_inner("darkV2Grad", "#ffffff", "#38bdf8")}
    </g>

    <text x="145" y="76" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="54" letter-spacing="-2">
      <tspan fill="#f8fafc">Ed</tspan><tspan fill="url(#darkV2TextGrad)">Loop</tspan>
    </text>

    <text x="147" y="104" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="13" fill="#94a3b8" letter-spacing="1.5">
      EDUCATION INTELLIGENCE &bull; EDLOOP.IN
    </text>
  </g>
</svg>'''

with open(os.path.join(assets_dir, "edloop-logo-dark.svg"), "w", encoding="utf-8") as f:
    f.write(logo_dark_svg)

print("Generated SVGs for Variation 2!")
