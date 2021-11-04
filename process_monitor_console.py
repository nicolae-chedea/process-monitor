import argparse
from process_monitor import ProcessMonitor
from prettytable import PrettyTable
from datetime import datetime

def process_data(name, duration, polling, csv=False): 
    process_utils =  ProcessMonitor(name, duration, polling)
    process_utils.gather_data() 
    table = PrettyTable()
    table.field_names = ['timestamp', 'cpu_percentage', 'private_memory', 'file_handles']

    for index in range(len(process_utils.timestamps)):
        table.add_row([process_utils.timestamps[index], process_utils.cpu_percentages[index], process_utils.memory_values[index], process_utils.file_handles[index]])
    table.add_row(['timestamp', 'average_cpu_percentage', 'average_private_memory', 'average_file_handles'])
    table.add_row([datetime.utcnow(), process_utils.cpu_average, process_utils.memory_average, process_utils.files_average])
    if process_utils.memory_values == sorted(process_utils.memory_values):
        table.add_row(['', '', 'Possible memory leak!', ''])
    print(table)
    if csv:
        process_utils.write_to_csv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process monitoring')
    parser.add_argument('name', type=str, help='enter process name')
    parser.add_argument('duration', type=int, help='enter monitoring duration')
    parser.add_argument('-p', '--polling', type=int, default=5, help='enter polling interval')
    parser.add_argument('-c', '--csv', action="store_true", help='set flag if you need the csv generated')
    args = parser.parse_args()
    process_data(args.name, args.duration, args.polling, args.csv)