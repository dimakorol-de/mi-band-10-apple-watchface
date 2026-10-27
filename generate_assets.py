import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

# Размеры экрана Mi Band 10
FINAL_W, FINAL_H = 50, 115
assets_dir = "assets"

print("--- Скрипт запущен! ---")

# 1. Удаляем старые png, если они есть
if os.path.exists(assets_dir):
    for file in os.listdir(assets_dir):
        if file.lower().endswith('.png'):
            os.remove(os.path.join(assets_dir, file))

# 2. Ищем загруженный шрифт
font_path = None
if os.path.exists(assets_dir):
    for file in os.listdir(assets_dir):
        if file.lower().endswith(('.ttf', '.otf')):
            font_path = os.path.join(assets_dir, file)
            print(f"Найдена основа! Используем шрифт: {font_path}")
            break

if not font_path:
    print("КРИТИЧЕСКАЯ ОШИБКА: Шрифт не найден в папке assets!")
    exit(1)

# Загружаем шрифт (размер 90)
font = ImageFont.truetype(font_path, 90)

# 3. Генерируем новые цифры с принудительным центрированием anchor="mm"
for i in range(10):
    text = str(i)
    
    # --- Основной набор (Stretched) ---
    temp_img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # anchor="mm" ставит математический центр самой цифры в координаты (100, 100) холста
    temp_draw.text((100, 100), text, fill=(255, 255, 255, 255), font=font, anchor="mm")
    
    bbox = temp_img.getbbox()
    if bbox is None:
        print(f"Внимание: Не удалось прорисовать цифру {text}!")
        continue
        
    cropped = temp_img.crop(bbox)
    stretched = cropped.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    stretched.save(f"assets/Stretched_{i}.png", "PNG")
    print(f"Успешно создана цифра Stretched_{i}.png (Размер: {stretched.size})")

    # --- Набор для режима ожидания (AOD) ---
    temp_aod = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    temp_draw_aod = ImageDraw.Draw(temp_aod)
    
    # Рисуем только контур, тоже центрируя по "mm"
    temp_draw_aod.text((100, 100), text, fill=(0, 0, 0, 0), 
                       stroke_width=4, stroke_fill=(255, 255, 255, 255), font=font, anchor="mm")
    
    bbox_aod = temp_aod.getbbox()
    if bbox_aod:
        cropped_aod = temp_aod.crop(bbox_aod)
        stretched_aod = cropped_aod.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        stretched_aod.save(f"assets/AOD_{i}.png", "PNG")

print("--- Все 20 картинок созданы! Начинаем упаковку. ---")

# 4. Собираем финальный .bin
watchface_bin_path = "AppleStyleFixed.bin"
with zipfile.ZipFile(watchface_bin_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    if os.path.exists("watchface.json"):
        zipf.write("watchface.json")
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".png"):
                zipf.write(os.path.join(root, file))

print(f"Готово! Сборка циферблата завершена: {watchface_bin_path}")
