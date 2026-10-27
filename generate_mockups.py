import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ASSETS_DIR = 'c:/Users/Windows/Documents/PROJETOS I.A/OSHER/assets'
os.makedirs(ASSETS_DIR, exist_ok=True)

clean_logo_path = os.path.join(ASSETS_DIR, 'osher_logo_clean.png')
if not os.path.exists(clean_logo_path):
    cover = Image.open(os.path.join(ASSETS_DIR, 'osher_logo_cover.png'))
    bbox = cover.getbbox()
    clean_logo = cover.crop(bbox)
    clean_logo.save(clean_logo_path)
else:
    clean_logo = Image.open(clean_logo_path)

def get_font(name, size):
    font_map = {
        'serif': 'C:/Windows/Fonts/georgiab.ttf',
        'serif_regular': 'C:/Windows/Fonts/georgia.ttf',
        'sans': 'C:/Windows/Fonts/segoeuib.ttf',
        'sans_regular': 'C:/Windows/Fonts/segoeui.ttf',
        'sans_light': 'C:/Windows/Fonts/segoeuil.ttf',
    }
    path = font_map.get(name, 'C:/Windows/Fonts/arial.ttf')
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_rect_shadow(img, rect, blur=18, offset=(0, 14), opacity=150, corner_radius=8):
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
    
    pos = (int(x1 - pad), int(y1 - pad))
    img.alpha_composite(shadow, pos)

def create_metallic_gold_rect(w, h, angle=35):
    grad = Image.new('RGBA', (w, h))
    pixels = grad.load()
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    max_d = abs(w * cos_a) + abs(h * sin_a)
    
    c1 = (180, 110, 5)     # escuro
    c2 = (221, 137, 1)     # base ouro
    c3 = (255, 230, 160)   # brilho especular
    c4 = (235, 165, 30)    # ouro vivo
    
    for y in range(h):
        for x in range(w):
            d = ((x * cos_a + y * sin_a) / max_d * 2.5) % 1.0
            if d < 0.3:
                t = d / 0.3
                r = int(c1[0] + t * (c2[0] - c1[0]))
                g = int(c1[1] + t * (c2[1] - c1[1]))
                b = int(c1[2] + t * (c2[2] - c1[2]))
            elif d < 0.6:
                t = (d - 0.3) / 0.3
                r = int(c2[0] + t * (c3[0] - c2[0]))
                g = int(c2[1] + t * (c3[1] - c2[1]))
                b = int(c2[2] + t * (c3[2] - c2[2]))
            else:
                t = (d - 0.6) / 0.4
                r = int(c3[0] + t * (c4[0] - c3[0]))
                g = int(c3[1] + t * (c4[1] - c3[1]))
                b = int(c3[2] + t * (c4[2] - c3[2]))
            pixels[x, y] = (r, g, b, 255)
    return grad

def apply_gold_mask(logo_img, target_w, target_h):
    resized = logo_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    if resized.mode != 'RGBA':
        resized = resized.convert('RGBA')
    gold = create_metallic_gold_rect(target_w, target_h)
    r, g, b, a = resized.split()
    gold.putalpha(a)
    return gold

# ==============================================================================
# 1. PAPELARIA CORPORATIVA LUXO (assets/osher_papelaria_corporativa.jpg)
# ==============================================================================
def render_stationery_luxury():
    W, H = 1600, 1000
    base = Image.new('RGBA', (W, H), (18, 18, 20, 255))
    draw = ImageDraw.Draw(base)
    
    # Ambient texture gradient & soft vignette
    for y in range(H):
        t = y / H
        col = int(22 - t * 8)
        draw.line([(0, y), (W, y)], fill=(col, col, col + 2, 255))
    
    # Warm directional light spotlight from top-left
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([-200, -200, 900, 800], fill=(221, 137, 1, 28))
    gdraw.ellipse([600, -100, 1700, 700], fill=(240, 220, 180, 16))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    base.alpha_composite(glow)
    
    # Grid lines / presentation guidelines (subtle architectural luxury)
    for x in range(100, W, 200):
        draw.line([(x, 40), (x, H - 40)], fill=(32, 32, 36, 120), width=1)
    for y in range(80, H, 160):
        draw.line([(40, y), (W - 40, y)], fill=(32, 32, 36, 120), width=1)

    # ITEM 1: Pasta Corporativa / Presentation Folder (Left-Center)
    f_rect = [100, 140, 680, 880]
    draw_rect_shadow(base, f_rect, blur=28, offset=(10, 22), opacity=170, corner_radius=12)
    
    folder = Image.new('RGBA', (f_rect[2] - f_rect[0], f_rect[3] - f_rect[1]), (26, 26, 28, 255))
    fdraw = ImageDraw.Draw(folder)
    # Subtle matte leather/soft touch texture
    fdraw.rounded_rectangle([0, 0, folder.width, folder.height], radius=12, fill=(28, 28, 32, 255), outline=(50, 50, 56, 255), width=1)
    
    # Gold hot-stamped filigree divider on folder
    fdraw.line([(40, 480), (folder.width - 40, 480)], fill=(221, 137, 1, 180), width=2)
    fdraw.line([(folder.width//2 - 60, 485), (folder.width//2 + 60, 485)], fill=(255, 215, 120, 220), width=1)
    
    # Gold Logo on Folder
    gold_logo_f = apply_gold_mask(clean_logo, 340, 240)
    folder.alpha_composite(gold_logo_f, ((folder.width - 340) // 2, 170))
    
    # Typography on Folder
    font_serif = get_font('serif', 22)
    font_sans = get_font('sans_light', 13)
    font_sans_b = get_font('sans', 14)
    
    fdraw.text((folder.width // 2, 530), "MANUAL DE IDENTIDADE VISUAL", fill=(245, 235, 220), font=font_serif, anchor="mm")
    fdraw.text((folder.width // 2, 570), "DIRETRIZES DE MARCA • BRANDKIT EXECUTIVO 2026", fill=(195, 145, 60), font=font_sans_b, anchor="mm")
    fdraw.text((folder.width // 2, 670), "OSHER AÇAÍ SHOP • BRASÍLIA / GUARÁ I", fill=(140, 140, 150), font=font_sans, anchor="mm")
    
    base.alpha_composite(folder, (f_rect[0], f_rect[1]))

    # ITEM 2: Papel Timbrado / Letterhead A4 (Center-Right)
    l_rect = [620, 110, 1160, 850]
    draw_rect_shadow(base, l_rect, blur=24, offset=(12, 20), opacity=160, corner_radius=6)
    
    letter = Image.new('RGBA', (l_rect[2] - l_rect[0], l_rect[3] - l_rect[1]), (248, 246, 240, 255))
    ldraw = ImageDraw.Draw(letter)
    ldraw.rounded_rectangle([0, 0, letter.width, letter.height], radius=6, fill=(248, 246, 240, 255), outline=(210, 205, 195, 255), width=1)
    
    # Header gold crest
    gold_logo_sm = apply_gold_mask(clean_logo, 160, 112)
    letter.alpha_composite(gold_logo_sm, (50, 40))
    
    ldraw.text((230, 68), "OSHER AÇAÍ SHOP", fill=(30, 30, 30), font=get_font('serif', 20))
    ldraw.text((230, 96), "Açaí + Sorvete. Do seu jeito.", fill=(180, 115, 10), font=get_font('serif_regular', 13))
    ldraw.line([(50, 165), (letter.width - 50, 165)], fill=(221, 137, 1, 200), width=1)
    
    # Body text simulation
    for idx, y_pos in enumerate(range(210, 620, 24)):
        lineWidth = letter.width - 100
        if idx in (3, 7, 12):
            lineWidth -= 120
        ldraw.line([(50, y_pos), (50 + lineWidth, y_pos)], fill=(215, 210, 200, 255), width=2)
    
    # Footer
    ldraw.line([(50, 680), (letter.width - 50, 680)], fill=(220, 215, 205, 255), width=1)
    ldraw.text((50, 696), "Guará I • Brasília - DF | contato@osheracai.com.br | www.osheracai.com.br", fill=(130, 125, 115), font=get_font('sans_light', 11))
    
    base.alpha_composite(letter, (l_rect[0], l_rect[1]))

    # ITEM 3: Envelope Preto com Lacre de Cera Dourada (Top-Right)
    e_rect = [1080, 140, 1540, 460]
    draw_rect_shadow(base, e_rect, blur=22, offset=(8, 16), opacity=180, corner_radius=8)
    
    env = Image.new('RGBA', (e_rect[2] - e_rect[0], e_rect[3] - e_rect[1]), (22, 22, 24, 255))
    edraw = ImageDraw.Draw(env)
    edraw.rounded_rectangle([0, 0, env.width, env.height], radius=8, fill=(24, 24, 26, 255), outline=(45, 45, 50, 255), width=1)
    # Flap lines
    edraw.polygon([(0, 0), (env.width // 2, 190), (env.width, 0)], fill=(32, 32, 36, 255), outline=(60, 60, 68, 255))
    
    # Wax seal (gold 3D medallion in center of flap)
    seal_center = (env.width // 2, 190)
    edraw.ellipse([seal_center[0] - 38, seal_center[1] - 38, seal_center[0] + 38, seal_center[1] + 38], fill=(185, 115, 10, 255))
    edraw.ellipse([seal_center[0] - 34, seal_center[1] - 34, seal_center[0] + 34, seal_center[1] + 34], fill=(221, 137, 1, 255))
    edraw.ellipse([seal_center[0] - 30, seal_center[1] - 30, seal_center[0] + 30, seal_center[1] + 30], fill=(255, 215, 120, 255))
    edraw.ellipse([seal_center[0] - 26, seal_center[1] - 26, seal_center[0] + 26, seal_center[1] + 26], fill=(215, 130, 5, 255))
    edraw.text(seal_center, "O", fill=(255, 245, 220), font=get_font('serif', 26), anchor="mm")
    
    base.alpha_composite(env, (e_rect[0], e_rect[1]))

    # ITEM 4: Cartões de Visita Frente & Verso (Bottom-Right)
    # Cartão 1: Frente (Fundo Grafite + Hot Stamping Dourado)
    c1_rect = [1120, 510, 1520, 730]
    draw_rect_shadow(base, c1_rect, blur=20, offset=(8, 14), opacity=180, corner_radius=6)
    card1 = Image.new('RGBA', (c1_rect[2] - c1_rect[0], c1_rect[3] - c1_rect[1]), (26, 26, 28, 255))
    c1draw = ImageDraw.Draw(card1)
    c1draw.rounded_rectangle([0, 0, card1.width, card1.height], radius=6, fill=(24, 24, 26, 255), outline=(221, 137, 1, 120), width=1)
    # Gold edge gilding simulation
    c1draw.line([(0, 0), (card1.width, 0)], fill=(255, 215, 120, 220), width=2)
    
    gold_c1 = apply_gold_mask(clean_logo, 200, 140)
    card1.alpha_composite(gold_c1, ((card1.width - 200) // 2, 25))
    c1draw.text((card1.width // 2, 180), "Açaí + Sorvete. Do seu jeito.", fill=(221, 137, 1), font=get_font('serif_regular', 12), anchor="mm")
    base.alpha_composite(card1, (c1_rect[0], c1_rect[1]))

    # Cartão 2: Verso (Dados de Contato e Cargo)
    c2_rect = [1040, 720, 1440, 940]
    draw_rect_shadow(base, c2_rect, blur=22, offset=(8, 16), opacity=190, corner_radius=6)
    card2 = Image.new('RGBA', (c2_rect[2] - c2_rect[0], c2_rect[3] - c2_rect[1]), (24, 24, 26, 255))
    c2draw = ImageDraw.Draw(card2)
    c2draw.rounded_rectangle([0, 0, card2.width, card2.height], radius=6, fill=(28, 28, 30, 255), outline=(55, 55, 62, 255), width=1)
    
    c2draw.text((35, 38), "RAFAEL LIMA", fill=(250, 245, 235), font=get_font('sans', 15))
    c2draw.text((35, 60), "Diretor de Marca & Expansão", fill=(221, 137, 1), font=get_font('sans_regular', 12))
    c2draw.line([(35, 88), (card2.width - 35, 88)], fill=(60, 60, 68, 255), width=1)
    
    c2draw.text((35, 110), "Tel: +55 (61) 98123-4567", fill=(200, 200, 205), font=get_font('sans_light', 11))
    c2draw.text((35, 134), "Email: rafael@osheracai.com.br", fill=(200, 200, 205), font=get_font('sans_light', 11))
    c2draw.text((35, 158), "Local: Guara I - Brasilia - DF", fill=(200, 200, 205), font=get_font('sans_light', 11))
    c2draw.text((35, 182), "Site: www.osheracai.com.br", fill=(221, 137, 1), font=get_font('sans_regular', 11))
    base.alpha_composite(card2, (c2_rect[0], c2_rect[1]))

    # ITEM 5: Caneta Executiva Dourada de Metal
    pen_rect = [920, 220, 946, 760]
    draw_rect_shadow(base, pen_rect, blur=18, offset=(14, 12), opacity=150, corner_radius=12)
    pen = create_metallic_gold_rect(pen_rect[2] - pen_rect[0], pen_rect[3] - pen_rect[1], angle=90)
    pdraw = ImageDraw.Draw(pen)
    pdraw.rounded_rectangle([0, 0, pen.width, pen.height], radius=12, fill=None, outline=(150, 90, 5, 255), width=1)
    # Pen clip and grip rings
    pdraw.rectangle([6, 30, 20, 220], fill=(255, 240, 180, 255))
    pdraw.line([(0, 380), (pen.width, 380)], fill=(90, 50, 0, 255), width=3)
    pdraw.line([(0, 386), (pen.width, 386)], fill=(255, 240, 180, 255), width=2)
    base.alpha_composite(pen, (pen_rect[0], pen_rect[1]))

    # Badge overlay: Papelaria & Identidade Corporativa
    tag = Image.new('RGBA', (360, 48), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tag)
    tdraw.rounded_rectangle([0, 0, 360, 48], radius=24, fill=(15, 15, 17, 230), outline=(221, 137, 1, 180), width=1)
    tdraw.text((180, 24), "PAPELARIA CORPORATIVA • 2026", fill=(221, 137, 1), font=get_font('sans', 12), anchor="mm")
    base.alpha_composite(tag, (60, 60))

    final = base.convert('RGB')
    final.save(os.path.join(ASSETS_DIR, 'osher_papelaria_corporativa.jpg'), quality=96)
    print("osher_papelaria_corporativa.jpg gerada com sucesso!")

# ==============================================================================
# 2. PAPELARIA DE PONTO DE VENDA & BALCÃO (assets/osher_papelaria_pdv.jpg)
# ==============================================================================
def render_stationery_pdv():
    W, H = 1600, 1000
    base = Image.new('RGBA', (W, H), (20, 20, 22, 255))
    draw = ImageDraw.Draw(base)
    
    # Dark Nero Marquina Marble background simulation
    for y in range(H):
        t = y / H
        val = int(24 - t * 10)
        draw.line([(0, y), (W, y)], fill=(val, val, val + 2, 255))
    
    # Marble gold & white delicate veins
    veins = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(veins)
    vdraw.line([(0, 200), (350, 350), (700, 280), (1200, 550), (1600, 480)], fill=(221, 137, 1, 30), width=2)
    vdraw.line([(200, 0), (600, 450), (900, 600), (1400, 950)], fill=(240, 230, 210, 22), width=1)
    vdraw.line([(800, 0), (1100, 320), (1500, 420)], fill=(221, 137, 1, 25), width=2)
    veins = veins.filter(ImageFilter.GaussianBlur(3))
    base.alpha_composite(veins)
    
    # Warm counter spotlight
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([200, 50, 1300, 850], fill=(255, 210, 140, 28))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base.alpha_composite(glow)

    # ITEM 1: Display de Mesa em Latão Dourado e Acrílico (Center)
    dt_rect = [460, 120, 1080, 880]
    draw_rect_shadow(base, dt_rect, blur=32, offset=(10, 25), opacity=180, corner_radius=16)
    
    # Brass base stand
    stand_rect = [420, 870, 1120, 930]
    draw_rect_shadow(base, stand_rect, blur=16, offset=(0, 18), opacity=200, corner_radius=10)
    stand = create_metallic_gold_rect(stand_rect[2] - stand_rect[0], stand_rect[3] - stand_rect[1], angle=0)
    base.alpha_composite(stand, (stand_rect[0], stand_rect[1]))

    # Menu Card inside Display
    menu = Image.new('RGBA', (dt_rect[2] - dt_rect[0], dt_rect[3] - dt_rect[1]), (25, 25, 27, 255))
    mdraw = ImageDraw.Draw(menu)
    mdraw.rounded_rectangle([0, 0, menu.width, menu.height], radius=16, fill=(24, 24, 26, 255), outline=(221, 137, 1, 180), width=2)
    
    # Top Gold Logo on Menu
    gold_logo_m = apply_gold_mask(clean_logo, 260, 182)
    menu.alpha_composite(gold_logo_m, ((menu.width - 260) // 2, 40))
    
    mdraw.text((menu.width // 2, 235), "CARDÁPIO DE BALCÃO & MESA", fill=(255, 220, 140), font=get_font('sans', 13), anchor="mm")
    mdraw.text((menu.width // 2, 265), "Açaí + Sorvete. Do seu jeito.", fill=(240, 235, 225), font=get_font('serif', 20), anchor="mm")
    mdraw.line([(60, 295), (menu.width - 60, 295)], fill=(221, 137, 1, 200), width=1)
    
    # Menu Items List
    items = [
        ("Copo Clássico 300ml", "1 Sorvete + 2 Caldas + 2 Toppings", "R$ 13,00"),
        ("Copo Especial 400ml", "Açaí cremoso + 2 Sorvetes + 3 Toppings", "R$ 15,00"),
        ("Copo OSHER 500ml", "Monte do seu jeito • Mais pedido", "R$ 17,00"),
        ("Bowl Cerâmico 600ml", "Experiência de salão + Frutas frescas", "R$ 22,00"),
        ("Mega Pote Família 1000ml", "1 Litro artesanal para levar ou mesa", "R$ 36,00")
    ]
    
    y_start = 325
    for title, desc, price in items:
        mdraw.text((60, y_start), title, fill=(250, 245, 235), font=get_font('serif', 17))
        mdraw.text((60, y_start + 24), desc, fill=(160, 155, 145), font=get_font('sans_light', 12))
        mdraw.text((menu.width - 60, y_start + 10), price, fill=(221, 137, 1), font=get_font('sans', 18), anchor="ra")
        mdraw.line([(60, y_start + 54), (menu.width - 60, y_start + 54)], fill=(45, 45, 50, 255), width=1)
        y_start += 72
        
    mdraw.text((menu.width // 2, 700), "Caldas Especiais: Mel Puro • Brigadeiro Nobre • Pistache Artesanal", fill=(200, 160, 90), font=get_font('sans_regular', 11), anchor="mm")
    mdraw.text((menu.width // 2, 725), "Peça pelo WhatsApp ou App Oficial OSHER", fill=(140, 140, 145), font=get_font('sans_light', 11), anchor="mm")
    base.alpha_composite(menu, (dt_rect[0], dt_rect[1]))

    # ITEM 2: Cartões Fidelidade "OSHER Club" (Left Side)
    fid_rect = [90, 280, 420, 490]
    draw_rect_shadow(base, fid_rect, blur=22, offset=(8, 14), opacity=170, corner_radius=10)
    fid = Image.new('RGBA', (fid_rect[2] - fid_rect[0], fid_rect[3] - fid_rect[1]), (248, 245, 238, 255))
    fiddraw = ImageDraw.Draw(fid)
    fiddraw.rounded_rectangle([0, 0, fid.width, fid.height], radius=10, fill=(248, 245, 238, 255), outline=(221, 137, 1, 150), width=1)
    
    fiddraw.text((25, 25), "OSHER CLUB", fill=(25, 25, 28), font=get_font('serif', 18))
    fiddraw.text((25, 48), "Cartão Fidelidade 10 Selos", fill=(180, 115, 10), font=get_font('sans', 11))
    
    # 10 stamp circles (2 rows of 5)
    for row in range(2):
        for col in range(5):
            cx = 38 + col * 58
            cy = 95 + row * 48
            stamped = (row == 0 and col < 4)
            if stamped:
                fiddraw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(221, 137, 1, 230))
                fiddraw.text((cx, cy), "★", fill=(255, 255, 255), font=get_font('sans', 14), anchor="mm")
            else:
                fiddraw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=None, outline=(180, 175, 165), width=2)
                fiddraw.text((cx, cy), str(row * 5 + col + 1), fill=(160, 155, 145), font=get_font('sans', 11), anchor="mm")
                
    fiddraw.text((fid.width // 2, 190), "Complete 10 selos e ganhe 1 Copo 500ml", fill=(60, 60, 60), font=get_font('sans_regular', 10), anchor="mm")
    base.alpha_composite(fid, (fid_rect[0], fid_rect[1]))

    # ITEM 3: Porta-Copos Hexagonal em Couro Escuro com Monograma Dourado (Bottom-Left)
    pc_rect = [120, 580, 380, 840]
    draw_rect_shadow(base, pc_rect, blur=24, offset=(8, 16), opacity=180, corner_radius=18)
    pc = Image.new('RGBA', (pc_rect[2] - pc_rect[0], pc_rect[3] - pc_rect[1]), (26, 26, 30, 255))
    pcdraw = ImageDraw.Draw(pc)
    pcdraw.rounded_rectangle([0, 0, pc.width, pc.height], radius=18, fill=(28, 28, 32, 255), outline=(221, 137, 1, 100), width=1)
    
    gold_pc = apply_gold_mask(clean_logo, 170, 120)
    pc.alpha_composite(gold_pc, ((pc.width - 170) // 2, 45))
    pcdraw.text((pc.width // 2, 195), "PORTA-COPOS BALCÃO", fill=(221, 137, 1), font=get_font('sans', 10), anchor="mm")
    base.alpha_composite(pc, (pc_rect[0], pc_rect[1]))

    # ITEM 4: Envelope de Talheres Kraft Ecológico (Right Side)
    env_rect = [1180, 260, 1500, 780]
    draw_rect_shadow(base, env_rect, blur=24, offset=(10, 16), opacity=170, corner_radius=10)
    env_k = Image.new('RGBA', (env_rect[2] - env_rect[0], env_rect[3] - env_rect[1]), (185, 155, 120, 255))
    ekdraw = ImageDraw.Draw(env_k)
    ekdraw.rounded_rectangle([0, 0, env_k.width, env_k.height], radius=10, fill=(180, 145, 110, 255), outline=(150, 115, 80, 255), width=1)
    
    # Dark graphite stamp on kraft
    gold_env = apply_gold_mask(clean_logo, 180, 126)
    env_k.alpha_composite(gold_env, ((env_k.width - 180) // 2, 60))
    ekdraw.text((env_k.width // 2, 220), "COLHER DE BAMBU BIODEGRADÁVEL", fill=(60, 45, 30), font=get_font('sans', 11), anchor="mm")
    ekdraw.line([(40, 250), (env_k.width - 40, 250)], fill=(150, 115, 80), width=1)
    ekdraw.text((env_k.width // 2, 380), "Embalagem 100% Biodegradavel e Ecologica", fill=(80, 60, 40), font=get_font('sans_light', 11), anchor="mm")
    ekdraw.text((env_k.width // 2, 410), "OSHER Acai Shop Sustentavel", fill=(80, 60, 40), font=get_font('serif_regular', 12), anchor="mm")
    base.alpha_composite(env_k, (env_rect[0], env_rect[1]))

    # Badge overlay: Papelaria de Balcão & Ponto de Venda
    tag = Image.new('RGBA', (380, 48), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tag)
    tdraw.rounded_rectangle([0, 0, 380, 48], radius=24, fill=(15, 15, 17, 230), outline=(221, 137, 1, 180), width=1)
    tdraw.text((190, 24), "PAPELARIA DE PONTO DE VENDA & MESA", fill=(221, 137, 1), font=get_font('sans', 12), anchor="mm")
    base.alpha_composite(tag, (60, 60))

    final = base.convert('RGB')
    final.save(os.path.join(ASSETS_DIR, 'osher_papelaria_pdv.jpg'), quality=96)
    print("osher_papelaria_pdv.jpg gerada com sucesso!")

# ==============================================================================
# 3. TOTEM ARQUITETÔNICO & MOSTRUÁRIO DE UNIFORMES (assets/osher_totem_fachada.jpg)
#    CRÍTICO: SEM NENHUMA PESSOA! (100% ZERO HUMANOS)
# ==============================================================================
def render_totem_fachada():
    W, H = 1600, 1000
    base = Image.new('RGBA', (W, H), (14, 15, 18, 255))
    draw = ImageDraw.Draw(base)
    
    # Modern boutique exterior facade (matte black slatted wall & warm terrazzo floor)
    # Background wall
    for y in range(0, 680):
        t = y / 680
        val = int(22 - t * 8)
        draw.line([(0, y), (W, y)], fill=(val, val, val + 2, 255))
        
    # Vertical architectural timber/metal slats
    for x in range(0, W, 36):
        draw.line([(x, 0), (x, 680)], fill=(28, 28, 32, 255), width=24)
        draw.line([(x + 24, 0), (x + 24, 680)], fill=(8, 8, 10, 255), width=12)
        
    # Floor: Polished concrete / terrazzo pavers
    for y in range(680, H):
        t = (y - 680) / (H - 680)
        val = int(36 - t * 14)
        draw.line([(0, y), (W, y)], fill=(val, val + 1, val + 2, 255))
    # Paver joint line
    draw.line([(0, 680), (W, 680)], fill=(12, 12, 14, 255), width=3)
    draw.line([(0, 830), (W, 830)], fill=(24, 24, 28, 255), width=2)
    for x in range(200, W, 400):
        draw.line([(x, 680), (x, H)], fill=(24, 24, 28, 255), width=2)

    # Warm architectural up-lights on facade
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    # Cone light 1 (above totem)
    gdraw.polygon([(460, 0), (250, 680), (670, 680)], fill=(255, 210, 140, 42))
    # Cone light 2 (above merchandising plinth)
    gdraw.polygon([(1150, 0), (950, 680), (1350, 680)], fill=(255, 210, 140, 36))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    base.alpha_composite(glow)

    # -------------------------------------------------------------------------
    # ELEMENTO 1: TOTEM MONOLÍTICO EXTERNO ILUMINADO (Left Side)
    # -------------------------------------------------------------------------
    t_rect = [280, 140, 640, 840]
    draw_rect_shadow(base, t_rect, blur=36, offset=(16, 28), opacity=210, corner_radius=14)
    
    totem = Image.new('RGBA', (t_rect[2] - t_rect[0], t_rect[3] - t_rect[1]), (20, 20, 22, 255))
    tdraw = ImageDraw.Draw(totem)
    # Totem body: Matte anthracite brushed metal
    tdraw.rounded_rectangle([0, 0, totem.width, totem.height], radius=14, fill=(22, 22, 25, 255), outline=(45, 45, 52, 255), width=2)
    
    # Brushed brass side profiles
    tdraw.rectangle([0, 0, 12, totem.height], fill=(221, 137, 1, 230))
    tdraw.rectangle([totem.width - 12, 0, totem.width, totem.height], fill=(221, 137, 1, 230))
    
    # Internal LED Halo Box
    halo = Image.new('RGBA', (totem.width, totem.height), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(halo)
    hdraw.ellipse([50, 40, totem.width - 50, 260], fill=(255, 215, 120, 45))
    halo = halo.filter(ImageFilter.GaussianBlur(25))
    totem.alpha_composite(halo)
    
    # Glowing 3D Dimensional Logo on Totem
    gold_logo_t = apply_gold_mask(clean_logo, 260, 182)
    totem.alpha_composite(gold_logo_t, ((totem.width - 260) // 2, 60))
    
    # Slogan with warm LED backlight
    tdraw.text((totem.width // 2, 270), "ACAI + SORVETE. DO SEU JEITO.", fill=(255, 225, 150), font=get_font('serif', 15), anchor="mm")
    tdraw.line([(40, 305), (totem.width - 40, 305)], fill=(221, 137, 1, 220), width=2)
    
    # Digital / Illuminated Menu Panel on Totem
    screen_rect = [32, 330, totem.width - 32, 640]
    tdraw.rounded_rectangle(screen_rect, radius=8, fill=(14, 14, 16, 255), outline=(55, 55, 65, 255), width=1)
    
    tdraw.text((totem.width // 2, 360), "- CARDAPIO DE ENTRADA -", fill=(221, 137, 1), font=get_font('sans', 13), anchor="mm")
    tdraw.text((50, 395), "COPOS MONTADOS DO SEU JEITO", fill=(240, 240, 240), font=get_font('sans', 12))
    tdraw.text((50, 420), "• 300ml Clássico .................. R$ 13", fill=(190, 190, 195), font=get_font('sans_light', 11))
    tdraw.text((50, 445), "• 400ml Especial .................. R$ 15", fill=(190, 190, 195), font=get_font('sans_light', 11))
    tdraw.text((50, 470), "• 500ml OSHER Ouro .............. R$ 17", fill=(255, 215, 120), font=get_font('sans', 11))
    tdraw.text((50, 495), "• 700ml Turbinado ................ R$ 25", fill=(190, 190, 195), font=get_font('sans_light', 11))
    tdraw.text((50, 520), "• Mega Pote 1 Litro .............. R$ 36", fill=(190, 190, 195), font=get_font('sans_light', 11))
    
    tdraw.line([(50, 555), (totem.width - 50, 555)], fill=(40, 40, 48, 255), width=1)
    tdraw.text((totem.width // 2, 580), "Retire seu pedido ou peça pelo Totem", fill=(160, 160, 170), font=get_font('sans_light', 11), anchor="mm")
    tdraw.text((totem.width // 2, 605), "iFood • Keeta • 99 Food • App Próprio", fill=(221, 137, 1), font=get_font('sans_regular', 11), anchor="mm")
    
    base.alpha_composite(totem, (t_rect[0], t_rect[1]))

    # -------------------------------------------------------------------------
    # ELEMENTO 2: PEDESTAL EXPOSITOR DE UNIFORMES (Center-Right)
    #             (Avental de Barista e Polo Grafite dobrados, sem pessoas!)
    # -------------------------------------------------------------------------
    plinth_rect = [860, 560, 1420, 860]
    draw_rect_shadow(base, plinth_rect, blur=30, offset=(10, 22), opacity=200, corner_radius=12)
    
    plinth = Image.new('RGBA', (plinth_rect[2] - plinth_rect[0], plinth_rect[3] - plinth_rect[1]), (30, 30, 34, 255))
    pdraw = ImageDraw.Draw(plinth)
    pdraw.rounded_rectangle([0, 0, plinth.width, plinth.height], radius=12, fill=(28, 28, 32, 255), outline=(50, 50, 58, 255), width=2)
    # Polished oak top band on plinth
    pdraw.rectangle([0, 0, plinth.width, 24], fill=(160, 115, 75, 255))
    pdraw.line([(0, 24), (plinth.width, 24)], fill=(120, 85, 50, 255), width=2)
    pdraw.text((plinth.width // 2, 180), "MOSTRUÁRIO OFICIAL DE VESTUÁRIO & EQUIPE", fill=(180, 175, 165), font=get_font('sans', 13), anchor="mm")
    pdraw.text((plinth.width // 2, 210), "Algodão nobre 100% penteado • Bordado computadorizado fio ouro", fill=(221, 137, 1), font=get_font('sans_light', 11), anchor="mm")
    base.alpha_composite(plinth, (plinth_rect[0], plinth_rect[1]))

    # UNIFORME 1: Avental de Barista Dobrado com Bordado Dourado (Esquerda no pedestal)
    apron_rect = [900, 380, 1130, 580]
    draw_rect_shadow(base, apron_rect, blur=20, offset=(6, 14), opacity=180, corner_radius=10)
    apron = Image.new('RGBA', (apron_rect[2] - apron_rect[0], apron_rect[3] - apron_rect[1]), (24, 24, 26, 255))
    adraw = ImageDraw.Draw(apron)
    adraw.rounded_rectangle([0, 0, apron.width, apron.height], radius=10, fill=(26, 26, 28, 255), outline=(42, 42, 46, 255), width=1)
    
    # Leather straps on apron
    adraw.rectangle([30, 0, 45, 50], fill=(140, 85, 45, 255))
    adraw.rectangle([apron.width - 45, 0, apron.width - 30, 50], fill=(140, 85, 45, 255))
    adraw.ellipse([34, 45, 41, 52], fill=(221, 137, 1, 255))
    adraw.ellipse([apron.width - 41, 45, apron.width - 34, 52], fill=(221, 137, 1, 255))
    
    # Front pocket with gold logo
    adraw.rounded_rectangle([25, 70, apron.width - 25, 175], radius=6, fill=(32, 32, 36, 255), outline=(50, 50, 56, 255), width=1)
    gold_apron = apply_gold_mask(clean_logo, 130, 92)
    apron.alpha_composite(gold_apron, ((apron.width - 130) // 2, 75))
    base.alpha_composite(apron, (apron_rect[0], apron_rect[1]))

    # UNIFORME 2: Camiseta Polo Grafite Dobrada (Direita no pedestal)
    polo_rect = [1160, 400, 1390, 580]
    draw_rect_shadow(base, polo_rect, blur=20, offset=(6, 14), opacity=180, corner_radius=10)
    polo = Image.new('RGBA', (polo_rect[2] - polo_rect[0], polo_rect[3] - polo_rect[1]), (28, 28, 30, 255))
    poldraw = ImageDraw.Draw(polo)
    poldraw.rounded_rectangle([0, 0, polo.width, polo.height], radius=10, fill=(30, 30, 34, 255), outline=(48, 48, 54, 255), width=1)
    
    # Polo collar fold
    poldraw.polygon([(polo.width // 2 - 45, 0), (polo.width // 2, 45), (polo.width // 2 - 25, 60), (polo.width // 2 - 50, 20)], fill=(36, 36, 42, 255))
    poldraw.polygon([(polo.width // 2 + 45, 0), (polo.width // 2, 45), (polo.width // 2 + 25, 60), (polo.width // 2 + 50, 20)], fill=(36, 36, 42, 255))
    poldraw.line([(polo.width // 2, 45), (polo.width // 2, 100)], fill=(22, 22, 26, 255), width=2)
    
    # Embroidered chest emblem
    gold_polo = apply_gold_mask(clean_logo, 85, 60)
    polo.alpha_composite(gold_polo, (35, 75))
    base.alpha_composite(polo, (polo_rect[0], polo_rect[1]))

    # Foliage: Tropical Potted Plant Silhouette (Luxury Hospitality touch on left/right edge)
    plant = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    pldraw = ImageDraw.Draw(plant)
    # Palm fronds on far left
    pldraw.arc([-80, 200, 250, 700], start=240, end=350, fill=(18, 45, 25, 200), width=6)
    pldraw.arc([-80, 280, 220, 800], start=260, end=360, fill=(22, 55, 30, 220), width=7)
    # Palm fronds on far right
    pldraw.arc([1380, 180, 1720, 700], start=190, end=290, fill=(18, 45, 25, 200), width=6)
    pldraw.arc([1400, 260, 1700, 820], start=180, end=280, fill=(22, 55, 30, 220), width=7)
    plant = plant.filter(ImageFilter.GaussianBlur(2))
    base.alpha_composite(plant)

    # Badge overlay: Totem Arquitetônico e Uniformes Oficiais
    tag = Image.new('RGBA', (430, 48), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tag)
    tdraw.rounded_rectangle([0, 0, 430, 48], radius=24, fill=(15, 15, 17, 230), outline=(221, 137, 1, 180), width=1)
    tdraw.text((215, 24), "TOTEM ARQUITETÔNICO & VESTUÁRIO OFICIAL", fill=(221, 137, 1), font=get_font('sans', 12), anchor="mm")
    base.alpha_composite(tag, (60, 60))

    final = base.convert('RGB')
    final.save(os.path.join(ASSETS_DIR, 'osher_totem_fachada.jpg'), quality=96)
    print("osher_totem_fachada.jpg gerada com sucesso (SEM PESSOAS)!")

if __name__ == '__main__':
    render_stationery_luxury()
    render_stationery_pdv()
    render_totem_fachada()
    print("Todas as 3 imagens fotográficas foram geradas com altíssima qualidade!")
