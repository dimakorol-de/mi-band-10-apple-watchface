import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

# Размеры экрана Mi Band 10
FINAL_W, FINAL_H = 50, 115
assets_dir = "assets"

print("--- Скрипт запущен! ---")

# 1. Очищаем папку от старых файлов
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

font = None
if font_path:
    try:
        font = ImageFont.truetype(font_path, 90)
    except Exception as e:
        print(f"Предупреждение при загрузке шрифта: {e}")

if font is None:
    font = ImageFont.load_default()

# 3. Генерируем 10 основных вытянутых цифр
for i in range(10):
    text = str(i)
    temp_img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    try:
        temp_draw.text((100, 100), text, fill=(255, 255, 255, 255), font=font, anchor="mm")
    except Exception:
        temp_draw.text((10, 10), text, fill=(255, 255, 255, 255), font=font)
    
    bbox = temp_img.getbbox()
    if bbox is None:
        temp_draw.text((30, 30), text, fill=(255, 255, 255, 255))
        bbox = temp_img.getbbox()
        
    cropped = temp_img.crop(bbox)
    stretched = cropped.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    
    # Сохраняем файлы напрямую
    stretched.save(f"assets/Stretched_{i}.png", "PNG")
    print(f"Успешно создана цифра Stretched_{i}.png")

print("--- Все картинки созданы! Начинаем правильную HyperOS-упаковку. ---")

# 4. Собираем финальный .bin с правильной внутренней структурой каталогов
watchface_bin_path = "AppleStyleFixed.bin"
with zipfile.ZipFile(watchface_bin_path, 'w', zipfile.ZIP_STORED) as zipf:
    # Важно: Записываем watchface.json в самый корень архива
    if os.path.exists("watchface.json"):
        zipf.write("watchface.json", "watchface.json")
    
    # Записываем картинки строго по путям без создания лишних дублирующих подпапок
    for i in range(10):
        img_name = f"Stretched_{i}.png"
        local_path = os.path.join(assets_dir, img_name)
        if os.path.exists(local_path):
            # Внутри bin-файла путь должен быть строго: assets/Stretched_X.png
            zipf.write(local_path, f"assets/{img_name}")

print(f"Готово! Сборка циферблата завершена: {watchface_bin_path}")
