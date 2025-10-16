import subprocess

def speak(text):
    cmd = [
        r".\piper.exe",
        "--model", "ru_RU-irina-medium.onnx"
    ]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True, encoding='utf-8')
    process.communicate(input=text + "\n")

speak("Привет!")