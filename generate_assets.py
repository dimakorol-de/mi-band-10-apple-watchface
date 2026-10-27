import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

# Размеры экрана Mi Band 10
FINAL_W, FINAL_H = 50, 115
assets_dir = "assets"

print("--- Скрипт запущен! ---")

# 1. Принудительно удаляем старые битые картинки, чтобы они не мешались
if os.path.exists(assets_dir):
    for file in os.listdir(assets_dir):
        if file.lower().endswith('.png'):
            os.remove(os.path.join(assets_dir, file))
            print(f"Удалён старый файл: {file}")

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

# Загружаем шрифт (размер 90, чтобы цифра была крупной на холсте-заготовке)
try:
    font = ImageFont.truetype(font_path, 90)
except Exception as e:
    print(f"Критическая ошибка при чтении шрифта: {e}")
    exit(1)

# 3. Генерируем новые, гарантированно заполненные цифры
for i in range(10):
    text = str(i)
    
    # --- Основной набор ---
    temp_img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Пишем цифру в левый верхний угол заготовки, чтобы она точно прорисовалась
    temp_draw.text((10, 10), text, fill=(255, 255, 255, 255), font=font)
    
    # Обрезаем холст строго по контуру прорисованной цифры
    bbox = temp_img.getbbox()
    if bbox is None:
        print(f"Внимание: Не удалось прорисовать цифру {text}! Проверяем параметры.")
        continue
        
    cropped = temp_img.crop(bbox)
    # Силой растягиваем её до нужных нам пропорций 50x115
    stretched = cropped.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    stretched.save(f"assets/Stretched_{i}.png", "PNG")
    print(f"Успешно создана цифра Stretched_{i}.png (Размер: {stretched.size})")

    # --- Набор для режима ожидания (AOD) ---
    temp_aod = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    temp_draw_aod = ImageDraw.Draw(temp_aod)
    # Рисуем контур толщиной в 4 пикселя
    temp_draw_aod.text((10, 10), text, fill=(0, 0, 0, 0), 
                       stroke_width=4, stroke_fill=(255, 255, 255, 255), font=font)
    
    bbox_aod = temp_aod.getbbox()
    if bbox_aod:
        cropped_aod = temp_aod.crop(bbox_aod)
        stretched_aod = cropped_aod.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        stretched_aod.save(f"assets/AOD_{i}.png", "PNG")
        print(f"Успешно создана AOD цифра AOD_{i}.png")

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
