import os
import subprocess
import time

repo_dir = r"c:\Users\Ashok\source\repos\edloop-legal"
assets_dir = os.path.join(repo_dir, "assets")
os.makedirs(assets_dir, exist_ok=True)

# 1. Standalone Mark (SVG) - The Cyclical Return Loop
mark_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="loopGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="35%" stop-color="#06b6d4" />
      <stop offset="70%" stop-color="#6366f1" />
      <stop offset="100%" stop-color="#8b5cf6" />
    </linearGradient>
    <linearGradient id="glowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#818cf8" />
    </linearGradient>
    <filter id="subtleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Ambient Glow Behind -->
  <circle cx="100" cy="100" r="65" fill="none" stroke="url(#loopGrad)" stroke-width="18" opacity="0.25" filter="url(#subtleGlow)" />

  <!-- Outer Open Orbit Loop -->
  <path d="M 100,28 A 72,72 0 1,1 32,122" 
        fill="none" 
        stroke="url(#loopGrad)" 
        stroke-width="16" 
        stroke-linecap="round" />

  <!-- Inner Return Arc -->
  <path d="M 52,130 A 52,52 0 0,0 148,110 A 52,52 0 0,0 100,48" 
        fill="none" 
        stroke="url(#glowGrad)" 
        stroke-width="11" 
        stroke-linecap="round" 
        opacity="0.9" />

  <!-- The Return Focal Node -->
  <circle cx="100" cy="28" r="10" fill="#ffffff" stroke="#0284c7" stroke-width="4" />
  <circle cx="100" cy="28" r="4" fill="#0284c7" />
</svg>'''

with open(os.path.join(assets_dir, "edloop-mark.svg"), "w", encoding="utf-8") as f:
    f.write(mark_svg)


# 2. Horizontal Logo - Light / Email Signature Version (Dark text, vibrant logo, transparent background)
logo_light_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 140" width="520" height="140">
  <defs>
    <linearGradient id="sigLoop" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="40%" stop-color="#06b6d4" />
      <stop offset="80%" stop-color="#4f46e5" />
      <stop offset="100%" stop-color="#7c3aed" />
    </linearGradient>
    <linearGradient id="brandText" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#6366f1" />
    </linearGradient>
    <filter id="sigGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <g transform="translate(10, 10)">
    <!-- Symbol -->
    <g transform="translate(10, 5)">
      <!-- Outer Orbit -->
      <path d="M 55,16 A 42,42 0 1,1 16,72" 
            fill="none" 
            stroke="url(#sigLoop)" 
            stroke-width="10" 
            stroke-linecap="round" />

      <!-- Inner Arc -->
      <path d="M 28,76 A 30,30 0 0,0 84,65 A 30,30 0 0,0 55,27" 
            fill="none" 
            stroke="url(#sigLoop)" 
            stroke-width="7" 
            stroke-linecap="round" 
            opacity="0.85" />

      <!-- Return Node -->
      <circle cx="55" cy="16" r="6" fill="#0284c7" />
      <circle cx="55" cy="16" r="2.5" fill="#ffffff" />
    </g>

    <!-- Wordmark -->
    <text x="135" y="72" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="52" fill="#0f172a" letter-spacing="-1.5">
      Ed<tspan fill="url(#brandText)">Loop</tspan>
    </text>

    <!-- Tagline -->
    <text x="137" y="100" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="13.5" fill="#64748b" letter-spacing="1.5">
      EDUCATION INTELLIGENCE &bull; EDLOOP.IN
    </text>
  </g>
</svg>'''

with open(os.path.join(assets_dir, "edloop-logo-light.svg"), "w", encoding="utf-8") as f:
    f.write(logo_light_svg)


# 3. Horizontal Logo - Dark Theme Version (White text, luminous glow)
logo_dark_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 140" width="520" height="140">
  <defs>
    <linearGradient id="darkLoop" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="40%" stop-color="#06b6d4" />
      <stop offset="80%" stop-color="#818cf8" />
      <stop offset="100%" stop-color="#c084fc" />
    </linearGradient>
    <linearGradient id="darkTextGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#a855f7" />
    </linearGradient>
  </defs>

  <g transform="translate(10, 10)">
    <!-- Symbol -->
    <g transform="translate(10, 5)">
      <path d="M 55,16 A 42,42 0 1,1 16,72" 
            fill="none" 
            stroke="url(#darkLoop)" 
            stroke-width="10" 
            stroke-linecap="round" />

      <path d="M 28,76 A 30,30 0 0,0 84,65 A 30,30 0 0,0 55,27" 
            fill="none" 
            stroke="url(#darkLoop)" 
            stroke-width="7" 
            stroke-linecap="round" 
            opacity="0.85" />

      <circle cx="55" cy="16" r="6" fill="#ffffff" />
      <circle cx="55" cy="16" r="3" fill="#38bdf8" />
    </g>

    <!-- Wordmark -->
    <text x="135" y="72" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="52" fill="#f8fafc" letter-spacing="-1.5">
      Ed<tspan fill="url(#darkTextGrad)">Loop</tspan>
    </text>

    <!-- Tagline -->
    <text x="137" y="100" font-family="'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="13.5" fill="#94a3b8" letter-spacing="1.5">
      EDUCATION INTELLIGENCE &bull; EDLOOP.IN
    </text>
  </g>
</svg>'''

with open(os.path.join(assets_dir, "edloop-logo-dark.svg"), "w", encoding="utf-8") as f:
    f.write(logo_dark_svg)

print("Generated SVGs successfully in", assets_dir)
