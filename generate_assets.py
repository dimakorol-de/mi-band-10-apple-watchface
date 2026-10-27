import os
from PIL import Image, ImageDraw, ImageFont

# Настройки пропорций под экран Mi Band 10
W, H = 50, 115
font_path = "assets/SF-Pro-Rounded-Regular.ttf"
font_size = 110

if not os.path.exists(font_path):
    print(f"Ошибка: Файл шрифта не найден по пути {font_path}")
    exit(1)

font = ImageFont.truetype(font_path, font_size)

for i in range(10):
    # 1. Генерация основных вытянутых цифр (Stretched)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    text = str(i)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    # Рисуем цифру строго по центру холста
    draw.text(((W - tw) // 2, (H - th) // 2 - 10), text, fill=(255, 255, 255, 255), font=font)
    img.save(f"assets/Stretched_{i}.png", "PNG")

    # 2. Генерация контурных цифр для AOD (Always-On Display)
    img_aod = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_aod = ImageDraw.Draw(img_aod)
    draw_aod.text(((W - tw) // 2, (H - th) // 2 - 10), text, fill=(0, 0, 0, 0), 
                  stroke_width=2, stroke_fill=(255, 255, 255, 255), font=font)
    img_aod.save(f"assets/AOD_{i}.png", "PNG")

print("Все 20 идеальных картинок созданы программно!")
