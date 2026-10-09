import math

def generate_return_mark_svg(size=200):
    c = size / 2
    B = size * 0.88 # 176
    RING_R = 0.2675 * B
    RING_W = 0.085 * B
    GAP_AT = -60.0
    GAP = 60.0
    DOT_R = 0.07 * B
    CORE_R = 0.085 * B
    
    start_deg = GAP_AT + GAP / 2 # -30 deg
    end_deg = GAP_AT + 360 - GAP / 2 # 270 deg
    
    # Calculate arc start and end points in SVG coordinate system (y downwards)
    # math.sin and math.cos with clockwise angles from 3 o'clock:
    # x = c + R * cos(rad), y = c + R * sin(rad)
    start_rad = math.radians(start_deg)
    end_rad = math.radians(end_deg)
    
    x_start = c + RING_R * math.cos(start_rad)
    y_start = c + RING_R * math.sin(start_rad)
    x_end = c + RING_R * math.cos(end_rad)
    y_end = c + RING_R * math.sin(end_rad)
    
    # Focal dot at GAP_AT
    dot_rad = math.radians(GAP_AT)
    x_dot = c + RING_R * math.cos(dot_rad)
    y_dot = c + RING_R * math.sin(dot_rad)
    
    # Arc flags: sweep-flag=1 (clockwise), large-arc-flag=1 (since 300 deg > 180 deg)
    path_d = f"M {x_start:.2f},{y_start:.2f} A {RING_R:.2f},{RING_R:.2f} 0 1 1 {x_end:.2f},{y_end:.2f}"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="100%" height="100%">
  <defs>
    <linearGradient id="edloopBrandGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="50%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#6366f1" />
    </linearGradient>
  </defs>

  <!-- The Open Ring with Rounded Caps -->
  <path d="{path_d}" 
        fill="none" 
        stroke="url(#edloopBrandGrad)" 
        stroke-width="{RING_W:.2f}" 
        stroke-linecap="round" />

  <!-- The Return Node in Opening -->
  <circle cx="{x_dot:.2f}" cy="{y_dot:.2f}" r="{DOT_R:.2f}" fill="#38bdf8" />

  <!-- The Core -->
  <circle cx="{c:.2f}" cy="{c:.2f}" r="{CORE_R:.2f}" fill="url(#edloopBrandGrad)" />
</svg>'''
    return svg

print(generate_return_mark_svg(200))
