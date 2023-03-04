import subprocess

# Tìm tất cả các tiến trình có tên bot.py và dừng chúng
subprocess.call("ps aux | grep bot.py | awk '{print $2}' | xargs kill", shell=True)
