f = open('c:/Users/Windows/Documents/PROJETOS I.A/OSHER/index.html', encoding='utf-8')
c = f.read()
f.close()

print('=== OSHER index.html Check ===')
print(f'Linhas: {len(c.splitlines())}')
print(f'SVGs logo_h_: {c.count("osher_logo_h_")}')
print(f'logo_symbol.svg: {c.count("osher_logo_symbol")}')
print(f'logo_err_colors.svg: {c.count("osher_logo_err_colors")}')
print(f'Secoes: {c.count("<section id=")}')
print(f'Parallax-orb: {c.count("parallax-orb")}')
print(f'Reveal classes: {c.count('class="reveal')}')
print(f'data-lightbox-src: {c.count("data-lightbox-src")}')
print(f'app.js tag: {c.count("app.js")}')
import re, os

assets = re.findall(r'(?:src|href|data-lightbox-src)=["\']([^"\']+)["\']', c)
local_assets = [a for a in assets if not a.startswith(('http:', 'https:', '#', 'mailto:', 'tel:'))]
broken = [a for a in local_assets if not os.path.exists(a.split('?')[0].split('#')[0])]
print(f'Total de links locais verificados: {len(local_assets)}')
print(f'Links quebrados: {len(broken)}')
if broken:
    print('Arquivos ausentes:', broken)
print('=== OK ===')
