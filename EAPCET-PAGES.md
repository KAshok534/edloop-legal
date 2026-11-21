# EAPCET Pages Build Report

Date: 2026-11-21  
Branch: `feature/eapcet-pages`  
Database: `content.prod-2026-11-19.sqlite`  

---

## 1. Hard Gates Summary

| Gate | Requirement | Status | Notes |
|------|-------------|--------|-------|
| **1. JEE output unchanged** | No changes under `q/`, `jee/`, `sitemap-q-*.xml` | **PASSED** | Zero changes to any JEE question, chapter, or sitemap files. |
| **2. Size** | Total HTML + image bytes <= 350 MB | **PASSED** | Total: **304,912,594 bytes (290.79 MB)**. Well under the 350 MB budget (by 45.09 MB / 59.21 MB). |
| **3. Counts from DB** | Question pages == verified non-sample EAPCET questions | **PASSED** | 23,840 questions in DB = 23,840 pages generated. 0 failed to render. |
| **4. No "JEE" / "NTA" / JEE Play link** | `grep -rl "NTA\|in.edloop.jee\|JEE Main" eapcet/q/ eapcet/pyq/` is empty | **PASSED** | 0 occurrences across all 23,932 files under `eapcet/q/` and `eapcet/pyq/`. |
| **5. Links resolve** | All internal links resolve in sample of 200 random pages | **PASSED** | 6,510 links tested across 200 random pages; 100% resolved to existing files. |
| **6. Local preview** | 5 pages served over local HTTP server | **PASSED** | Verified Math, Physics, Chemistry, figure question + WebP image, and correction note ("Dropped by APSCHE"). |

---

## 2. Detailed Counts & Byte Sizes

### Page & Question Counts
- **Verified non-sample EAPCET questions in database**: 23,840
- **Generated question pages**: 23,840
  - Mathematics: 9,280 pages
  - Physics: 7,280 pages
  - Chemistry: 7,280 pages
- **Questions with figure image**: 1,555
- **Questions failed to render**: **0**
- **Duplicate titles disambiguated**: 157
- **Hub pages generated**: 92
  - Index hub: 1 (`/eapcet/pyq/`)
  - Subject hubs: 3 (`/eapcet/pyq/mathematics`, `/eapcet/pyq/physics`, `/eapcet/pyq/chemistry`)
  - Chapter hubs: 88 (29 maths, 28 physics, 31 chemistry)

### Byte Sizes
- **HTML bytes**: 255,662,096 bytes (243.82 MB across 23,932 HTML pages; ~10.68 KB/page)
- **Image bytes**: 49,250,498 bytes (46.97 MB across 1,555 WebP figures; ~31.67 KB/image)
- **Total EAPCET bytes**: **304,912,594 bytes (290.79 MB)**
- **Gate 2 Threshold**: 350,000,000 bytes (333.78 MB / 350 MB)
- **Budget Margin**: 45,087,406 bytes (~45 MB) under the 350 MB limit.

### Image Optimization
Each figure image from the database was re-encoded using Pillow (`PIL.Image`):
- Scaled down to at most 900 px wide (aspect ratio preserved using Lanczos resampling).
- Saved as WebP at quality 75.
- `<img>` tags in HTML set with exact updated `width` and `height` dimensions.
- Total image size reduced from 120.59 MB to 49.25 MB (a 59.2% reduction).

---

## 3. Sample Verification (Gate 6)

Tested via local HTTP server serving `C:\wt-eapcet`:
1. **Maths**: `/eapcet/q/q-apeapcet-2010-05-30-offline-m01.html` (HTTP 200, 10,252 bytes)
2. **Physics**: `/eapcet/q/q-apeapcet-2010-05-30-offline-p01.html` (HTTP 200, 10,431 bytes)
3. **Chemistry**: `/eapcet/q/q-apeapcet-2010-05-30-offline-c01.html` (HTTP 200, 10,325 bytes)
4. **Figure**: `/eapcet/q/q-apeapcet-2010-05-30-offline-c30.html` (HTTP 200, 11,260 bytes)
   - Figure image: `/eapcet/q/img/q-apeapcet-2010-05-30-offline-c30.webp` (HTTP 200, 22,506 bytes)
5. **Correction Note**: `/eapcet/q/q-apeapcet-2012-05-12-offline-p05.html` (HTTP 200, 10,807 bytes)
   - Renders: `Dropped by APSCHE. Full marks to everyone.` with prov `Official APSCHE final key`.

---

## 4. Legibility Check on 10 Figure Pages

Inspected 10 figure pages with intricate diagrams, circuits, logic gates, chemical structures, and graphs:
1. `q-tseapcet-2023-05-14-m-p24` (Physics — Capacitors): Multi-branch capacitor network with labels A, B, C values, bridge wires, Telugu/English text. **Sharp and readable.**
2. `q-apeapcet-2026-05-18-e-c18` (Chemistry — General Organic Chemistry): Four skeletal carbocation structures (a)–(d) with $\oplus$ charges and oxygen atoms. **Sharp and readable.**
3. `q-apeapcet-2026-05-15-m-p39` (Physics — Semiconductor Electronics): Multi-gate logic circuit with NAND, NOT gates, inversion bubbles, wire hops, inputs 1/0, output Y. **Sharp and readable.**
4. `q-tseapcet-2023-05-14-e-p36` (Physics — Dual Nature of Matter & Radiation): Photocurrent $I$ vs applied voltage $V$ graph curves 1–4, axes, stopping potential points. **Sharp and readable.**
5. `q-tseapcet-2023-05-14-m-p32` (Physics — Alternating Current): Complex AC circuit with 10 components ($8\,\Omega$, $20\,\text{mH}$, $6\,\mu\text{F}$, $0.5\,\mu\text{F}$, $0.8\,\mu\text{F}$, $220\,\text{V}$ AC source, current arrow $i$). Small unit labels ($\mu\text{F}, \text{mH}, \Omega$) are **sharp and legible**.
6. `q-apeapcet-2023-05-15-e-p27` (Physics — Current Electricity): Resistor network with battery $E, 2\,\Omega$, seven resistors ($5\,\Omega, 10\,\Omega, 3\,\Omega, 8\,\Omega, 6\,\Omega$). **Sharp and readable.**
7. `q-apeapcet-2026-05-18-e-c14` (Chemistry — p-Block Elements): Dimeric $\text{Al}_2\text{Cl}_6$ bridge structure, terminal and bridging chlorines, angle arcs $X, Y, Z$. **Sharp and readable.**
8. `q-apeapcet-2024-05-22-m-p21` (Physics — Waves): Standing wave vibration profiles in 4 air columns (a)–(d), length markings $L$, nodes and antinodes. **Sharp and readable.**
9. `q-apeapcet-2021-10-05-m-m70` (Mathematics — Applications of Derivatives): Composite window diagram (rectangle + semicircle) with formula options. **Sharp and readable.**
10. `q-apeapcet-2010-05-30-offline-c30` (Chemistry — Hydrocarbons): Diels-Alder reaction dienes and dienophiles (1)–(4) from scanned historical paper. **Sharp and readable.**

Conclusion: Quality 75 at max 900 px width preserves high fidelity and legibility for all diagrams and text. No individual figure quality increases were required.

---

## 5. Deliverable Status

All six hard gates passed.
Total EAPCET footprint: 304.91 MB (within 350 MB limit).
Pages committed on branch `feature/eapcet-pages` and pushed to remote repository.
