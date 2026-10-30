"""
OSHER Açaí Shop — Gerador de Mockups Premium (Pillow / PIL)
Gera 3 imagens fotorrealistas de alta qualidade para a apresentação da marca:
1. Papelaria Corporativa de Luxo
2. Papelaria de Ponto de Venda & Mesa
3. Totem Arquitetônico & Fachada (100% sem pessoas)
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

# Carregar logo limpa
clean_logo_path = os.path.join(ASSETS_DIR, 'osher_logo_clean.png')
if not os.path.exists(clean_logo_path):
    cover = Image.open(os.path.join(ASSETS_DIR, 'osher_logo_cover.png'))
    bbox = cover.getbbox()
    clean_logo = cover.crop(bbox)
    clean_logo.save(clean_logo_path)
else:
    clean_logo = Image.open(clean_logo_path)

# ==============================================================================
# UTILITÁRIOS DE FONTE
# ==============================================================================
def get_font(name, size):
    font_map = {
        'serif': 'C:/Windows/Fonts/georgiab.ttf',
        'serif_regular': 'C:/Windows/Fonts/georgia.ttf',
        'serif_italic': 'C:/Windows/Fonts/georgiai.ttf',
        'sans': 'C:/Windows/Fonts/segoeuib.ttf',
        'sans_regular': 'C:/Windows/Fonts/segoeui.ttf',
        'sans_light': 'C:/Windows/Fonts/segoeuil.ttf',
        'sans_semibold': 'C:/Windows/Fonts/seguisb.ttf',
    }
    path = font_map.get(name, 'C:/Windows/Fonts/arial.ttf')
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# ==============================================================================
# UTILITÁRIOS DE RENDERIZAÇÃO
# ==============================================================================
def draw_rect_shadow(img, rect, blur=22, offset=(0, 16), opacity=160, corner_radius=10):
    """Desenha sombra suave com desfoque gaussian multi-layer"""
    x1, y1, x2, y2 = rect
    pad = blur * 3
    sw = int(x2 - x1 + pad * 2)
    sh = int(y2 - y1 + pad * 2)
    shadow = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sx1 = pad + offset[0]
    sy1 = pad + offset[1]
    sx2 = sx1 + (x2 - x1)
    sy2 = sy1 + (y2 - y1)
    sdraw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=corner_radius, fill=(0, 0, 0, opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    # Segunda camada de sombra mais suave e dispersa
    shadow2 = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    s2draw = ImageDraw.Draw(shadow2)
    s2draw.rounded_rectangle([sx1 + 4, sy1 + 6, sx2 + 4, sy2 + 6], radius=corner_radius + 4, fill=(0, 0, 0, opacity // 3))
    shadow2 = shadow2.filter(ImageFilter.GaussianBlur(blur * 2))
    shadow.alpha_composite(shadow2)
    pos = (int(x1 - pad), int(y1 - pad))
    img.alpha_composite(shadow, pos)


def create_metallic_gold_rect(w, h, angle=35):
    """Cria retângulo com gradiente metálico dourado premium"""
    grad = Image.new('RGBA', (w, h))
    pixels = grad.load()
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    max_d = abs(w * cos_a) + abs(h * sin_a)
    if max_d == 0:
        max_d = 1

    c1 = (155, 95, 5)       # sombra profunda
    c2 = (195, 120, 8)      # base escura
    c3 = (221, 137, 1)      # ouro principal
    c4 = (255, 225, 140)    # brilho especular intenso
    c5 = (240, 175, 40)     # ouro vivo

    for y in range(h):
        for x in range(w):
            d = ((x * cos_a + y * sin_a) / max_d * 3.0) % 1.0
            if d < 0.2:
                t = d / 0.2
                r = int(c1[0] + t * (c2[0] - c1[0]))
                g = int(c1[1] + t * (c2[1] - c1[1]))
                b = int(c1[2] + t * (c2[2] - c1[2]))
            elif d < 0.45:
                t = (d - 0.2) / 0.25
                r = int(c2[0] + t * (c3[0] - c2[0]))
                g = int(c2[1] + t * (c3[1] - c2[1]))
                b = int(c2[2] + t * (c3[2] - c2[2]))
            elif d < 0.6:
                t = (d - 0.45) / 0.15
                r = int(c3[0] + t * (c4[0] - c3[0]))
                g = int(c3[1] + t * (c4[1] - c3[1]))
                b = int(c3[2] + t * (c4[2] - c3[2]))
            elif d < 0.8:
                t = (d - 0.6) / 0.2
                r = int(c4[0] + t * (c5[0] - c4[0]))
                g = int(c4[1] + t * (c5[1] - c4[1]))
                b = int(c4[2] + t * (c5[2] - c4[2]))
            else:
                t = (d - 0.8) / 0.2
                r = int(c5[0] + t * (c1[0] - c5[0]))
                g = int(c5[1] + t * (c1[1] - c5[1]))
                b = int(c5[2] + t * (c1[2] - c5[2]))
            pixels[x, y] = (r, g, b, 255)
    return grad


def apply_gold_mask(logo_img, target_w, target_h):
    """Aplica máscara metálica dourada sobre a logo"""
    resized = logo_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    if resized.mode != 'RGBA':
        resized = resized.convert('RGBA')
    gold = create_metallic_gold_rect(target_w, target_h)
    r, g, b, a = resized.split()
    gold.putalpha(a)
    return gold


def create_noise_texture(w, h, intensity=12, seed=42):
    """Cria textura de ruído sutil para simular granulação de papel/couro"""
    rng = random.Random(seed)
    noise = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pixels = noise.load()
    for y in range(h):
        for x in range(w):
            val = rng.randint(-intensity, intensity)
            pixels[x, y] = (128 + val, 128 + val, 128 + val, 18)
    return noise


def create_radial_gradient(w, h, cx, cy, radius, color, max_alpha=40):
    """Cria gradiente radial para simular iluminação de estúdio"""
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pixels = glow.load()
    for y in range(h):
        for x in range(w):
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            t = max(0.0, 1.0 - dist / radius)
            alpha = int(t * t * max_alpha)
            if alpha > 0:
                pixels[x, y] = (color[0], color[1], color[2], alpha)
    return glow


def create_dark_marble_bg(w, h, seed=123):
    """Cria fundo de mármore escuro com veios procedurais"""
    base = Image.new('RGBA', (w, h), (18, 18, 20, 255))
    draw = ImageDraw.Draw(base)

    # Gradiente vertical suave
    for y in range(h):
        t = y / h
        val = int(20 - t * 6)
        draw.line([(0, y), (w, y)], fill=(val, val, val + 1, 255))

    # Veios de mármore procedurais
    rng = random.Random(seed)
    veins = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(veins)
    for _ in range(8):
        points = []
        x = rng.randint(-100, w // 3)
        y = rng.randint(0, h)
        for _ in range(rng.randint(4, 8)):
            x += rng.randint(100, 400)
            y += rng.randint(-200, 200)
            points.append((x, y))
        if len(points) >= 2:
            color_choice = rng.choice([
                (221, 137, 1, rng.randint(15, 30)),
                (200, 190, 170, rng.randint(12, 22)),
                (255, 230, 180, rng.randint(8, 18)),
            ])
            vdraw.line(points, fill=color_choice, width=rng.randint(1, 3))
    veins = veins.filter(ImageFilter.GaussianBlur(3))
    base.alpha_composite(veins)

    return base


def create_kraft_texture(w, h, base_color=(175, 140, 100)):
    """Cria textura kraft/papel pardo realista"""
    img = Image.new('RGBA', (w, h), base_color + (255,))
    pixels = img.load()
    rng = random.Random(77)
    for y in range(h):
        for x in range(w):
            noise = rng.randint(-8, 8)
            fiber = int(math.sin(x * 0.15 + y * 0.03) * 4)
            r = max(0, min(255, base_color[0] + noise + fiber))
            g = max(0, min(255, base_color[1] + noise + fiber))
            b = max(0, min(255, base_color[2] + noise + fiber))
            pixels[x, y] = (r, g, b, 255)
    return img


# ==============================================================================
# 1. PAPELARIA CORPORATIVA LUXO
# ==============================================================================
def render_stationery_luxury():
    print("  ⏳ Gerando papelaria corporativa de luxo...")
    W, H = 1800, 1100
    base = create_dark_marble_bg(W, H, seed=101)
    draw = ImageDraw.Draw(base)

    # Iluminação volumétrica — spotlight superior esquerdo
    spotlight1 = create_radial_gradient(W, H, 400, 200, 900, (255, 215, 140), 35)
    base.alpha_composite(spotlight1)
    # Rim light sutil à direita
    spotlight2 = create_radial_gradient(W, H, W - 200, 400, 700, (240, 220, 200), 18)
    base.alpha_composite(spotlight2)

    # Reflexo suave no plano (simula mesa polida)
    for y in range(H - 80, H):
        t = (y - (H - 80)) / 80
        alpha = int(t * 25)
        draw.line([(0, y), (W, y)], fill=(30, 28, 26, 255))

    # ─── ITEM 1: Pasta Corporativa (Left) ───
    f_rect = [80, 120, 720, 920]
    draw_rect_shadow(base, f_rect, blur=32, offset=(12, 26), opacity=190, corner_radius=14)

    folder = Image.new('RGBA', (f_rect[2] - f_rect[0], f_rect[3] - f_rect[1]), (26, 26, 28, 255))
    fdraw = ImageDraw.Draw(folder)
    fdraw.rounded_rectangle([0, 0, folder.width, folder.height], radius=14, fill=(24, 24, 28, 255), outline=(42, 42, 48, 255), width=2)

    # Textura sutil de couro/soft-touch
    noise_f = create_noise_texture(folder.width, folder.height, intensity=6, seed=200)
    folder.alpha_composite(noise_f)

    # Filigrana decorativa dourada
    fdraw = ImageDraw.Draw(folder)
    fdraw.line([(50, 510), (folder.width - 50, 510)], fill=(221, 137, 1, 200), width=2)
    fdraw.line([(folder.width // 2 - 80, 516), (folder.width // 2 + 80, 516)], fill=(255, 220, 140, 200), width=1)

    # Logo dourada grande
    gold_logo_f = apply_gold_mask(clean_logo, 380, 268)
    folder.alpha_composite(gold_logo_f, ((folder.width - 380) // 2, 140))

    # Tipografia
    fdraw.text((folder.width // 2, 560), "MANUAL DE IDENTIDADE VISUAL", fill=(248, 240, 225), font=get_font('serif', 24), anchor="mm")
    fdraw.text((folder.width // 2, 600), "DIRETRIZES DE MARCA • BRANDKIT EXECUTIVO 2026", fill=(200, 150, 50), font=get_font('sans', 14), anchor="mm")
    fdraw.text((folder.width // 2, 720), "OSHER AÇAÍ SHOP • BRASÍLIA / GUARÁ I", fill=(130, 130, 140), font=get_font('sans_light', 12), anchor="mm")

    base.alpha_composite(folder, (f_rect[0], f_rect[1]))

    # ─── ITEM 2: Papel Timbrado A4 (Center) ───
    l_rect = [660, 90, 1250, 880]
    draw_rect_shadow(base, l_rect, blur=28, offset=(14, 22), opacity=175, corner_radius=8)

    letter = Image.new('RGBA', (l_rect[2] - l_rect[0], l_rect[3] - l_rect[1]), (252, 250, 245, 255))
    ldraw = ImageDraw.Draw(letter)
    ldraw.rounded_rectangle([0, 0, letter.width, letter.height], radius=8, fill=(252, 250, 245, 255), outline=(218, 213, 205, 255), width=1)

    # Textura de papel sutil
    paper_noise = create_noise_texture(letter.width, letter.height, intensity=4, seed=300)
    letter.alpha_composite(paper_noise)
    ldraw = ImageDraw.Draw(letter)

    # Header com logo e dados
    gold_logo_sm = apply_gold_mask(clean_logo, 170, 120)
    letter.alpha_composite(gold_logo_sm, (50, 35))

    ldraw.text((240, 62), "OSHER AÇAÍ SHOP", fill=(28, 28, 30), font=get_font('serif', 22))
    ldraw.text((240, 92), "Açaí + Sorvete. Do seu jeito.", fill=(185, 120, 12), font=get_font('serif_italic', 14))
    ldraw.line([(50, 170), (letter.width - 50, 170)], fill=(221, 137, 1, 200), width=2)

    # Simulação de texto de corpo
    for idx, y_pos in enumerate(range(215, 640, 26)):
        line_w = letter.width - 100
        if idx in (3, 7, 11, 15):
            line_w -= random.Random(idx).randint(60, 180)
        ldraw.line([(50, y_pos), (50 + line_w, y_pos)], fill=(220, 216, 208, 255), width=2)

    # Rodapé
    ldraw.line([(50, 700), (letter.width - 50, 700)], fill=(225, 220, 210, 255), width=1)
    ldraw.text((50, 718), "Guará I • Brasília - DF | contato@osheracai.com.br | www.osheracai.com.br", fill=(135, 130, 120), font=get_font('sans_light', 11))

    base.alpha_composite(letter, (l_rect[0], l_rect[1]))

    # ─── ITEM 3: Envelope com Lacre de Cera (Top-Right) ───
    e_rect = [1180, 120, 1700, 470]
    draw_rect_shadow(base, e_rect, blur=26, offset=(10, 18), opacity=185, corner_radius=10)

    env = Image.new('RGBA', (e_rect[2] - e_rect[0], e_rect[3] - e_rect[1]), (22, 22, 24, 255))
    edraw = ImageDraw.Draw(env)
    edraw.rounded_rectangle([0, 0, env.width, env.height], radius=10, fill=(24, 24, 26, 255), outline=(48, 48, 55, 255), width=2)

    # Aba triangular
    edraw.polygon([(0, 0), (env.width // 2, 200), (env.width, 0)], fill=(30, 30, 34, 255), outline=(55, 55, 62, 255))

    # Lacre de cera dourado 3D — múltiplas camadas para profundidade
    sc = (env.width // 2, 200)
    edraw.ellipse([sc[0] - 44, sc[1] - 44, sc[0] + 44, sc[1] + 44], fill=(160, 95, 5, 255))
    edraw.ellipse([sc[0] - 40, sc[1] - 40, sc[0] + 40, sc[1] + 40], fill=(195, 120, 8, 255))
    edraw.ellipse([sc[0] - 36, sc[1] - 36, sc[0] + 36, sc[1] + 36], fill=(221, 137, 1, 255))
    edraw.ellipse([sc[0] - 32, sc[1] - 32, sc[0] + 32, sc[1] + 32], fill=(255, 220, 130, 255))
    edraw.ellipse([sc[0] - 28, sc[1] - 28, sc[0] + 28, sc[1] + 28], fill=(221, 142, 10, 255))
    edraw.text(sc, "O", fill=(255, 250, 230), font=get_font('serif', 30), anchor="mm")

    # Logo pequena no corpo do envelope
    gold_env_logo = apply_gold_mask(clean_logo, 100, 70)
    env.alpha_composite(gold_env_logo, ((env.width - 100) // 2, 255))

    base.alpha_composite(env, (e_rect[0], e_rect[1]))

    # ─── ITEM 4: Cartão de Visita Frente (Bottom-Right) ───
    c1_rect = [1200, 530, 1660, 770]
    draw_rect_shadow(base, c1_rect, blur=22, offset=(8, 16), opacity=180, corner_radius=8)
    card1 = Image.new('RGBA', (c1_rect[2] - c1_rect[0], c1_rect[3] - c1_rect[1]), (22, 22, 24, 255))
    c1draw = ImageDraw.Draw(card1)
    c1draw.rounded_rectangle([0, 0, card1.width, card1.height], radius=8, fill=(22, 22, 26, 255), outline=(221, 137, 1, 140), width=2)
    # Borda dourada superior (gilding)
    c1draw.line([(0, 2), (card1.width, 2)], fill=(255, 220, 130, 240), width=3)

    gold_c1 = apply_gold_mask(clean_logo, 220, 155)
    card1.alpha_composite(gold_c1, ((card1.width - 220) // 2, 20))
    c1draw.text((card1.width // 2, 195), "Açaí + Sorvete. Do seu jeito.", fill=(221, 137, 1), font=get_font('serif_italic', 13), anchor="mm")
    base.alpha_composite(card1, (c1_rect[0], c1_rect[1]))

    # ─── ITEM 5: Cartão de Visita Verso (Bottom-Right-Lower) ───
    c2_rect = [1120, 770, 1580, 1010]
    draw_rect_shadow(base, c2_rect, blur=24, offset=(10, 18), opacity=185, corner_radius=8)
    card2 = Image.new('RGBA', (c2_rect[2] - c2_rect[0], c2_rect[3] - c2_rect[1]), (26, 26, 28, 255))
    c2draw = ImageDraw.Draw(card2)
    c2draw.rounded_rectangle([0, 0, card2.width, card2.height], radius=8, fill=(26, 26, 30, 255), outline=(52, 52, 60, 255), width=2)

    c2draw.text((35, 30), "RAFAEL LIMA", fill=(252, 248, 240), font=get_font('sans', 16))
    c2draw.text((35, 54), "Diretor de Marca & Expansão", fill=(221, 137, 1), font=get_font('sans_regular', 12))
    c2draw.line([(35, 82), (card2.width - 35, 82)], fill=(55, 55, 62, 255), width=1)
    c2draw.text((35, 100), "Tel: +55 (61) 98123-4567", fill=(195, 195, 200), font=get_font('sans_light', 11))
    c2draw.text((35, 124), "Email: rafael@osheracai.com.br", fill=(195, 195, 200), font=get_font('sans_light', 11))
    c2draw.text((35, 148), "Local: Guará I - Brasília - DF", fill=(195, 195, 200), font=get_font('sans_light', 11))
    c2draw.text((35, 172), "Site: www.osheracai.com.br", fill=(221, 137, 1), font=get_font('sans_regular', 11))

    base.alpha_composite(card2, (c2_rect[0], c2_rect[1]))

    # ─── ITEM 6: Caneta Executiva Dourada ───
    pen_rect = [1000, 200, 1028, 800]
    draw_rect_shadow(base, pen_rect, blur=18, offset=(16, 14), opacity=160, corner_radius=14)
    pen = create_metallic_gold_rect(pen_rect[2] - pen_rect[0], pen_rect[3] - pen_rect[1], angle=90)
    pdraw = ImageDraw.Draw(pen)
    pdraw.rounded_rectangle([0, 0, pen.width, pen.height], radius=14, fill=None, outline=(140, 85, 5, 255), width=1)
    # Clip e anéis
    pdraw.rectangle([6, 25, 22, 200], fill=(255, 235, 170, 255))
    pdraw.line([(0, 400), (pen.width, 400)], fill=(85, 48, 0, 255), width=3)
    pdraw.line([(0, 406), (pen.width, 406)], fill=(255, 235, 170, 255), width=2)
    # Ponta
    pdraw.polygon([(pen.width // 2 - 4, pen.height), (pen.width // 2 + 4, pen.height), (pen.width // 2, pen.height + 8)], fill=(90, 90, 95, 255))
    base.alpha_composite(pen, (pen_rect[0], pen_rect[1]))

    # ─── Badge ───
    tag = Image.new('RGBA', (400, 52), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tag)
    tdraw.rounded_rectangle([0, 0, 400, 52], radius=26, fill=(12, 12, 14, 240), outline=(221, 137, 1, 200), width=2)
    tdraw.text((200, 26), "PAPELARIA CORPORATIVA • 2026", fill=(221, 137, 1), font=get_font('sans', 13), anchor="mm")
    base.alpha_composite(tag, (60, 50))

    # ─── Ruído final fotográfico ───
    final_noise = create_noise_texture(W, H, intensity=3, seed=999)
    base.alpha_composite(final_noise)

    final = base.convert('RGB')
    # Ajuste de contraste e saturação para look fotográfico
    enhancer = ImageEnhance.Contrast(final)
    final = enhancer.enhance(1.08)
    enhancer = ImageEnhance.Sharpness(final)
    final = enhancer.enhance(1.15)

    final.save(os.path.join(ASSETS_DIR, 'osher_papelaria_corporativa.jpg'), quality=97)
    print("  ✅ osher_papelaria_corporativa.jpg — GERADA!")


# ==============================================================================
# 2. PAPELARIA DE PONTO DE VENDA & BALCÃO
# ==============================================================================
def render_stationery_pdv():
    print("  ⏳ Gerando papelaria de ponto de venda...")
    W, H = 1800, 1100
    base = create_dark_marble_bg(W, H, seed=202)
    draw = ImageDraw.Draw(base)

    # Iluminação de balcão quente
    spotlight = create_radial_gradient(W, H, W // 2, H // 3, 850, (255, 210, 140), 32)
    base.alpha_composite(spotlight)
    spotlight2 = create_radial_gradient(W, H, 300, 600, 500, (255, 220, 160), 20)
    base.alpha_composite(spotlight2)

    # ─── ITEM 1: Display de Mesa em Latão (Center) ───
    dt_rect = [490, 100, 1180, 920]
    draw_rect_shadow(base, dt_rect, blur=36, offset=(12, 28), opacity=200, corner_radius=18)

    # Base de latão
    stand_rect = [440, 910, 1230, 980]
    draw_rect_shadow(base, stand_rect, blur=18, offset=(0, 20), opacity=210, corner_radius=12)
    stand = create_metallic_gold_rect(stand_rect[2] - stand_rect[0], stand_rect[3] - stand_rect[1], angle=0)
    sdraw = ImageDraw.Draw(stand)
    sdraw.rounded_rectangle([0, 0, stand.width, stand.height], radius=12, fill=None, outline=(150, 90, 5, 200), width=2)
    base.alpha_composite(stand, (stand_rect[0], stand_rect[1]))

    # Painel do menu
    menu = Image.new('RGBA', (dt_rect[2] - dt_rect[0], dt_rect[3] - dt_rect[1]), (22, 22, 24, 255))
    mdraw = ImageDraw.Draw(menu)
    mdraw.rounded_rectangle([0, 0, menu.width, menu.height], radius=18, fill=(20, 20, 22, 255), outline=(221, 137, 1, 200), width=3)

    # Textura sutil
    menu_noise = create_noise_texture(menu.width, menu.height, intensity=5, seed=400)
    menu.alpha_composite(menu_noise)
    mdraw = ImageDraw.Draw(menu)

    # Logo grande no topo
    gold_logo_m = apply_gold_mask(clean_logo, 290, 204)
    menu.alpha_composite(gold_logo_m, ((menu.width - 290) // 2, 35))

    mdraw.text((menu.width // 2, 255), "CARDÁPIO DE BALCÃO & MESA", fill=(255, 225, 145), font=get_font('sans', 14), anchor="mm")
    mdraw.text((menu.width // 2, 288), "Açaí + Sorvete. Do seu jeito.", fill=(248, 242, 230), font=get_font('serif', 22), anchor="mm")
    mdraw.line([(65, 320), (menu.width - 65, 320)], fill=(221, 137, 1, 220), width=2)

    # Lista de produtos
    items = [
        ("Copo Clássico 300ml", "1 Sorvete + 2 Caldas + 2 Toppings", "R$ 13,00"),
        ("Copo Especial 400ml", "Açaí cremoso + 2 Sorvetes + 3 Toppings", "R$ 15,00"),
        ("Copo OSHER 500ml", "Monte do seu jeito • Mais pedido", "R$ 17,00"),
        ("Bowl Cerâmico 600ml", "Experiência de salão + Frutas frescas", "R$ 22,00"),
        ("Mega Pote Família 1000ml", "1 Litro artesanal para levar ou mesa", "R$ 36,00")
    ]

    y_start = 350
    for i, (title, desc, price) in enumerate(items):
        is_highlight = (i == 2)
        title_color = (255, 225, 140) if is_highlight else (250, 245, 235)
        title_font = get_font('serif', 19) if is_highlight else get_font('serif', 17)
        price_font = get_font('sans', 20) if is_highlight else get_font('sans', 18)

        mdraw.text((65, y_start), title, fill=title_color, font=title_font)
        mdraw.text((65, y_start + 26), desc, fill=(155, 150, 140), font=get_font('sans_light', 12))
        mdraw.text((menu.width - 65, y_start + 12), price, fill=(221, 137, 1), font=price_font, anchor="ra")
        mdraw.line([(65, y_start + 58), (menu.width - 65, y_start + 58)], fill=(42, 42, 48, 255), width=1)
        y_start += 78

    mdraw.text((menu.width // 2, 755), "Caldas Especiais: Mel Puro • Brigadeiro Nobre • Pistache Artesanal", fill=(205, 165, 90), font=get_font('sans_regular', 12), anchor="mm")
    mdraw.text((menu.width // 2, 780), "Peça pelo WhatsApp ou App Oficial OSHER", fill=(140, 140, 148), font=get_font('sans_light', 11), anchor="mm")

    base.alpha_composite(menu, (dt_rect[0], dt_rect[1]))

    # ─── ITEM 2: Cartão Fidelidade OSHER Club (Left) ───
    fid_rect = [60, 260, 440, 500]
    draw_rect_shadow(base, fid_rect, blur=24, offset=(8, 16), opacity=180, corner_radius=12)
    fid = Image.new('RGBA', (fid_rect[2] - fid_rect[0], fid_rect[3] - fid_rect[1]), (250, 248, 242, 255))
    fiddraw = ImageDraw.Draw(fid)
    fiddraw.rounded_rectangle([0, 0, fid.width, fid.height], radius=12, fill=(250, 248, 242, 255), outline=(221, 137, 1, 170), width=2)

    fiddraw.text((25, 22), "OSHER CLUB", fill=(24, 24, 28), font=get_font('serif', 19))
    fiddraw.text((25, 48), "Cartão Fidelidade 10 Selos", fill=(185, 120, 12), font=get_font('sans', 12))

    for row in range(2):
        for col in range(5):
            cx = 42 + col * 62
            cy = 100 + row * 52
            stamped = (row == 0 and col < 4)
            if stamped:
                fiddraw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(221, 137, 1, 240))
                fiddraw.text((cx, cy), "★", fill=(255, 255, 255), font=get_font('sans', 15), anchor="mm")
            else:
                fiddraw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=None, outline=(175, 170, 160), width=2)
                fiddraw.text((cx, cy), str(row * 5 + col + 1), fill=(155, 150, 140), font=get_font('sans', 12), anchor="mm")

    fiddraw.text((fid.width // 2, 200), "Complete 10 selos e ganhe 1 Copo 500ml", fill=(55, 55, 55), font=get_font('sans_regular', 10), anchor="mm")
    base.alpha_composite(fid, (fid_rect[0], fid_rect[1]))

    # ─── ITEM 3: Porta-Copos em Couro (Bottom-Left) ───
    pc_rect = [90, 580, 400, 880]
    draw_rect_shadow(base, pc_rect, blur=26, offset=(10, 18), opacity=185, corner_radius=20)
    pc = Image.new('RGBA', (pc_rect[2] - pc_rect[0], pc_rect[3] - pc_rect[1]), (28, 28, 32, 255))
    pcdraw = ImageDraw.Draw(pc)
    pcdraw.rounded_rectangle([0, 0, pc.width, pc.height], radius=20, fill=(26, 26, 30, 255), outline=(221, 137, 1, 120), width=2)

    # Textura de couro
    leather_noise = create_noise_texture(pc.width, pc.height, intensity=8, seed=500)
    pc.alpha_composite(leather_noise)
    pcdraw = ImageDraw.Draw(pc)

    gold_pc = apply_gold_mask(clean_logo, 190, 134)
    pc.alpha_composite(gold_pc, ((pc.width - 190) // 2, 40))
    pcdraw.text((pc.width // 2, 205), "PORTA-COPOS BALCÃO", fill=(221, 137, 1), font=get_font('sans', 11), anchor="mm")
    pcdraw.text((pc.width // 2, 230), "Couro Nobre Gravado", fill=(140, 140, 148), font=get_font('sans_light', 10), anchor="mm")
    base.alpha_composite(pc, (pc_rect[0], pc_rect[1]))

    # ─── ITEM 4: Envelope de Talheres Kraft (Right) ───
    env_rect = [1280, 240, 1640, 820]
    draw_rect_shadow(base, env_rect, blur=26, offset=(12, 18), opacity=175, corner_radius=12)

    env_w = env_rect[2] - env_rect[0]
    env_h = env_rect[3] - env_rect[1]
    env_k = create_kraft_texture(env_w, env_h, base_color=(182, 150, 108))
    ekdraw = ImageDraw.Draw(env_k)
    ekdraw.rounded_rectangle([0, 0, env_w, env_h], radius=12, fill=None, outline=(150, 120, 85, 255), width=2)

    gold_env = apply_gold_mask(clean_logo, 200, 140)
    env_k.alpha_composite(gold_env, ((env_w - 200) // 2, 55))
    ekdraw.text((env_w // 2, 230), "COLHER DE BAMBU BIODEGRADÁVEL", fill=(55, 40, 25), font=get_font('sans', 12), anchor="mm")
    ekdraw.line([(40, 260), (env_w - 40, 260)], fill=(140, 110, 75), width=1)
    ekdraw.text((env_w // 2, 400), "Embalagem 100% Biodegradável", fill=(75, 55, 35), font=get_font('sans_light', 11), anchor="mm")
    ekdraw.text((env_w // 2, 425), "& Ecológica", fill=(75, 55, 35), font=get_font('sans_light', 11), anchor="mm")
    ekdraw.text((env_w // 2, 460), "OSHER Açaí Shop Sustentável", fill=(75, 55, 35), font=get_font('serif_regular', 13), anchor="mm")

    base.alpha_composite(env_k, (env_rect[0], env_rect[1]))

    # ─── Badge ───
    tag = Image.new('RGBA', (430, 52), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tag)
    tdraw.rounded_rectangle([0, 0, 430, 52], radius=26, fill=(12, 12, 14, 240), outline=(221, 137, 1, 200), width=2)
    tdraw.text((215, 26), "PAPELARIA DE PONTO DE VENDA & MESA", fill=(221, 137, 1), font=get_font('sans', 13), anchor="mm")
    base.alpha_composite(tag, (60, 50))

    # Ruído fotográfico final
    final_noise = create_noise_texture(W, H, intensity=3, seed=998)
    base.alpha_composite(final_noise)

    final = base.convert('RGB')
    enhancer = ImageEnhance.Contrast(final)
    final = enhancer.enhance(1.08)
    enhancer = ImageEnhance.Sharpness(final)
    final = enhancer.enhance(1.12)

    final.save(os.path.join(ASSETS_DIR, 'osher_papelaria_pdv.jpg'), quality=97)
    print("  ✅ osher_papelaria_pdv.jpg — GERADA!")


# ==============================================================================
# 3. TOTEM ARQUITETÔNICO & FACHADA (SEM PESSOAS)
# ==============================================================================
def render_totem_fachada():
    print("  ⏳ Gerando totem arquitetônico & fachada...")
    W, H = 1800, 1100
    base = Image.new('RGBA', (W, H), (12, 13, 16, 255))
    draw = ImageDraw.Draw(base)

    # ── Parede de ripas metálicas arquitetônicas ──
    for y in range(0, 720):
        t = y / 720
        val = int(20 - t * 7)
        draw.line([(0, y), (W, y)], fill=(val, val, val + 1, 255))

    # Ripas verticais com profundidade 3D
    for x in range(0, W, 40):
        # Face frontal da ripa
        draw.rectangle([x, 0, x + 26, 720], fill=(24, 24, 28, 255))
        # Sombra lateral
        draw.rectangle([x + 26, 0, x + 30, 720], fill=(8, 8, 10, 255))
        # Highlight sutil
        draw.line([(x + 1, 0), (x + 1, 720)], fill=(32, 32, 36, 255), width=1)

    # ── Piso de concreto polido ──
    for y in range(720, H):
        t = (y - 720) / (H - 720)
        val = int(38 - t * 16)
        draw.line([(0, y), (W, y)], fill=(val, val + 1, val + 2, 255))
    draw.line([(0, 720), (W, 720)], fill=(10, 10, 12, 255), width=4)
    # Juntas do piso
    draw.line([(0, 860), (W, 860)], fill=(22, 22, 26, 255), width=2)
    for px in range(250, W, 450):
        draw.line([(px, 720), (px, H)], fill=(22, 22, 26, 255), width=2)

    # ── Iluminação arquitetônica ──
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    # Cone de luz sobre o totem
    gdraw.polygon([(480, 0), (260, 720), (700, 720)], fill=(255, 215, 140, 45))
    # Cone de luz sobre o mostruário
    gdraw.polygon([(1200, 0), (980, 720), (1420, 720)], fill=(255, 215, 140, 38))
    # Luz ambiente quente
    gdraw.ellipse([300, -100, 1500, 500], fill=(255, 210, 140, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    base.alpha_composite(glow)

    # Reflexo no piso
    floor_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fgdraw = ImageDraw.Draw(floor_glow)
    fgdraw.ellipse([250, 740, 750, 1000], fill=(221, 137, 1, 15))
    fgdraw.ellipse([950, 760, 1450, 1020], fill=(221, 137, 1, 12))
    floor_glow = floor_glow.filter(ImageFilter.GaussianBlur(40))
    base.alpha_composite(floor_glow)

    # ── TOTEM MONOLÍTICO (Left) ──
    t_rect = [280, 100, 690, 880]
    draw_rect_shadow(base, t_rect, blur=40, offset=(18, 30), opacity=220, corner_radius=16)

    totem = Image.new('RGBA', (t_rect[2] - t_rect[0], t_rect[3] - t_rect[1]), (18, 18, 20, 255))
    tdraw = ImageDraw.Draw(totem)
    tdraw.rounded_rectangle([0, 0, totem.width, totem.height], radius=16, fill=(20, 20, 23, 255), outline=(40, 40, 48, 255), width=3)

    # Textura brushed metal sutil
    totem_noise = create_noise_texture(totem.width, totem.height, intensity=4, seed=600)
    totem.alpha_composite(totem_noise)
    tdraw = ImageDraw.Draw(totem)

    # Perfis laterais de latão
    left_profile = create_metallic_gold_rect(14, totem.height, angle=90)
    right_profile = create_metallic_gold_rect(14, totem.height, angle=90)
    totem.alpha_composite(left_profile, (0, 0))
    totem.alpha_composite(right_profile, (totem.width - 14, 0))

    # Halo LED interno
    halo = Image.new('RGBA', (totem.width, totem.height), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(halo)
    hdraw.ellipse([40, 30, totem.width - 40, 280], fill=(255, 220, 130, 50))
    halo = halo.filter(ImageFilter.GaussianBlur(30))
    totem.alpha_composite(halo)

    # Logo 3D iluminada
    gold_logo_t = apply_gold_mask(clean_logo, 300, 210)
    totem.alpha_composite(gold_logo_t, ((totem.width - 300) // 2, 45))

    # Slogan com efeito LED
    tdraw.text((totem.width // 2, 285), "AÇAÍ + SORVETE. DO SEU JEITO.", fill=(255, 228, 155), font=get_font('serif', 16), anchor="mm")
    tdraw.line([(40, 315), (totem.width - 40, 315)], fill=(221, 137, 1, 230), width=3)

    # Painel digital do cardápio
    screen = [35, 340, totem.width - 35, 680]
    tdraw.rounded_rectangle(screen, radius=10, fill=(12, 12, 14, 255), outline=(50, 50, 58, 255), width=2)

    # LED glow interno da tela
    screen_glow = Image.new('RGBA', (totem.width, totem.height), (0, 0, 0, 0))
    sgdraw = ImageDraw.Draw(screen_glow)
    sgdraw.rounded_rectangle([screen[0] + 5, screen[1] + 5, screen[2] - 5, screen[3] - 5], radius=8, fill=(221, 137, 1, 12))
    screen_glow = screen_glow.filter(ImageFilter.GaussianBlur(8))
    totem.alpha_composite(screen_glow)
    tdraw = ImageDraw.Draw(totem)

    tdraw.text((totem.width // 2, 375), "— CARDÁPIO DE ENTRADA —", fill=(221, 137, 1), font=get_font('sans', 14), anchor="mm")
    tdraw.text((55, 412), "COPOS MONTADOS DO SEU JEITO", fill=(245, 245, 245), font=get_font('sans', 13))

    menu_items = [
        ("• 300ml Clássico", "R$ 13", False),
        ("• 400ml Especial", "R$ 15", False),
        ("• 500ml OSHER Ouro", "R$ 17", True),
        ("• 700ml Turbinado", "R$ 25", False),
        ("• Mega Pote 1 Litro", "R$ 36", False),
    ]
    yy = 445
    for name, price, highlight in menu_items:
        color = (255, 225, 140) if highlight else (185, 185, 190)
        font = get_font('sans', 12) if highlight else get_font('sans_light', 12)
        tdraw.text((55, yy), name, fill=color, font=font)
        tdraw.text((totem.width - 55, yy), price, fill=color, font=font, anchor="ra")
        yy += 28

    tdraw.line([(55, 595), (totem.width - 55, 595)], fill=(38, 38, 45, 255), width=1)
    tdraw.text((totem.width // 2, 620), "Retire seu pedido ou peça pelo Totem", fill=(155, 155, 165), font=get_font('sans_light', 11), anchor="mm")
    tdraw.text((totem.width // 2, 648), "iFood • Keeta • 99 Food • App Próprio", fill=(221, 137, 1), font=get_font('sans_regular', 12), anchor="mm")

    # Base do totem (pedestal)
    tdraw.rectangle([0, totem.height - 45, totem.width, totem.height], fill=(16, 16, 18, 255))
    pedestal_gold = create_metallic_gold_rect(totem.width, 6, angle=0)
    totem.alpha_composite(pedestal_gold, (0, totem.height - 48))

    base.alpha_composite(totem, (t_rect[0], t_rect[1]))

    # ── MOSTRUÁRIO DE VESTUÁRIO (Right) ──
    # Pedestal/Vitrine
    plinth_rect = [860, 520, 1520, 870]
    draw_rect_shadow(base, plinth_rect, blur=34, offset=(12, 24), opacity=210, corner_radius=14)

    plinth = Image.new('RGBA', (plinth_rect[2] - plinth_rect[0], plinth_rect[3] - plinth_rect[1]), (28, 28, 32, 255))
    pldraw = ImageDraw.Draw(plinth)
    pldraw.rounded_rectangle([0, 0, plinth.width, plinth.height], radius=14, fill=(26, 26, 30, 255), outline=(48, 48, 56, 255), width=2)

    # Faixa de madeira polida no topo
    wood_band = create_metallic_gold_rect(plinth.width, 28, angle=0)
    # Escurecer para parecer madeira
    wood_pixels = wood_band.load()
    for y in range(28):
        for x in range(plinth.width):
            r, g, b, a = wood_pixels[x, y]
            wood_pixels[x, y] = (int(r * 0.72), int(g * 0.55), int(b * 0.45), a)
    plinth.alpha_composite(wood_band, (0, 0))

    pldraw = ImageDraw.Draw(plinth)
    pldraw.text((plinth.width // 2, 190), "MOSTRUÁRIO OFICIAL DE VESTUÁRIO & EQUIPE", fill=(185, 180, 170), font=get_font('sans', 14), anchor="mm")
    pldraw.text((plinth.width // 2, 218), "Algodão nobre 100% penteado • Bordado computadorizado fio ouro", fill=(221, 137, 1), font=get_font('sans_light', 12), anchor="mm")

    base.alpha_composite(plinth, (plinth_rect[0], plinth_rect[1]))

    # Avental de Barista
    apron_rect = [910, 330, 1180, 550]
    draw_rect_shadow(base, apron_rect, blur=22, offset=(8, 16), opacity=185, corner_radius=12)
    apron = Image.new('RGBA', (apron_rect[2] - apron_rect[0], apron_rect[3] - apron_rect[1]), (22, 22, 24, 255))
    adraw = ImageDraw.Draw(apron)
    adraw.rounded_rectangle([0, 0, apron.width, apron.height], radius=12, fill=(24, 24, 28, 255), outline=(40, 40, 46, 255), width=2)

    # Alças de couro
    adraw.rectangle([35, 0, 52, 55], fill=(145, 90, 45, 255))
    adraw.rectangle([apron.width - 52, 0, apron.width - 35, 55], fill=(145, 90, 45, 255))
    adraw.ellipse([38, 50, 48, 60], fill=(221, 137, 1, 255))
    adraw.ellipse([apron.width - 48, 50, apron.width - 38, 60], fill=(221, 137, 1, 255))

    # Bolso com logo
    adraw.rounded_rectangle([28, 75, apron.width - 28, 185], radius=8, fill=(30, 30, 34, 255), outline=(48, 48, 54, 255), width=1)
    gold_apron = apply_gold_mask(clean_logo, 145, 102)
    apron.alpha_composite(gold_apron, ((apron.width - 145) // 2, 78))

    base.alpha_composite(apron, (apron_rect[0], apron_rect[1]))

    # Polo Grafite
    polo_rect = [1210, 350, 1470, 550]
    draw_rect_shadow(base, polo_rect, blur=22, offset=(8, 16), opacity=185, corner_radius=12)
    polo = Image.new('RGBA', (polo_rect[2] - polo_rect[0], polo_rect[3] - polo_rect[1]), (28, 28, 30, 255))
    poldraw = ImageDraw.Draw(polo)
    poldraw.rounded_rectangle([0, 0, polo.width, polo.height], radius=12, fill=(30, 30, 34, 255), outline=(46, 46, 52, 255), width=2)

    # Gola polo dobrada
    poldraw.polygon([(polo.width // 2 - 50, 0), (polo.width // 2, 50), (polo.width // 2 - 28, 65), (polo.width // 2 - 55, 22)], fill=(36, 36, 42, 255))
    poldraw.polygon([(polo.width // 2 + 50, 0), (polo.width // 2, 50), (polo.width // 2 + 28, 65), (polo.width // 2 + 55, 22)], fill=(36, 36, 42, 255))
    poldraw.line([(polo.width // 2, 50), (polo.width // 2, 110)], fill=(20, 20, 24, 255), width=2)
    # Botões
    for by in [55, 80]:
        poldraw.ellipse([polo.width // 2 - 4, by - 4, polo.width // 2 + 4, by + 4], fill=(221, 137, 1, 200))

    # Brasão bordado
    gold_polo = apply_gold_mask(clean_logo, 95, 67)
    polo.alpha_composite(gold_polo, (38, 80))

    base.alpha_composite(polo, (polo_rect[0], polo_rect[1]))

    # ── Vegetação Decorativa (toques de paisagismo sem pessoas) ──
    plant = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    pldraw = ImageDraw.Draw(plant)
    # Folhas de palmeira na esquerda
    for offset_y in range(-40, 80, 40):
        pldraw.arc([-90, 180 + offset_y, 260, 720 + offset_y], start=235, end=345, fill=(15, 42, 22, 180), width=7)
    # Folhas na direita
    for offset_y in range(-30, 60, 30):
        pldraw.arc([1400, 160 + offset_y, 1760, 720 + offset_y], start=195, end=300, fill=(15, 42, 22, 180), width=7)
    plant = plant.filter(ImageFilter.GaussianBlur(3))
    base.alpha_composite(plant)

    # ── Detalhe: Letreiro LED dourado acima da porta ──
    sign_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sgd = ImageDraw.Draw(sign_glow)
    sgd.rounded_rectangle([740, 60, 1080, 120], radius=8, fill=(221, 137, 1, 35))
    sign_glow = sign_glow.filter(ImageFilter.GaussianBlur(15))
    base.alpha_composite(sign_glow)
    draw = ImageDraw.Draw(base)
    draw.text((910, 85), "OSHER AÇAÍ SHOP", fill=(255, 225, 140, 200), font=get_font('serif', 20), anchor="mm")

    # ── Badge ──
    tag = Image.new('RGBA', (470, 52), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tag)
    tdraw.rounded_rectangle([0, 0, 470, 52], radius=26, fill=(12, 12, 14, 240), outline=(221, 137, 1, 200), width=2)
    tdraw.text((235, 26), "TOTEM ARQUITETÔNICO & VESTUÁRIO OFICIAL", fill=(221, 137, 1), font=get_font('sans', 13), anchor="mm")
    base.alpha_composite(tag, (60, 25))

    # Ruído fotográfico
    final_noise = create_noise_texture(W, H, intensity=3, seed=997)
    base.alpha_composite(final_noise)

    final = base.convert('RGB')
    enhancer = ImageEnhance.Contrast(final)
    final = enhancer.enhance(1.1)
    enhancer = ImageEnhance.Sharpness(final)
    final = enhancer.enhance(1.15)

    final.save(os.path.join(ASSETS_DIR, 'osher_totem_fachada.jpg'), quality=97)
    print("  ✅ osher_totem_fachada.jpg — GERADA (100% SEM PESSOAS)!")


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  OSHER Açaí Shop — Geração de Mockups Premium")
    print("=" * 60)
    render_stationery_luxury()
    render_stationery_pdv()
    render_totem_fachada()
    print("=" * 60)
    print("  🎉 Todas as 3 imagens foram geradas com sucesso!")
    print("=" * 60)
