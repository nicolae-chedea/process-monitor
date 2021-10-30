import psutil
import os


class ProcessMetrics:
    """
    • % of CPU used
    • private memory used
    • number of open handles / file descriptors
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.cpu = 0
        self.memory = 0
        self.handles = 0

    def find_procs_by_name(self):
        """
        Return a list of processes matching 'name'.
        Taken from here: https://psutil.readthedocs.io/en/latest/#find-process-by-name
        """
        ls = []
        for p in psutil.process_iter(["name", "pid", "cpu_percent", "memory_percent", "num_handles", "memory_info"]):
            if self.name == p.info['name']:
                ls.append(p)
                break
        return ls

    def get_process_data(self):
        processes = self.find_procs_by_name()
        for proc in processes:
            self.cpu = proc.info['cpu_percent']
            self.handles = proc.info['num_handles']
            self.memory = proc.info['memory_info'].private
            break  


if __name__ == '__main__':
    p = ProcessMetrics('python.exe')
    p.get_process_data()
    print(p.name)
    print(p.cpu)
    print(p.handles)
    print(p.memory)
