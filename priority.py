from tabulate import tabulate

# priority_queues = {}
# processes = []
# selected_processes = []
n = 0   # number of process

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Process:

    def __init__(self, name, arrivalTime, burstTime, priority):
        self.name = name
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.remainingTime = burstTime
        self.priority = priority
        self.finishTime = None
        self.turnaroundTime = None
        self.Tr_Ts = None  # Ratio of turnaround time to service(burst) time
        self.selected = False

    def execute(self, duration, currentTime):
        if self.remainingTime - duration == 0:
            self.remainingTime = 0
            self.finishTime = currentTime
            self.turnaroundTime = self.finishTime - self.arrivalTime
            self.Tr_Ts = self.turnaroundTime / self.burstTime
        else:
            self.remainingTime -= duration


def get_process_info(name):
    info = input(f'{name}: ').split(' ')
    return int(info[0]), int(info[1]), int(info[2])

def update_queues(time, processes, priority_queues, selected_processes):
    for p in processes:
        if p.arrivalTime <= time and p.selected == False:
            p.selected = True
            index = processes.index(p)
            selected_processes.append(processes[index])
            if p.priority not in priority_queues.keys():
                priority_queues[p.priority] = []
            priority_queues[p.priority].append(p)


def remove_finished_processe(process, priority_queues):
    if process.finishTime != None:
        priority_queues[process.priority].remove(process)


def select_highest_priority(priority_queues):
    selected_processes = None
    priorities = list(priority_queues.keys())
    priorities.sort(reverse=False)
    for priority in priorities:
        if len(priority_queues[priority]) > 0:
            selected_processes = priority_queues[priority][0]
            break
        else:
            continue

    return selected_processes

def choose_process(priority_queues, runningProcess, preemptive):
    choosen_process = None
    if preemptive:
        # bedoon ghabze
        if runningProcess == None or runningProcess.remainingTime == 0:
            choosen_process = select_highest_priority(priority_queues)
        else:
            choosen_process = runningProcess
    else:
        # ba ghabze
        choosen_process = select_highest_priority(priority_queues)

    return choosen_process


def print_processes_info(processes, order_of_execution):

    times = ['time']
    t = 0
    for i in order_of_execution:
        times.append(f'{t} - {t + 1}')
        t += 1
    op = order_of_execution.copy()
    op.insert(0, 'Process')
    print(bcolors.WARNING + tabulate([times, op], headers='firstrow', tablefmt='fancy_grid') + bcolors.ENDC)

    print()

    info = [['Process', 'Arrival Time', 'Burst Time', 'Priority', 'Finish Time', 'Turnaround Time', 'Waiting Time', 'Tr/Ts']]
    for process in processes:
        row = [process.name, process.arrivalTime, process.burstTime, process.priority, process.finishTime, process.turnaroundTime, process.turnaroundTime - process.burstTime, process.Tr_Ts]
        info.append(row)


    print(bcolors.OKCYAN + tabulate(info, headers='firstrow', tablefmt='fancy_grid') + bcolors.ENDC)

    sum = 0
    for process in processes:
        sum += process.turnaroundTime

    print(f'mean tr: {sum/n}')

    sum = 0
    for process in processes:
        sum += process.Tr_Ts

    print(f'mean tr/ts: {sum / n}')




def number_of_unselected_processes(processes):
    count = 0
    for p in processes:
        if p.selected == False:
            count += 1

    return count

def run(processes_list, preemptive):
    processes = processes_list.copy()
    priority_queues = {}
    selected_processes = []
    order_of_execution = []

    currentTime = 0
    step = 1
    runningProcess = None
    while True:
        update_queues(currentTime, processes, priority_queues, selected_processes)
        runningProcess = choose_process(priority_queues, runningProcess, preemptive)
        currentTime += step
        if runningProcess != None:
            runningProcess.execute(step, currentTime)
            remove_finished_processe(runningProcess, priority_queues)
            order_of_execution.append(runningProcess.name)
        elif number_of_unselected_processes(processes) == 0:
            break

    print_processes_info(processes, order_of_execution)



def main():
    processes_1 = []
    processes_2 = []
    global n
    n = int(input('Enter Number Of Process: '))
    print('N | A  B  P')
    for i in range(n):
        name = f'P{i+1}'
        arrivalTime, burstTime, priority = get_process_info(name)
        p1 = Process(name, arrivalTime, burstTime, priority)
        p2 = Process(name, arrivalTime, burstTime, priority)
        processes_1.append(p1)
        processes_2.append(p2)

    print(bcolors.FAIL + "------------------------------- Preemptive -------------------------------" + bcolors.ENDC)
    run(processes_1, True)
    print("\n\n")
    print(bcolors.HEADER + "----------------------------- Non Preemptive -----------------------------" + bcolors.ENDC)
    run(processes_2, False)
    # print(priorities)
    # print(processes)



if __name__ == '__main__':
    main()