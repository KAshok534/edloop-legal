import math
import os
import subprocess
import time
from PIL import Image

repo_dir = r"c:\Users\Ashok\source\repos\edloop-legal"
assets_dir = os.path.join(repo_dir, "assets")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
os.makedirs(assets_dir, exist_ok=True)

# Generate mathematical Return Mark SVG
def get_mark_svg_inner(grad_id="loopGrad", glow_color="#38bdf8", stroke_grad="url(#loopGrad)"):
    # Geometry from make_brand.py
    # S = 200, B = 176 (box = 0.88 * 200)
    c = 100.0
    B = 176.0
    RING_R = 0.2675 * B # 47.08
    RING_W = 0.085 * B  # 14.96
    GAP_AT = -60.0
    GAP = 60.0
    DOT_R = 0.07 * B    # 12.32
    CORE_R = 0.085 * B  # 14.96
    
    start_deg = GAP_AT + GAP / 2 # -30 deg
    end_deg = GAP_AT + 360 - GAP / 2 # 270 deg
    
    start_rad = math.radians(start_deg)
    end_rad = math.radians(end_deg)
    
    x_start = c + RING_R * math.cos(start_rad)
    y_start = c + RING_R * math.sin(start_rad)
    x_end = c + RING_R * math.cos(end_rad)
    y_end = c + RING_R * math.sin(end_rad)
    
    dot_rad = math.radians(GAP_AT)
    x_dot = c + RING_R * math.cos(dot_rad)
    y_dot = c + RING_R * math.sin(dot_rad)
    
    path_d = f"M {x_start:.2f},{y_start:.2f} A {RING_R:.2f},{RING_R:.2f} 0 1 1 {x_end:.2f},{y_end:.2f}"
    
    return f'''
  <!-- The Open Ring with Rounded Caps -->
  <path d="{path_d}" 
        fill="none" 
        stroke="{stroke_grad}" 
        stroke-width="{RING_W:.2f}" 
        stroke-linecap="round" />

  <!-- The Return Node in Opening -->
  <circle cx="{x_dot:.2f}" cy="{y_dot:.2f}" r="{DOT_R:.2f}" fill="{glow_color}" />

  <!-- The Core -->
  <circle cx="{c:.2f}" cy="{c:.2f}" r="{CORE_R:.2f}" fill="{stroke_grad}" />
'''

# 1. Standalone Mark (SVG)
mark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="markGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="45%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#6366f1" />
    </linearGradient>
  </defs>
  {get_mark_svg_inner("markGrad", "#38bdf8", "url(#markGrad)")}
</svg>'''

with open(os.path.join(assets_dir, "edloop-mark.svg"), "w", encoding="utf-8") as f:
    f.write(mark_svg)


# 2. Email Signature Logo (Light background, transparent, sharp)
# Box 560x140 with mark on left, Ed in dark slate, Loop in gradient
logo_light_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 140" width="540" height="140">
  <defs>
    <linearGradient id="sigLoopGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="45%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#4f46e5" />
    </linearGradient>
    <linearGradient id="sigTextGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#6366f1" />
    </linearGradient>
  </defs>

  <g transform="translate(10, 0)">
    <!-- Symbol scaled to 110x110 -->
    <g transform="translate(10, 15) scale(0.55)">
      {get_mark_svg_inner("sigLoopGrad", "#0284c7", "url(#sigLoopGrad)")}
    </g>

    <!-- Wordmark with differentiated Ed and Loop -->
    <text x="145" y="76" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="54" letter-spacing="-2">
      <tspan fill="#0f172a">Ed</tspan><tspan fill="url(#sigTextGrad)">Loop</tspan>
    </text>

    <!-- Tagline -->
    <text x="147" y="104" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="13" fill="#64748b" letter-spacing="1.5">
      EDUCATION INTELLIGENCE &bull; EDLOOP.IN
    </text>
  </g>
</svg>'''

with open(os.path.join(assets_dir, "edloop-logo-light.svg"), "w", encoding="utf-8") as f:
    f.write(logo_light_svg)


# 3. Dark Theme Logo (for dark background)
logo_dark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 140" width="540" height="140">
  <defs>
    <linearGradient id="darkLoopGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="45%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#818cf8" />
    </linearGradient>
    <linearGradient id="darkTextGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#c084fc" />
    </linearGradient>
  </defs>

  <g transform="translate(10, 0)">
    <!-- Symbol scaled to 110x110 -->
    <g transform="translate(10, 15) scale(0.55)">
      {get_mark_svg_inner("darkLoopGrad", "#38bdf8", "url(#darkLoopGrad)")}
    </g>

    <!-- Wordmark with differentiated Ed and Loop -->
    <text x="145" y="76" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="54" letter-spacing="-2">
      <tspan fill="#f8fafc">Ed</tspan><tspan fill="url(#darkTextGrad)">Loop</tspan>
    </text>

    <!-- Tagline -->
    <text x="147" y="104" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="13" fill="#94a3b8" letter-spacing="1.5">
      EDUCATION INTELLIGENCE &bull; EDLOOP.IN
    </text>
  </g>
</svg>'''

with open(os.path.join(assets_dir, "edloop-logo-dark.svg"), "w", encoding="utf-8") as f:
    f.write(logo_dark_svg)

print("Updated SVGs written!")
