from ursina import *
import math
import random
import json
import os

app = Ursina()

window.title = "City Simulator 3D"
window.borderless = False
window.fullscreen = False
window.color = color.rgb(135, 190, 235)

# ============================================================
# НАСТРОЙКИ
# ============================================================

GRID = 32
CELL = 2

money = 75000
population = 0
happiness = 70
pollution = 0
electricity = 100
water = 100

tax_rate = 10
month = 1

income_last = 0
expenses_last = 0

paused = False

buildings = []

selected = "house"

income_timer = 0


# ============================================================
# ЗДАНИЯ
# ============================================================

BUILDINGS = {

    "house": {
        "name": "Жилой дом",
        "price": 3000,
        "population": 25,
        "income": 0,
        "expense": 30,
        "power": 2,
        "pollution": 0,
        "happiness": 1,
        "color": color.rgb(220, 185, 145),
        "scale": (1.7, 2.5, 1.7)
    },

    "shop": {
        "name": "Магазин",
        "price": 6000,
        "population": 0,
        "income": 180,
        "expense": 40,
        "power": 3,
        "pollution": 1,
        "happiness": 2,
        "color": color.rgb(80, 150, 230),
        "scale": (1.8, 2.2, 1.8)
    },

    "factory": {
        "name": "Завод",
        "price": 12000,
        "population": 0,
        "income": 500,
        "expense": 100,
        "power": 8,
        "pollution": 12,
        "happiness": -4,
        "color": color.rgb(115, 115, 120),
        "scale": (2.2, 3.5, 2.2)
    },

    "school": {
        "name": "Школа",
        "price": 10000,
        "population": 0,
        "income": 0,
        "expense": 150,
        "power": 4,
        "pollution": 0,
        "happiness": 6,
        "color": color.rgb(235, 205, 80),
        "scale": (3, 1.8, 2.5)
    },

    "hospital": {
        "name": "Больница",
        "price": 15000,
        "population": 0,
        "income": 0,
        "expense": 220,
        "power": 6,
        "pollution": 0,
        "happiness": 8,
        "color": color.rgb(235, 235, 235),
        "scale": (2.5, 2.2, 2.5)
    },

    "police": {
        "name": "Полиция",
        "price": 9000,
        "population": 0,
        "income": 0,
        "expense": 130,
        "power": 3,
        "pollution": 0,
        "happiness": 5,
        "color": color.rgb(70, 90, 170),
        "scale": (2, 1.6, 2)
    },

    "park": {
        "name": "Парк",
        "price": 2500,
        "population": 0,
        "income": 0,
        "expense": 15,
        "power": 0,
        "pollution": -6,
        "happiness": 5,
        "color": color.rgb(70, 180, 80),
        "scale": (2, 0.25, 2)
    },

    "power": {
        "name": "Электростанция",
        "price": 20000,
        "population": 0,
        "income": 0,
        "expense": 250,
        "power": -40,
        "pollution": 15,
        "happiness": -2,
        "color": color.rgb(190, 100, 100),
        "scale": (2.5, 4, 2.5)
    },

    "water": {
        "name": "Водоканал",
        "price": 16000,
        "population": 0,
        "income": 0,
        "expense": 180,
        "power": 5,
        "pollution": 0,
        "happiness": 4,
        "color": color.rgb(80, 180, 220),
        "scale": (2.5, 2, 2.5)
    },

  
# ============================================================
# ЗДАНИЯ
# ============================================================

BUILDINGS = {

    "house": {
        "name": "Жилой дом",
        "price": 3000,
        "population": 25,
        "income": 0,
        "expense": 30,
        "power": 2,
        "pollution": 0,
        "happiness": 1,
        "color": color.rgb(220, 185, 145),
        "scale": (1.7, 2.5, 1.7)
    },

    "shop": {
        "name": "Магазин",
        "price": 6000,
        "population": 0,
        "income": 180,
        "expense": 40,
        "power": 3,
        "pollution": 1,
        "happiness": 2,
        "color": color.rgb(80, 150, 230),
        "scale": (1.8, 2.2, 1.8)
    },

    "factory": {
        "name": "Завод",
        "price": 12000,
        "population": 0,
        "income": 500,
        "expense": 100,
        "power": 8,
        "pollution": 12,
        "happiness": -4,
        "color": color.rgb(115, 115, 120),
        "scale": (2.2, 3.5, 2.2)
    },

    "school": {
        "name": "Школа",
        "price": 10000,
        "population": 0,
        "income": 0,
        "expense": 150,
        "power": 4,
        "pollution": 0,
        "happiness": 6,
        "color": color.rgb(235, 205, 80),
        "scale": (3, 1.8, 2.5)
    },

    "hospital": {
        "name": "Больница",
        "price": 15000,
        "population": 0,
        "income": 0,
        "expense": 220,
        "power": 6,
        "pollution": 0,
        "happiness": 8,
        "color": color.rgb(235, 235, 235),
        "scale": (2.5, 2.2, 2.5)
    },

    "police": {
        "name": "Полиция",
        "price": 9000,
        "population": 0,
        "income": 0,
        "expense": 130,
        "power": 3,
        "pollution": 0,
        "happiness": 5,
        "color": color.rgb(70, 90, 170),
        "scale": (2, 1.6, 2)
    },

    "park": {
        "name": "Парк",
        "price": 2500,
        "population": 0,
        "income": 0,
        "expense": 15,
        "power": 0,
        "pollution": -6,
        "happiness": 5,
        "color": color.rgb(70, 180, 80),
        "scale": (2, 0.25, 2)
    },

    "power": {
        "name": "Электростанция",
        "price": 20000,
        "population": 0,
        "income": 0,
        "expense": 250,
        "power": -40,
        "pollution": 15,
        "happiness": -2,
        "color": color.rgb(190, 100, 100),
        "scale": (2.5, 4, 2.5)
    },

    "water": {
        "name": "Водоканал",
        "price": 16000,
        "population": 0,
        "income": 0,
        "expense": 180,
        "power": 5,
        "pollution": 0,
        "happiness": 4,
        "color": color.rgb(80, 180, 220),
        "scale": (2.5, 2, 2.5)
    },

    "road": {
        "name": "Дорога",
        "price": 500,
        "population": 0,
        "income": 0,
        "expense": 10,
        "power": 0,
        "pollution": 1,
        "happiness": 0,
        "color": color.rgb(65, 65, 65),
        "scale": (2, 0.15, 2)
    }
}



# ============================================================
# ЗЕМЛЯ
# ============================================================

ground = Entity(
    model="cube",
    scale=(GRID * CELL, 0.2, GRID * CELL),
    position=(0, -0.1, 0),
    color=color.rgb(75, 155, 75),
    collider="box"
)


# ============================================================
# СЕТКА
# ============================================================

for x in range(-GRID // 2, GRID // 2 + 1):

    Entity(
        model="cube",
        scale=(0.01, 0.01, GRID * CELL),
        position=(x * CELL, 0.01, 0),
        color=color.rgba(255, 255, 255, 35)
    )


for z in range(-GRID // 2, GRID // 2 + 1):

    Entity(
        model="cube",
        scale=(GRID * CELL, 0.01, 0.01),
        position=(0, 0.01, z * CELL),
        color=color.rgba(255, 255, 255, 35)
    )


# ============================================================
# UI
# ============================================================

stats = Text(
    position=(-0.86, 0.46),
    scale=0.95
)

selected_text = Text(
    position=(-0.86, 0.16),
    scale=0.8
)

message = Text(
    position=(-0.86, -0.38),
    scale=0.8
)

controls = Text(
    text=(
        "СТРЕЛКИ — камера\n"
        "ЛКМ — строить\n"
        "ПКМ — удалить\n"
        "1 Дом\n"
        "2 Магазин\n"
        "3 Завод\n"
        "4 Школа\n"
        "5 Больница\n"
        "6 Полиция\n"
        "7 Парк\n"
        "8 Электростанция\n"
        "9 Водоканал\n"
        "0 Дорога\n"
        "SPACE — следующий месяц\n"
        "P — пауза\n"
        "F5 — сохранить\n"
        "F9 — загрузить"
    ),
    position=(0.55, 0.42),
    scale=0.72
)


# ============================================================
# ПРЕДПРОСМОТР
# ============================================================

preview = Entity(
    model="cube",
    color=color.rgba(80, 255, 80, 100),
    enabled=True
)


# ============================================================
# UI ОБНОВЛЕНИЕ
# ============================================================

def update_ui():

    stats.text = (
        "🏙 ГОРОД\n"
        f"Месяц: {month}\n"
        f"💰 Деньги: ${money}\n"
        f"👥 Население: {population}\n"
        f"😊 Счастье: {int(happiness)}%\n"
        f"☢ Загрязнение: {int(pollution)}%\n"
        f"⚡ Электричество: {int(electricity)}%\n"
        f"💧 Вода: {int(water)}%\n"
        f"💵 Налог: {tax_rate}%\n"
        f"📈 Доход: ${income_last}\n"
        f"📉 Расходы: ${expenses_last}"
    )

    data = BUILDINGS[selected]

    selected_text.text = (
        f"Выбрано: {data['name']}\n"
        f"Цена: ${data['price']}"
    )


update_ui()


# ============================================================
# ПОЗИЦИЯ НА СЕТКЕ
# ============================================================

def snap_position(pos):

    x = round(pos.x / CELL) * CELL
    z = round(pos.z / CELL) * CELL

    return Vec3(x, 0, z)


def occupied(pos):

    for obj in buildings:

        if (
            abs(obj.x - pos.x) < 0.5
            and abs(obj.z - pos.z) < 0.5
        ):
            return True

    return False


# ============================================================
# ПОСТРОЙКА
# ============================================================

def build():

    global money
    global population

    if mouse.world_point is None:
        return

    pos = snap_position(mouse.world_point)

    data = BUILDINGS[selected]

    if occupied(pos):

        show_message(
            "Здесь уже что-то построено."
        )

        return

    if money < data["price"]:

        show_message(
            "Недостаточно денег!"
        )

        return

    money -= data["price"]

    obj = Entity(
        model="cube",
        color=data["color"],
        scale=data["scale"],
        position=(
            pos.x,
            data["scale"][1] / 2,
            pos.z
        ),
        collider="box"
    )

    obj.building_type = selected

    buildings.append(obj)

    population += data["population"]

    show_message(
        data["name"] + " построено!"
    )

    update_ui()


# ============================================================
# УДАЛЕНИЕ
# ============================================================

def delete_building():

    global money
    global population

    obj = mouse.hovered_entity

    if obj is None:
        return

    if obj not in buildings:
        return

    data = BUILDINGS[obj.building_type]

    refund = data["price"] // 2

    money += refund

    population -= data["population"]

    buildings.remove(obj)

    destroy(obj)

    show_message(
        f"Здание продано. Возвращено ${refund}"
    )

    update_ui()


# ============================================================
# СООБЩЕНИЯ
# ============================================================

message_timer = 0


def show_message(text):

    global message_timer

    message.text = text
    message_timer = 3


# ============================================================
# ЭКОНОМИКА
# ============================================================

def next_month():

    global money
    global month
    global income_last
    global expenses_last
    global happiness
    global pollution
    global electricity
    global water
    global population

    month += 1

    income = 0
    expenses = 0

    total_power = 0
    total_water = 0

    houses = 0
    shops = 0

    for obj in buildings:

        data = BUILDINGS[obj.building_type]

        expenses += data["expense"]

        total_power += data["power"]

        total_water += data["power"] * 0.5

        income += data["income"]

        if obj.building_type == "house":
            houses += 1

        if obj.building_type == "shop":
            shops += 1

    # ========================================================
    # НАЛОГИ
    # ========================================================

    tax_income = int(
        population * tax_rate * 0.8
    )

    income += tax_income

    # ========================================================
    # ЭЛЕКТРИЧЕСТВО
    # ========================================================

    required_power = max(
        1,
        population // 10
    )

    if total_power < required_power:

        electricity = max(
            10,
            electricity - 15
        )

        happiness -= 5

        show_message(
            "⚡ Нехватка электричества!"
        )

    else:

        electricity = min(
            100,
            electricity + 5
        )

    # ========================================================
    # ВОДА
    # ========================================================

    required_water = max(
        1,
        population // 8
    )

    if total_water < required_water:

        water = max(
            10,
            water - 10
        )

        happiness -= 4

    else:

        water = min(
            100,
            water + 4
        )

    # ========================================================
    # ЗАГРЯЗНЕНИЕ
    # ========================================================

    pollution_change = 0

    for obj in buildings:

        data = BUILDINGS[obj.building_type]

        pollution_change += data["pollution"]

    pollution += pollution_change * 0.15

    pollution -= (
        sum(
            1
            for obj in buildings
            if obj.building_type == "park"
        ) * 0.5
    )

    pollution = max(
        0,
        min(100, pollution)
    )

    # ========================================================
    # СЧАСТЬЕ
    # ========================================================

    happiness += (
        sum(
            BUILDINGS[obj.building_type]["happiness"]
            for obj in buildings
        ) * 0.1
    )

    happiness -= pollution * 0.04

    if electricity < 40:
        happiness -= 3

    if water < 40:
        happiness -= 3

    happiness = max(
        0,
        min(100, happiness)
    )

    # ========================================================
    # РОСТ НАСЕЛЕНИЯ
    # ========================================================

    if houses > 0 and happiness >= 60:

        growth = max(
            1,
            int(
                houses *
                random.uniform(
                    0.5,
                    2
                )
            )
        )

        population += growth

    elif happiness < 30:

        loss = max(
            1,
            int(population * 0.03)
        )

        population = max(
            0,
            population - loss
        )

    # ========================================================
    # БОНУС ЗА МАГАЗИНЫ
    # ========================================================

    if population > 100:

        income += shops * 50

    # ========================================================
    # ИТОГ
    # ========================================================

    money += income
    money -= expenses

    income_last = income
    expenses_last = expenses

    if money < 0:

        show_message(
            "⚠ Город обанкротился!"
        )

    else:

        show_message(
            f"Месяц {month}: +${income} / -${expenses}"
        )

    update_ui()


# ============================================================
# СОХРАНЕНИЕ
# ============================================================

SAVE_FILE = "city_save.json"


def save_game():

    data = {
        "money": money,
        "population": population,
        "happiness": happiness,
        "pollution": pollution,
        "electricity": electricity,
        "water": water,
        "tax_rate": tax_rate,
        "month": month,

        "buildings": [
            {
                "type": obj.building_type,
                "x": obj.x,
                "z": obj.z
            }
            for obj in buildings
        ]
    }

    with open(
        SAVE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

    show_message(
        "💾 Город сохранён!"
    )


# ============================================================
# ЗАГРУЗКА
# ============================================================

def clear_city():

    global population

    for obj in buildings:

        destroy(obj)

    buildings.clear()

    population = 0


def load_game():

    global money
    global population
    global happiness
    global pollution
    global electricity
    global water
    global tax_rate
    global month

    if not os.path.exists(SAVE_FILE):

        show_message(
            "Сохранение не найдено."
        )

        return

    with open(
        SAVE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    clear_city()

    money = data["money"]
    population = data["population"]
    happiness = data["happiness"]
    pollution = data["pollution"]
    electricity = data["electricity"]
    water = data["water"]
    tax_rate = data["tax_rate"]
    month = data["month"]

    for item in data["buildings"]:

        building_type = item["type"]

        info = BUILDINGS[building_type]

        obj = Entity(
            model="cube",
            color=info["color"],
            scale=info["scale"],
            position=(
                item["x"],
                info["scale"][1] / 2,
                item["z"]
            ),
            collider="box"
        )

        obj.building_type = building_type

        buildings.append(obj)

    update_ui()

    show_message(
        "📂 Город загружен!"
    )


# ============================================================
# ВЫБОР ЗДАНИЯ
# ============================================================

def select(name):

    global selected

    selected = name

    info = BUILDINGS[name]

    preview.scale = info["scale"]

    update_ui()


# ============================================================
# КЛАВИАТУРА
# ============================================================

def input(key):

    global paused

    if key == "1":
        select("house")

    elif key == "2":
        select("shop")

    elif key == "3":
        select("factory")

    elif key == "4":
        select("school")

    elif key == "5":
        select("hospital")

    elif key == "6":
        select("police")

    elif key == "7":
        select("park")

    elif key == "8":
        select("power")

    elif key == "9":
        select("water")

    elif key == "0":
        select("road")

    elif key == "left mouse down":

        if not paused:
            build()

    elif key == "right mouse down":

        if not paused:
            delete_building()

    elif key == "space":

        if not paused:
            next_month()

    elif key == "p":

        paused = not paused

        if paused:
            show_message("⏸ Игра на паузе")
        else:
            show_message("▶ Игра продолжается")

    elif key == "f5":

        save_game()

    elif key == "f9":

        load_game()


# ============================================================
# КАМЕРА
# ============================================================

camera.position = (
    0,
    28,
    -28
)

camera.rotation_x = 55

camera_speed = 18


# ============================================================
# ОБНОВЛЕНИЕ
# ============================================================

def update():

    global message_timer

    if not paused:

        if held_keys["left arrow"]:
            camera.x -= camera_speed * time.dt

        if held_keys["right arrow"]:
            camera.x += camera_speed * time.dt

        if held_keys["up arrow"]:
            camera.z += camera_speed * time.dt

        if held_keys["down arrow"]:
            camera.z -= camera_speed * time.dt

    # ========================================================
    # ПРЕДПРОСМОТР
    # ========================================================

    if mouse.world_point is not None:

        pos = snap_position(
            mouse.world_point
        )

        info = BUILDINGS[selected]

        preview.position = (
            pos.x,
            info["scale"][1] / 2,
            pos.z
        )

        if occupied(pos):

            preview.color = color.rgba(
                255,
                60,
                60,
                100
            )

        elif money < info["price"]:

            preview.color = color.rgba(
                255,
                60,
                60,
                100
            )

        else:

            preview.color = color.rgba(
                70,
                255,
                100,
                100
            )

    # ========================================================
    # СООБЩЕНИЯ
    # ========================================================

    if message_timer > 0:

        message_timer -= time.dt

        if message_timer <= 0:

            message.text = ""


# ============================================================
# СТАРТОВЫЕ ДОРОГИ
# ============================================================

for x in range(-8, 9, 2):

    info = BUILDINGS["road"]

    obj = Entity(
        model="cube",
        color=info["color"],
        scale=info["scale"],
        position=(
            x,
            info["scale"][1] / 2,
            0
        ),
        collider="box"
    )

    obj.building_type = "road"

    buildings.append(obj)

    money -= info["price"]


# ============================================================
# СТАРТОВЫЕ ДОМА
# ============================================================

for x in [-6, -2, 2, 6]:

    info = BUILDINGS["house"]

    obj = Entity(
        model="cube",
        color=info["color"],
        scale=info["scale"],
        position=(
            x,
            info["scale"][1] / 2,
            4
        ),
        collider="box"
    )

    obj.building_type = "house"

    buildings.append(obj)

    money -= info["price"]

    population += info["population"]


# ============================================================
# ЗАПУСК
# ============================================================

select("house")
update_ui()

app.run()
