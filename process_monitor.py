from metrics import ProcessMetrics
from time import sleep
from datetime import datetime
import csv


class ProcessMonitor:
    """
    • periodically gathers process metrics (for a specified amount of time)
    • creates a report of the gathered process metrics (in CSV format)
    • outputs the average for each process metric
    • detects possible memory leaks and raises a warning
    """
    def __init__(self, process_name: str, monitoring_duration: int,
                 sampling_interval: int = 5) -> None:
        self.process_name = process_name
        self.monitoring_duration = monitoring_duration
        self.sampling_interval = sampling_interval

    def monitor(self):
        print(f"process: {self.process_name}")
        with open(self.process_name + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'cpu_percentage', 'private_memory', 'file_handles']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        process_info = ProcessMetrics(self.process_name)
        for _ in range(0, self.monitoring_duration, self.sampling_interval):
            process_info.get_process_data()
            with open(self.process_name + '.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'timestamp': datetime.utcnow(), 'cpu_percentage': process_info.cpu, 
                'private_memory': process_info.memory, 'file_handles': process_info.handles})

            sleep(self.sampling_interval)


if __name__ == '__main__':
    p = ProcessMonitor('Code.exe', 30)
    p.monitor()