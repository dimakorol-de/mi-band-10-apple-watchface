import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

# Конечные размеры для Mi Band 10
FINAL_W, FINAL_H = 50, 115
font_path = "assets/SF-Pro-Rounded-Regular.ttf"

if not os.path.exists(font_path):
    print(f"Ошибка: Шрифт не найден по пути {font_path}")
    exit(1)

# Берем чуть меньший шрифт, чтобы цифра гарантированно прорисовалась на холсте-заготовке
font = ImageFont.truetype(font_path, 70)

for i in range(10):
    text = str(i)
    
    # --- 1. Основные растянутые цифры ---
    # Создаем квадратную заготовку, где цифра точно поместится
    temp_img = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Центрируем текст на заготовке
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    temp_draw.text(((150 - tw) // 2, (150 - th) // 2), text, fill=(255, 255, 255, 255), font=font)
    
    # Обрезаем холст строго по границам цифры
    cropped = temp_img.crop(temp_img.getbbox())
    
    # Принудительно растягиваем цифру до размеров экрана Mi Band 10 (50x115)
    stretched = cropped.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    stretched.save(f"assets/Stretched_{i}.png", "PNG")

    # --- 2. Контурные цифры для AOD ---
    temp_aod = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
    temp_draw_aod = ImageDraw.Draw(temp_aod)
    
    # Рисуем только контур в 3 пикселя (после уменьшения он станет аккуратным в 1-2 пикселя)
    temp_draw_aod.text(((150 - tw) // 2, (150 - th) // 2), text, fill=(0, 0, 0, 0), 
                       stroke_width=3, stroke_fill=(255, 255, 255, 255), font=font)
    
    cropped_aod = temp_aod.crop(temp_aod.getbbox())
    stretched_aod = cropped_aod.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    stretched_aod.save(f"assets/AOD_{i}.png", "PNG")

print("Все файлы успешно сгенерированы и принудительно растянуты!")

# 3. Упаковка в BIN-архив
watchface_bin_path = "AppleStyleFixed.bin"
with zipfile.ZipFile(watchface_bin_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    if os.path.exists("watchface.json"):
        zipf.write("watchface.json")
    for root, dirs, files in os.walk("assets"):
        for file in files:
            if file.endswith(".png"):
                zipf.write(os.path.join(root, file))
