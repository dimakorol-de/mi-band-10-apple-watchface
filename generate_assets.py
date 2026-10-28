import os
import zipfile
import json

# Настройки папок и финального имени для HyperOS
assets_dir = "assets"
watchface_face_path = "AppleStyleFixed.face"

print("--- Скрипт чистой ручной сборки в .FACE запущен! ---")

# Проверяем файлы
if not os.path.exists(assets_dir) or not os.listdir(assets_dir):
    print("Ошибка: Папка assets пуста!")
    exit(1)

if not os.path.exists("watchface.json"):
    print("Ошибка: Файл watchface.json не найден!")
    exit(1)

# Собираем монолитный .face архив БЕЗ скрытых системных тегов Linux (UT)
with zipfile.ZipFile(watchface_face_path, 'w', zipfile.ZIP_STORED) as zipf:
    # Принудительно очищаем системные метаданные для JSON
    json_info = zipfile.ZipInfo("watchface.json")
    json_info.create_system = 0  # Вырезает Unix-атрибуты
    with open("watchface.json", "r", encoding="utf-8") as f:
        zipf.writestr(json_info, f.read())
    
    # Очищаем метаданные для каждой твоей картинки от 0 до 9
    for i in range(10):
        img_name = f"Stretched_{i}.png"
        local_path = os.path.join(assets_dir, img_name)
        if os.path.exists(local_path):
            img_info = zipfile.ZipInfo(f"assets/{img_name}")
            img_info.create_system = 0  # Вырезает Unix-атрибуты
            with open(local_path, "rb") as f:
                zipf.writestr(img_info, f.read())
            print(f"В .face пакет добавлен файл: assets/{img_name}")

print(f"Циферблат успешно скомпилирован в чистый фабричный формат: {watchface_face_path}")
