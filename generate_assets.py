import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

# 1. Настройки отрисовки цифр
W, H = 50, 115
font_path = "assets/SF-Pro-Rounded-Regular.ttf"
font_size = 110

if not os.path.exists(font_path):
    print(f"Ошибка: Шрифт не найден по пути {font_path}")
    exit(1)

font = ImageFont.truetype(font_path, font_size)

# Генерируем 20 картинок
for i in range(10):
    # Основные растянутые цифры
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    text = str(i)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((W - tw) // 2, (H - th) // 2 - 10), text, fill=(255, 255, 255, 255), font=font)
    img.save(f"assets/Stretched_{i}.png", "PNG")

    # Контурные цифры для AOD
    img_aod = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_aod = ImageDraw.Draw(img_aod)
    draw_aod.text(((W - tw) // 2, (H - th) // 2 - 10), text, fill=(0, 0, 0, 0), 
                  stroke_width=2, stroke_fill=(255, 255, 255, 255), font=font)
    img_aod.save(f"assets/AOD_{i}.png", "PNG")

print("Графика сгенерирована!")

# 2. Создаем чистый правильный BIN-архив средствами Python
watchface_bin_path = "AppleStyleFixed.bin"
with zipfile.ZipFile(watchface_bin_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Упаковываем JSON конфигурации
    if os.path.exists("watchface.json"):
        zipf.write("watchface.json")
    # Упаковываем все картинки из assets
    for root, dirs, files in os.walk("assets"):
        for file in files:
            if file.endswith(".png"):
                zipf.write(os.path.join(root, file))

print(f"Циферблат успешно упакован в чистый файл: {watchface_bin_path}")
