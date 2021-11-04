# process-monitor
Script meant to monitor processes by name for a given duration.
Results can be displayed or stored in a csv file.
Script should run on Windows, MacOS or Linux distributions.

## Prerequisites
Make sure to install dependencies:
 - Python 3.9 or newer
 - libraries from [requirements.txt](requirements.txt)

## Usages
Easiest way to use the script is by its graphical user interface:
```
python -m process_monitor_guy.py
```
Alternatively, it can be used as a console application, run the following command to get more details:
```
python -m process_monitor_console.py --help
```
If csv output is selected, a csv file having the process name as file name will be generated.

## Known limitations
- GUI is not responsive
- output for longer monitoring durations only happens after the monitoring finishes
- there is no data validation, application will crash when entering wrong data
- application works under the assumption that a single process with the given name exists and is monitored. If multiple processes with the same name exist, the first one will be picked.
