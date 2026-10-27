import os
import zipfile
import json
from PIL import Image, ImageDraw, ImageFont

# Размеры экрана Mi Band 10
FINAL_W, FINAL_H = 50, 115
assets_dir = "assets"

print("--- Скрипт запущен! ---")

# 1. Очищаем старые картинки в рабочей папке сервера
if os.path.exists(assets_dir):
    for file in os.listdir(assets_dir):
        if file.lower().endswith('.png'):
            os.remove(os.path.join(assets_dir, file))
else:
    os.makedirs(assets_dir)

# 2. Ищем загруженный шрифт
font_path = None
if os.path.exists(assets_dir):
    for file in os.listdir(assets_dir):
        if file.lower().endswith(('.ttf', '.otf')):
            font_path = os.path.join(assets_dir, file)
            break

font = None
if font_path:
    try:
        font = ImageFont.truetype(font_path, 90)
    except Exception:
        pass

if font is None:
    font = ImageFont.load_default()

# 3. Генерируем 10 идеальных вытянутых цифр
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
    stretched.save(f"assets/Stretched_{i}.png", "PNG")

print("Картинки успешно сгенерированы!")

# 4. Генерируем абсолютно ЧИСТЫЙ watchface.json программно на сервере
wf_data = {
  "sdk_version": "3.0.0",
  "device_id": "xiaomi.smartband.10",
  "device_type": "smart_band",
  "meta": {
    "name": "Apple Style Fixed",
    "version": "1.0.5",
    "author": "Custom",
    "description": "Apple Watch Stretched Style with Fixed Complication"
  },
  "settings": {
    "fps": 30,
    "hardware_acceleration": True,
    "cache_resources": True
  },
  "theme": {
    "default_color_index": 0,
    "color_palettes": [
      { "name": "Apple Umber", "primary": "#D4A373", "secondary": "#7A5C43" },
      { "name": "Pure White", "primary": "#FFFFFF", "secondary": "#888888" }
    ]
  },
  "views": {
    "main": {
      "background": { "color": "#000000" },
      "components": [
        {
          "type": "date",
          "format": "EEE, d MMM",
          "locale": "ru_RU",
          "x": 96, "y": 45,
          "align": "center",
          "font": "system_16",
          "color": "@theme.primary"
        },
        {
          "type": "time_images",
          "x": 96, "y": 120,
          "align": "center",
          "spacing": -1,
          "resource_prefix": "assets/Stretched_",
          "color_mask": "@theme.primary"
        },
        {
          "type": "complication_slot",
          "id": "slot_bottom",
          "x": 96, "y": 370,
          "align": "center",
          "radius": 28,
          "supported_types": ["steps", "heart_rate", "sleep", "flashlight"],
          "default_type": "steps",
          "style": {
            "icon_color": "@theme.primary",
            "progress_color": "@theme.primary",
            "bg_color": "#1A1A1A"
          }
        }
      ]
    },
    "aod": {
      "enabled": True,
      "background": { "color": "#000000" },
      "components": [
        {
          "type": "time_images",
          "x": 96, "y": 120,
          "align": "center",
          "spacing": -1,
          "resource_prefix": "assets/Stretched_",
          "color_mask": "@theme.secondary"
        }
      ]
    }
  }
}

# Записываем чистую конфигурацию поверх старой в рабочей среде сборщика
with open("watchface.json", "w", encoding="utf-8") as f:
    json.dump(wf_data, f, indent=2, ensure_ascii=False)

print("Файл watchface.json успешно перезаписан на чистый вариант!")

# 5. Собираем финальный .bin с правильным несжатым методом (ZIP_STORED) для мода
watchface_bin_path = "AppleStyleFixed.bin"
with zipfile.ZipFile(watchface_bin_path, 'w', zipfile.ZIP_STORED) as zipf:
    zipf.write("watchface.json", "watchface.json")
    for i in range(10):
        img_name = f"Stretched_{i}.png"
        local_path = os.path.join(assets_dir, img_name)
        if os.path.exists(local_path):
            zipf.write(local_path, f"assets/{img_name}")

print(f"Сборка полностью завершена: {watchface_bin_path}")
