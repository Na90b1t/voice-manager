import subprocess
import os
import tempfile
from pathlib import Path

# === НАСТРОЙКИ ===
# Определяем папку проекта (где лежит manager.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPER_DIR = os.path.join(BASE_DIR, "piper")  # папка с piper.exe
MODEL_NAME = "ru_RU-irina-medium.onnx"  # имя вашей модели
# =================

def speak(text):
    if not text or not text.strip():
        return

    piper_path = os.path.join(PIPER_DIR, "piper.exe")
    model_path = os.path.join(PIPER_DIR, MODEL_NAME)

    # Проверка файлов
    if not os.path.exists(piper_path):
        print(f"❌ Не найден piper.exe: {piper_path}")
        return
    if not os.path.exists(model_path):
        print(f"❌ Не найдена модель: {model_path}")
        return

    # Создаём временный WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Генерация аудио в файл
        cmd = [piper_path, "--model", model_path, "-f", tmp_path]
        result = subprocess.run(
            cmd,
            input=text.strip() + "\n",
            text=True,
            encoding='utf-8',
            capture_output=True
        )
        if result.returncode != 0:
            print(f"Ошибка Piper: {result.stderr}")
            return

        # Проигрываем через PowerShell (встроено в Windows)
        play_cmd = [
            "powershell", "-c",
            f"(New-Object Media.SoundPlayer '{tmp_path}').PlaySync()"
        ]
        subprocess.run(play_cmd, check=True)

    finally:
        # Удаляем временный файл
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except Exception:
            pass