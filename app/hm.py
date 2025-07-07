import subprocess
import time
import json
from multiprocessing import Process, Queue
from collections import defaultdict


def get_temperature():
    result = subprocess.run(['sensors', '-j'],
                            capture_output=True, text=True, check=True)
    output = json.loads(result.stdout)
    monitored = {}
    for device, device_data in output.items():
        device_temps = []
        for sensor, sensor_data in device_data.items():
            try:
                for key, value in sensor_data.items():
                    if key.startswith('temp') and key.endswith('input'):
                        temp_name = key.replace('_input', '')
                        temp_key = f'{sensor} - {value}'
                        device_temps.append(round(value))
            except:
                None
        if device_temps:
            monitored[device] = device_temps
    return monitored


def show_temp(temp):
    b = ''
    for key, value in temp.items():
        a = f'{key} -'
        temp_values = []
        for val in value:
            if val is not None:
                temp_values.append(str(val))
        if temp_values:
            a += ' ' + ', '.join(temp_values)
        a += '°C\n'
        b += a
    return b


temperature_data_hour = defaultdict(list)
timestamp_data_hour = defaultdict(list)

temperature_data_day = defaultdict(list)
timestamp_data_day = defaultdict(list)

def collect_temperature_data(current_data, time_in_secounds, timestamp_data, temperature_data):
    """Функция для сбора данных температурных показателей"""
    current_time = time.time()

    for sensor, temps in current_data.items():
        # Добавляем данные с временной меткой
        timestamp_data[sensor].append((current_time, temps))
        temperature_data[sensor].append(temps)

    # Удаляем данные старше одного часа
    one_hour_ago = current_time - time_in_secounds
    for sensor in list(timestamp_data.keys()):
        # Фильтруем данные по времени
        timestamp_data[sensor] = [
            (t, temps) for t, temps in timestamp_data[sensor] if t >= one_hour_ago
        ]
        # Если для датчика не осталось данных, удаляем его
        if not timestamp_data[sensor]:
            del timestamp_data[sensor]
            if sensor in temperature_data:
                del temperature_data[sensor]

def get_hourly_average_temperatures(timestamp_data):
    """Функция для получения средних значений за последний час"""
    averages = {}

    for sensor, data in timestamp_data.items():
        if not data:
            continue

        # Собираем все показания за час
        all_readings = []
        for _, temps in data:
            all_readings.append(temps)

        # Если нет данных, пропускаем
        if not all_readings:
            continue

        # Определяем количество сенсоров у данного датчика
        num_sensors = len(all_readings[0])
        sensor_averages = []

        # Вычисляем среднее для каждого сенсора
        for i in range(num_sensors):
            sensor_values = []
            for reading in all_readings:
                if i < len(reading):  # На случай, если количество сенсоров менялось
                    sensor_values.append(reading[i])

            if sensor_values:
                avg = sum(sensor_values) / len(sensor_values)
                sensor_averages.append(round(avg, 2))

        if sensor_averages:
            averages[sensor] = sensor_averages

    return averages

def get_usage():
    result = subprocess.run(['top', '-b', '-n', '1', '-d', '1'],
                           capture_output=True, text=True, check=True)
    output = result.stdout
    result = []
    for line in output.split('\n'):
        # print(result)
        if '%Cpu(s):' in line:
            parts = line.split(',')
            us = parts[0]
            us = us[:-2][8:]
            sy = parts[1]
            sy = sy[:-2]
            cpu_usage = float(sy) + float(us)
            result.append(round(cpu_usage))
        if 'MiB Mem :' in line:
            parts = line.split(',')
            total = parts[0]
            total = float(total[:-5][9:])
            used = parts[2]
            memory_used = float(used[:-4])
            memory_free = total - memory_used
            result.append(round(memory_free))
            result.append(round(memory_used))
        if line.startswith('top'):
            parts = line.split(' ')
            uptime = parts[4]
            uptime = uptime[:-1]
            result.append(uptime)
    return result


def collect_usage_data(time_hours:int, cpu, mem_free, mem_use):
    seconds = time_hours * 3600
    timer = 0
    if timer >= seconds:
        cpu.pop(0)
        mem_free.pop(0)
        mem_use.pop(0)
    cpu.append(get_usage()[1])
    mem_free.append(get_usage()[2])
    mem_use.append(get_usage()[3])
    timer += 1
    time.sleep(1)


def get_avg_usage(cpu, mem_free, mem_use):
    avg_cpu = sum(cpu) / len(cpu)
    avg_free = sum(mem_free) / len(mem_free)
    avg_use = sum(mem_use) / len(mem_use)
    return (round(avg_cpu), round(avg_free), round(avg_use))


# USAGE
avg_temp_hour = []
queue_temp_hour = Queue()

avg_temp_day = []
queue_temp_day = Queue()

cpu_hour = []
mem_free_hour = []
mem_use_hour = []
queue_usage_hour = Queue()

cpu_day = []
mem_free_day = []
mem_use_day = []
queue_usage_day = Queue()
def server_monitoring():
    while True:
        time.sleep(1)
        collect_temperature_data(get_temperature(), 3600, timestamp_data_hour, temperature_data_hour)
        avg_temp_hour = get_hourly_average_temperatures(timestamp_data_hour)
        queue_temp_hour.put(avg_temp_hour)

        collect_temperature_data(get_temperature(), 84600, timestamp_data_day, temperature_data_day)
        avg_temp_day = get_hourly_average_temperatures(timestamp_data_day)
        queue_temp_day.put(avg_temp_day)

        collect_usage_data(1, cpu_hour, mem_free_hour, mem_use_hour)
        avg_usage_hour = get_avg_usage(cpu_hour, mem_free_hour, mem_use_hour)
        queue_usage_hour.put(avg_usage_hour)

        collect_usage_data(24, cpu_day, mem_free_day, mem_use_day)
        avg_usage_day = get_avg_usage(cpu_day, mem_free_day, mem_use_day)
        queue_usage_day.put(avg_usage_day)

monitor_process = Process(target=server_monitoring)
monitor_process.start()

