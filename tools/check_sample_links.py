import os, random, re
from urllib.parse import urlparse

root = r'C:\wt-eapcet'
all_pages = []
for dirpath, dirs, files in os.walk(os.path.join(root, 'eapcet')):
    for f in files:
        if f.endswith('.html'):
            all_pages.append(os.path.join(dirpath, f))

print('Total EAPCET html pages:', len(all_pages))
random.seed(42)
sample = random.sample(all_pages, min(200, len(all_pages)))

broken = []
total_links = 0
for page_path in sample:
    with open(page_path, encoding='utf-8') as fh:
        content = fh.read()
    
    # find all href and src
    links = re.findall(r'\b(?:href|src)="([^"]*)"', content)
    for l in links:
        # Ignore external, hash only, mailto, tel
        if l.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'intent:')):
            continue
        total_links += 1
        path = urlparse(l).path
        if not path:
            continue
        
        # Resolve to file
        if path.startswith('/'):
            rel = path.lstrip('/')
        else:
            rel = os.path.relpath(os.path.join(os.path.dirname(page_path), path), root)
        
        # Check target
        target = os.path.join(root, rel)
        if os.path.isfile(target):
            pass
        elif os.path.isfile(target + '.html'):
            target = target + '.html'
        elif os.path.isdir(target) and os.path.isfile(os.path.join(target, 'index.html')):
            target = os.path.join(target, 'index.html')
        elif not os.path.exists(target):
            broken.append((page_path, l, target))

print(f"Checked {len(sample)} pages, {total_links} internal links.")
print(f"Broken links: {len(broken)}")
if broken:
    for p, l, t in broken[:10]:
        print(f"  In {os.path.basename(p)}: {l} -> {t}")
