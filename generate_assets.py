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

# Пробуем загрузить шрифт Apple, если не выйдет — берем системный дефолт
font = None
if font_path:
    try:
        font = ImageFont.truetype(font_path, 90)
    except Exception as e:
        print(f"Предупреждение при загрузке шрифта: {e}. Переключаемся на резерв.")

if font is None:
    font = ImageFont.load_default()

# 3. Генерируем 20 картинок
for i in range(10):
    text = str(i)
    
    # --- Основной набор (Stretched) ---
    temp_img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Пробуем нарисовать с разным позиционированием
    try:
        temp_draw.text((100, 100), text, fill=(255, 255, 255, 255), font=font, anchor="mm")
    except Exception:
        temp_draw.text((10, 10), text, fill=(255, 255, 255, 255), font=font)
    
    bbox = temp_img.getbbox()
    if bbox is None:
        # Резервный вариант на случай полной пустоты — рисуем цифру гарантированным методом
        temp_draw.text((30, 30), text, fill=(255, 255, 255, 255))
        bbox = temp_img.getbbox()
        
    cropped = temp_img.crop(bbox)
    stretched = cropped.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    stretched.save(f"assets/Stretched_{i}.png", "PNG")
    print(f"Успешно создана цифра Stretched_{i}.png (Размер: {stretched.size})")

    # --- Набор для режима ожидания (AOD) ---
    temp_aod = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    temp_draw_aod = ImageDraw.Draw(temp_aod)
    
    try:
        temp_draw_aod.text((100, 100), text, fill=(0, 0, 0, 0), stroke_width=4, stroke_fill=(255, 255, 255, 255), font=font, anchor="mm")
    except Exception:
        temp_draw_aod.text((10, 10), text, fill=(255, 255, 255, 255), font=font)
        
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
