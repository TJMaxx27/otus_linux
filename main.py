import subprocess
from datetime import datetime

def get_ps_aux_output():
    ps_aux_output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
    return ps_aux_output.split('\n')

def parse_ps_aux_output(ps_output):
    users = {}
    total_processes = 0
    total_memory_percent = 0.0
    total_cpu_percent = 0.0
    max_memory_process = ('', 0.0)
    max_cpu_process = ('', 0.0)

    for line in ps_output[1:]:
        if line.strip() == '':
            continue

        fields = line.split()
        user = fields[0]
        cpu_percent = float(fields[2])
        memory_percent = float(fields[3])
        command = ' '.join(fields[10:])

        if user in users:
            users[user] += 1
        else:
            users[user] = 1

        total_processes += 1
        total_memory_percent += memory_percent
        total_cpu_percent += cpu_percent

        if memory_percent > max_memory_process[1]:
            max_memory_process = (command[:20], memory_percent)
        if cpu_percent > max_cpu_process[1]:
            max_cpu_process = (command[:20], cpu_percent)

    return users, total_processes, total_memory_percent, total_cpu_percent, max_memory_process, max_cpu_process

def save_report(users, total_processes, total_memory_percent, total_cpu_percent, max_memory_process, max_cpu_process):
    current_time = datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = f"{current_time}-scan.txt"
    with open(filename, 'w') as f:
        f.write("Отчёт о состоянии системы:\n")
        f.write(f"Пользователи системы: {', '.join(users.keys())}\n")
        f.write(f"Процессов запущено: {total_processes}\n")
        f.write("Пользовательских процессов:\n")
        for user, count in users.items():
            f.write(f"{user}: {count}\n")
        f.write(f"Всего памяти используется: {total_memory_percent:.1f}%\n")
        f.write(f"Всего CPU используется: {total_cpu_percent:.1f}%\n")
        f.write(f"Больше всего памяти использует: ({max_memory_process[0]}, {max_memory_process[1]:.1f}%)\n")
        f.write(f"Больше всего CPU использует: ({max_cpu_process[0]}, {max_cpu_process[1]:.1f}%)\n")
    print(f"Отчёт сохранён в файле: {filename}")

ps_output = get_ps_aux_output()

users, total_processes, total_memory_percent, total_cpu_percent, max_memory_process, max_cpu_process = parse_ps_aux_output(ps_output)

save_report(users, total_processes, total_memory_percent, total_cpu_percent, max_memory_process, max_cpu_process)