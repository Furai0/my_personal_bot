import subprocess
import datetime
import time
bot_folder = '/home/f/disks/c_os_staff/FarraHella_Bot/'
file_main = 'FarraHella_main.py'
python_v = '/.venv/bin/python3.8'


venv_folder = bot_folder + '.venv/'
venv_act = venv_folder + 'bin/activate'


process = python_v + file
def kill(process_name):
    try:
        # Сначала пробуем мягко завершить (SIGTERM)
        subprocess.run(["pkill", "-f", process_name], check=True)
        print(f"Процессам {process_name} отправлен сигнал завершения")
    except subprocess.CalledProcessError:
        try:
            # Если не сработало, пробуем SIGKILL
            subprocess.run(["pkill", "-9", "-f", process_name], check=True)
            print(f"Процессы {process_name} принудительно завершены")
        except subprocess.CalledProcessError:
            print(f"Процессы {process_name} не найдены")
def restart():
    kill(process)
    try:
        subprocess.run(f'cd {folder_with_git} ;git reset --hard ;git pull', shell=True)
    except:
        None
    subprocess.run(f'{venv} {file} &', shell=True)
restart()
while True:
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        restart()
    time.sleep(60)  # Проверяем каждую минуту