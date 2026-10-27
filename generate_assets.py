import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

# Конечные размеры для Mi Band 10
FINAL_W, FINAL_H = 50, 115
assets_dir = "assets"

# Умный поиск ЛЮБОГО файла шрифта в папке assets
font_path = None
if os.path.exists(assets_dir):
    for file in os.listdir(assets_dir):
        if file.lower().endswith(('.ttf', '.otf')):
            font_path = os.path.join(assets_dir, file)
            print(f"Ура! Найдён шрифт: {font_path}")
            break

if not font_path:
    print("Ошибка: В папке assets нет ни одного файла шрифта (.ttf или .otf)!")
    exit(1)

# Загружаем найденный шрифт
font = ImageFont.truetype(font_path, 70)

for i in range(10):
    text = str(i)
    
    # --- 1. Основные растянутые цифры ---
    temp_img = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    temp_draw.text(((150 - tw) // 2, (150 - th) // 2), text, fill=(255, 255, 255, 255), font=font)
    
    cropped = temp_img.crop(temp_img.getbbox())
    stretched = cropped.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    stretched.save(f"assets/Stretched_{i}.png", "PNG")

    # --- 2. Контурные цифры для AOD ---
    temp_aod = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
    temp_draw_aod = ImageDraw.Draw(temp_aod)
    
    temp_draw_aod.text(((150 - tw) // 2, (150 - th) // 2), text, fill=(0, 0, 0, 0), 
                       stroke_width=3, stroke_fill=(255, 255, 255, 255), font=font)
    
    cropped_aod = temp_aod.crop(temp_aod.getbbox())
    stretched_aod = cropped_aod.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    stretched_aod.save(f"assets/AOD_{i}.png", "PNG")

print("Все файлы успешно сгенерированы!")

# 3. Упаковка в BIN-архив
watchface_bin_path = "AppleStyleFixed.bin"
with zipfile.ZipFile(watchface_bin_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    if os.path.exists("watchface.json"):
        zipf.write("watchface.json")
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".png"):
                zipf.write(os.path.join(root, file))
