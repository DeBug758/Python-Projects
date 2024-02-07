import argparse
import json
import time 
import os

class Characteristics:
    total_processes = 0
    sleeping_processes = 0
    running_processes = 0
    zombie_processes = 0
    stopped_processes = 0

    def count_processes(self):
        for proc in psutil.process_iter(['status']):
            self.total_processes += 1
            if proc.info['status'] == psutil.STATUS_SLEEPING:
                self.sleeping_processes += 1
            elif proc.info['status'] == psutil.STATUS_RUNNING:
                self.running_processes += 1
            elif proc.info['status'] == psutil.STATUS_STOPPED:
                self.stopped_processes += 1
            elif proc.info['status'] == psutil.STATUS_ZOMBIE:
                self.zombie_processes += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Interval between snapshots in seconds", type=int, default=30)
    parser.add_argument("-f", help="Output file name", default="snapshot.json")
    parser.add_argument("-n", help="Quantity of snapshot to output", default=20)

    args = parser.parse_args()

    if os.path.exists(args.f):
        os.remove(args.f)
    i=0
    for _ in range(int(args.n)):
        data = Characteristics()
        data.count_processes()
        snapsot = dict()
        snapsot['Tasks'] = {'total': data.total_processes,
                            'running': data.running_processes,
                            'sleeping': data.sleeping_processes,
                            'stopped': data.stopped_processes,
                            'zombie': data.zombie_processes}
        cpu = psutil.cpu_times_percent(interval=args.i)
        snapsot['%CPU'] = {'user': cpu.user, 'system': cpu.system, 'idle': cpu.idle}
        mem = psutil.virtual_memory()
        snapsot['KiB Mem'] = {'total': round(mem.total / 1024), 'free': round(mem.free / 1024), 'used': round(mem.used / 1024)}
        swap = psutil.swap_memory()
        snapsot['KiB Swap'] = {'total': round(swap.total / 1024), 'free': round(swap.free / 1024), 'used': round(swap.used / 1000)}
        var = round(1624406400.0) + int(args.i) * i
        #var = 1624406400
        snapsot['Timestamp'] = var
        formatted_data = json.dumps(snapsot, indent=None)#.replace("}, ", "},\n")
        with open(args.f, "a") as file:
            file.write(formatted_data)
            file.write('\n\n')
        os.system('clear')
        print(formatted_data, end="\r")
        i += 1


if __name__ == "__main__":
    main()
