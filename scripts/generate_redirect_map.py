import json, re, sys
from datetime import datetime
import xml.etree.ElementTree as ET

sitemap_file = "data/blogger/sitemap.xml"
output_file = "data/blogger/migration_seo_map.json"

print(f"Парсинг: {sitemap_file}")

try:
    tree = ET.parse(sitemap_file)
    root = tree.getroot()
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    urls = []
    for url_elem in root.findall('ns:url', ns):
        loc = url_elem.find('ns:loc', ns)
        if loc is not None and loc.text:
            urls.append(loc.text.strip())
            
    print(f"Найдено URL в sitemap: {len(urls)}")
    
    redirects = {}
    skipped = []
    
    for url in urls:
        match = re.search(r'/\d{4}/\d{2}/(.+?)\.html$', url)
        if match:
            slug = match.group(1)
            old_path_match = re.search(r'(\/\d{4}\/\d{2}\/.+?\.html)$', url)
            if old_path_match:
                redirects[old_path_match.group(1)] = f"/{slug}/"
            else:
                skipped.append(url)
        else:
            skipped.append(url)
            
    output = {
        "site": sys.argv[1] if len(sys.argv) > 1 else "unknown",
        "generated_at": datetime.now().isoformat(),
        "source": sitemap_file,
        "total_urls": len(urls),
        "redirects_count": len(redirects),
        "skipped_count": len(skipped),
        "redirects": redirects
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
    print(f"Карта редиректов создана: {output_file}")
    print(f"Всего редиректов: {len(redirects)}")
    print(f"Пропущено: {len(skipped)}")
    
except Exception as e:
    print(f"Ошибка при парсинге: {e}")
    sys.exit(1)
