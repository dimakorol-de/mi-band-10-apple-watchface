-- Шаблон циферблата Apple Style для Xiaomi Smart Band 10 (HyperOS / LVGL)
local lvgl = require("lvgl")
local time = require("time")
local fitness = require("fitness")

-- Конфигурация экрана (Разрешение Mi Band 10)
local SCREEN_WIDTH = 192
local SCREEN_HEIGHT = 490

-- Цветовая палитра (Эквивалент Apple Gold из вашего JSON)
local COLOR_PRIMARY = lvgl.color_hex(0xEED1A2)
local COLOR_BG = lvgl.color_hex(0x000000)
local COLOR_WIDGET_BG = lvgl.color_hex(0x1A1A1A)

function init_watchface()
    -- 1. Главный экран и фон
    local screen = lvgl.scr_act()
    lvgl.obj_set_style_bg_color(screen, COLOR_BG, 0)
    
    -- 2. Блок ДАТЫ (EEE, d MMM)
    local date_label = lvgl.label_create(screen)
    lvgl.obj_align(date_label, lvgl.ALIGN_TOP_MID, 0, 45)
    lvgl.obj_set_style_text_color(date_label, COLOR_PRIMARY, 0)
    
    -- Функция обновления даты (вызывается системой)
    function update_date(time_info)
        local months = {"янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"}
        local days = {"Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"}
        -- Форматируем как "Ср, 28 окт"
        local date_str = string.format("%s, %d %s", days[time_info.wday], time_info.mday, months[time_info.month])
        lvgl.label_set_text(date_label, date_str)
    end

    -- 3. Блок ВРЕМЕНИ (Использование ваших картинок assets/Stretched_*.png)
    -- В HyperOS для вывода кастомных цифровых шрифтов используется контейнер картинок
    local time_container = lvgl.obj_create(screen)
    lvgl.obj_set_size(time_container, 180, 100)
    lvgl.obj_align(time_container, lvgl.ALIGN_TOP_MID, 0, 120)
    lvgl.obj_set_style_bg_opa(time_container, lvgl.OPA_TRANSP, 0) -- Прозрачный фон
    
    local img_hour1 = lvgl.img_create(time_container)
    local img_hour2 = lvgl.img_create(time_container)
    local img_min1 = lvgl.img_create(time_container)
    local img_min2 = lvgl.img_create(time_container)
    
    -- Выстраиваем сетку для цифр (x: 96 - центр)
    lvgl.obj_align(img_hour1, lvgl.ALIGN_LEFT_MID, 10, 0)
    lvgl.obj_align(img_hour2, lvgl.ALIGN_LEFT_MID, 50, 0)
    lvgl.obj_align(img_min1, lvgl.ALIGN_LEFT_MID, 95, 0)
    lvgl.obj_align(img_min2, lvgl.ALIGN_LEFT_MID, 135, 0)

    function update_time(time_info)
        -- Получаем отдельные цифры часов и минут
        local h1, h2 = math.floor(time_info.hour / 10), time_info.hour % 10
        local m1, m2 = math.floor(time_info.min / 10), time_info.min % 10
        
        -- Динамически подставляем пути к вашим ассетам
        lvgl.img_set_src(img_hour1, string.format("assets/Stretched_%d.png", h1))
        lvgl.img_set_src(img_hour2, string.format("assets/Stretched_%d.png", h2))
        lvgl.img_set_src(img_min1, string.format("assets/Stretched_%d.png", m1))
        lvgl.img_set_src(img_min2, string.format("assets/Stretched_%d.png", m2))
        
        -- Применяем маску цвета (color_mask из вашего старого JSON)
        lvgl.obj_set_style_img_recolor(img_hour1, COLOR_PRIMARY, 0)
        lvgl.obj_set_style_img_recolor(img_hour2, COLOR_PRIMARY, 0)
        lvgl.obj_set_style_img_recolor(img_min1, COLOR_PRIMARY, 0)
        lvgl.obj_set_style_img_recolor(img_min2, COLOR_PRIMARY, 0)
        lvgl.obj_set_style_img_recolor_opa(img_hour1, lvgl.OPA_COVER, 0)
        lvgl.obj_set_style_img_recolor_opa(img_hour2, lvgl.OPA_COVER, 0)
        lvgl.obj_set_style_img_recolor_opa(img_min1, lvgl.OPA_COVER, 0)
        lvgl.obj_set_style_img_recolor_opa(img_min2, lvgl.OPA_COVER, 0)
    end

    -- 4. Нижний виджет (Слоты расширений / Короткие шаги)
    local steps_widget = lvgl.obj_create(screen)
    lvgl.obj_set_size(steps_widget, 56, 56) -- radius * 2 = 28 * 2 = 56
    lvgl.obj_align(steps_widget, lvgl.ALIGN_TOP_MID, 0, 370)
    lvgl.obj_set_style_radius(steps_widget, 28, 0)
    lvgl.obj_set_style_bg_color(steps_widget, COLOR_WIDGET_BG, 0)
    
    local steps_label = lvgl.label_create(steps_widget)
    lvgl.obj_align(steps_label, lvgl.ALIGN_CENTER, 0, 0)
    lvgl.obj_set_style_text_color(steps_label, COLOR_PRIMARY, 0)

    function update_fitness()
        local step_count = fitness.get_steps()
        lvgl.label_set_text(steps_label, tostring(step_count))
    end

    -- Регистрация колбэков на системные события времени и активности
    time.subscribe_minute(function(time_info)
        update_time(time_info)
        update_date(time_info)
    end)
    
    fitness.subscribe_steps(function()
        update_fitness()
    end)
    
    -- Первичный запуск отрисовки при загрузке экрана
    local current_time = time.get_current()
    update_time(current_time)
    update_date(current_time)
    update_fitness()
end

init_watchface()
