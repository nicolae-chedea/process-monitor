from metrics import ProcessMetrics
from time import sleep
from datetime import datetime
import csv
from statistics import mean
import warnings


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
        self.timestamps = []
        self.cpu_percentages = []
        self.cpu_average = 0
        self.memory_values = []
        self.memory_average = 0
        self.file_handles = []
        self.files_average = 0

    def gather_data(self):
        process_info = ProcessMetrics(self.process_name)
        for _ in range(0, self.monitoring_duration, self.sampling_interval):
            process_info.get_process_data()
            self.timestamps.append(str(datetime.utcnow()))
            self.cpu_percentages.append(process_info.cpu)
            self.memory_values.append(process_info.memory)
            self.file_handles.append(process_info.handles)
            sleep(self.sampling_interval)
        self.cpu_average = mean(self.cpu_percentages)
        self.memory_average = mean(self.memory_values)
        self.files_average = mean(self.file_handles)
        if self.memory_values == sorted(self.memory_values):
            warnings.warn(f'Process {self.process_name} might have a memory leak, private memory keeps increasing!')

    def write_to_csv(self):
        with open(self.process_name + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'cpu_percentage', 'private_memory', 'file_handles']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for index in range(len(self.timestamps)):
                writer.writerow({'timestamp': self.timestamps[index], 
                                 'cpu_percentage': self.cpu_percentages[index], 
                                 'private_memory': self.memory_values[index], 
                                 'file_handles': self.file_handles[index]})
            avg_fieldnames = ['timestamp', 'average_cpu_percentage', 'average_private_memory', 'average_file_handles']
            writer = csv.DictWriter(csvfile, fieldnames=avg_fieldnames)
            writer.writeheader()
            writer.writerow({'timestamp': datetime.utcnow(), 
                             'average_cpu_percentage': self.cpu_average, 
                             'average_private_memory': self.memory_average, 
                             'average_file_handles': self.files_average})
            if self.memory_values == sorted(self.memory_values):
                writer.writerow({'timestamp': datetime.utcnow(), 
                             'average_private_memory': 'Possible memory leak!'})


if __name__ == '__main__':
    p = ProcessMonitor('python.exe', 30)
    p.gather_data()
    p.write_to_csv()