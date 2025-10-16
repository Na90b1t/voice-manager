import json
import time
import datetime
from piper_wrapper import speak
import os

def load_schedule():
    # Определяем папку, где лежит этот скрипт
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    schedule_path = os.path.join(BASE_DIR, "schedule.json")
    
    try:
        with open(schedule_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки расписания: {e}")
        return {}

def get_current_schedule(schedule):
    # Получаем текущий день недели как строку: 'monday', 'tuesday', ...
    weekday_en = datetime.datetime.now().strftime("%A").lower() # Функция strftime("%A") возвращает английские названия дней недели
    return schedule.get(weekday_en, {})

def main():
    print("✅ Голосовой менеджер запущен. Проверка каждую минуту...")
    last_triggered = set()

    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        schedule = load_schedule()
        today_schedule = get_current_schedule(schedule)

        if current_time in today_schedule and current_time not in last_triggered:
            message = today_schedule[current_time]
            print(f"📢 [{current_time}] {message}")
            speak(message)
            last_triggered.add(current_time)

        # Сброс в полночь
        if current_time == "00:01":
            last_triggered.clear()

        time.sleep(60)  # ждём 1 минуту

if __name__ == "__main__":
    main()