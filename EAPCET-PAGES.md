# EAPCET Pages Build Report

Date: 2026-11-21  
Branch: `feature/eapcet-pages`  
Database: `content.prod-2026-11-19.sqlite`  

---

## 1. Hard Gates Summary

| Gate | Requirement | Status | Notes |
|------|-------------|--------|-------|
| **1. JEE output unchanged** | No changes under `q/`, `jee/`, `sitemap-q-*.xml` | **PASSED** | Zero changes to any JEE question, chapter, or sitemap files. |
| **2. Size** | Total HTML + image bytes <= 350 MB | **FAILED** | Total: **376,132,871 bytes (358.71 MB)**. Exceeds 350 MB threshold by ~8.71 MB. Pages commit held pending review. |
| **3. Counts from DB** | Question pages == verified non-sample EAPCET questions | **PASSED** | 23,840 questions in DB = 23,840 pages generated. 0 failed to render. |
| **4. No "JEE" / "NTA" / JEE Play link** | `grep -rl "NTA\|in.edloop.jee\|JEE Main" eapcet/` is empty | **PASSED** | 0 occurrences across all 23,933 files in `eapcet/`. |
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
- **HTML bytes**: 255,543,847 bytes (243.70 MB across 23,932 HTML pages; ~10.68 KB/page)
- **Image bytes**: 120,589,024 bytes (115.00 MB across 1,555 WebP figures; ~77.55 KB/image)
- **Total EAPCET bytes**: **376,132,871 bytes (358.71 MB)**
- **Gate 2 Threshold**: 350,000,000 bytes (333.78 MB / 350 MB)
- **Difference**: +26,132,871 bytes over 350 MB threshold (or +8.71 MB above 350 MiB).

---

## 3. Sample Verification (Gate 6)

Tested via local HTTP server serving `C:\wt-eapcet`:
1. **Maths**: `/eapcet/q/q-apeapcet-2010-05-30-offline-m01.html` (HTTP 200, 10,247 bytes)
2. **Physics**: `/eapcet/q/q-apeapcet-2010-05-30-offline-p01.html` (HTTP 200, 10,426 bytes)
3. **Chemistry**: `/eapcet/q/q-apeapcet-2010-05-30-offline-c01.html` (HTTP 200, 10,320 bytes)
4. **Figure**: `/eapcet/q/q-apeapcet-2010-05-30-offline-c30.html` (HTTP 200, 11,256 bytes)
   - Figure image: `/eapcet/q/img/q-apeapcet-2010-05-30-offline-c30.webp` (HTTP 200, 202,166 bytes)
5. **Correction Note**: `/eapcet/q/q-apeapcet-2012-05-12-offline-p05.html` (HTTP 200, 10,802 bytes)
   - Renders: `Dropped by APSCHE. Full marks to everyone.` with prov `Official APSCHE final key`.

---

## 4. Deliverable Status

Per the brief instructions:
> *"If it is over 350 MB, stop before committing pages and report (GitHub Pages limit is 1 GB for the whole site; JEE uses about 220 MB). Commit code first, pages in a separate commit."*
> *"Stop and report if the size gate fails."*

The code commit and `EAPCET-PAGES.md` are committed and pushed to `feature/eapcet-pages`.
The pages commit (`eapcet/q/`, `eapcet/pyq/`, sitemaps) is held pending approval/guidance on the size gate.
