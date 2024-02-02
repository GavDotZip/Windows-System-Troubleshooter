import ctypes
import os
import re
import socket
import subprocess
import uuid
from datetime import datetime
import platform
import psutil
import wmi


def print_separator():
    print("\n", "-" * 100)


def print_system_information():
    print(f"\nSystem: {uname.system}")
    print(f"Device Name: {uname.node}")
    print(f"Serial Number: {serial_number}")
    print(f"Windows Version: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    print(f"Boot Time: {bt.day}/{bt.month}/{bt.year} {bt.hour}:{bt.minute}:{bt.second}")
    print(f"Uptime: {days} days, {hour:02}:{mins:02}:{sec:02}")


def print_cpu_information():
    print("\nCPU Usage Per Core")
    for i, (percent, freq) in enumerate(zip(cpu_percent, cpu_freq), start=True):
        print(f"Core {i}: {percent}% \nFrequency: {freq.current} MHz")


def print_virtual_memory_information():
    print(f"\nVirtual Memory")
    print(f"Total: {virtual_mem.total / (1024 ** 3):.2f} GB")
    print(f"Used: {virtual_mem.used / (1024 ** 3):.2f} GB")
    print(f"Swap Total: {swap.total / (1024 ** 3):.2f} GB")
    print(f"Swap Used: {swap.used / (1024 ** 3):.2f} GB")


def print_disk_information():
    print(f"\nDisk Information")
    print(f"Total Disk Information: {disk.total / (1024 ** 3):.2f} GB")
    print(f"Used Disk Space: {disk.used / (1024 ** 3):.2f} GB")
    print(f"Free Disk Space: {disk.free / (1024 ** 3):.2f} GB")


def print_network_information():
    devices = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    devices = devices.decode('ascii')
    devices = devices.replace("\r", "")
    network = psutil.net_io_counters()
    print("\nNetwork Information\n ")
    print("IP Address: ", socket.gethostbyname(socket.gethostname()))
    print(f"MAC Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")
    print(f"Bytes Received: {network.bytes_recv / (1024 ** 2):.2f} MB")
    print(f"Bytes Sent: {network.bytes_sent / (1024 ** 2):.2f} MB")
    print(devices)


def print_battery_information():
    print("\nBattery Information ")
    try:
        temperatures = psutil.sensors_temperatures()
        if temperatures:
            print("\nTemperatures: ")
            for name, entries in temperatures.items():
                for entry in entries:
                    print(f"{name}: {entry.current}°C")
        else:
            print("\nTemperature Unavailable")
    except AttributeError:
        print("\nTemperature Unavailable")

    c = wmi.WMI()
    t = wmi.WMI(moniker="//.root/wmi")

    batts1 = c.CIM_Battery(Caption='Portable Battery')
    for i, b in enumerate(batts1):
        print('Battery %d Design Capacity: %d mWh' % (i, b.DesignCapacity or 0))

    batts = t.ExecQuery('Select * from BatteryFullChargedCapacity')
    for i, b in enumerate(batts):
        print('Battery %d Fully Charged Capacity: %d mWh' % (i, b.FullChargedCapacity))

    batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
    for i, b in enumerate(batts):
        print('\nTag:               ' + str(b.Tag))
        print('Name:                ' + b.InstanceName)
        print('PowerOnline:         ' + str(b.PowerOnline))
        print('Discharging:         ' + str(b.Discharging))
        print('Charging:            ' + str(b.Charging))
        print('Voltage:             ' + str(b.Voltage))
        print('DischargeRate:       ' + str(b.DischargeRate))
        print('ChargeRate:          ' + str(b.ChargeRate))
        print('RemainingCapacity:   ' + str(b.RemainingCapacity))
        print('Active:              ' + str(b.Active))
        print('Critical:            ' + str(b.Critical))

    battery = psutil.sensors_battery()
    if battery:
        plugged = "Plugged In" if battery.power_plugged else "Not Plugged In"
        print(f"\nBattery StatusL {plugged}, {battery.percent}%")
    else:
        print("\nBattery Information Unavailable")


def open_troubleshooting_tools():
    print("Select the following for tools:\n"
          "1 - Devices and Printers\n"
          "2 - System Properties\n"
          "3 - Task Manager\n"
          "4 - Device Manager\n"
          "5 - Task Scheduler\n"
          "Enter 'exit' to close the program")
    while True:
        user_options = input("\nSelect an Option: ")

        if user_options.lower() == 'exit':
            print("Shutting down...")
            break
        elif user_options == '1':
            print("Devices and Printers...")
            os.system('control /name Microsoft.DevicesAndPrinters')
        elif user_options == '2':
            print("System Properties...")
            os.system('start sysdm.cpl')
        elif user_options == '3':
            print("Task Manager...")
            os.system('start taskmgr.exe')
        elif user_options == '4':
            print("Device Manager...")
            os.system('start devmgmt.msc')
        elif user_options == '5':
            print("Task Scheduler...")
            os.system('start taskschd.msc')

def main():
    print_separator()
    print_system_information()
    print_cpu_information()
    print_separator()
    print_virtual_memory_information()
    print_separator()
    print_disk_information()
    print_separator()
    print_network_information()
    print_separator()
    print_battery_information()
    print_separator()
    open_troubleshooting_tools()


if __name__ == "__main__":
    # Script execution starts here
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_freq = psutil.cpu_freq(percpu=True)
    uname = platform.uname()
    sn = wmi.WMI()
    bios = sn.Win32_BIOS()[0]
    serial_number = bios.SerialNumber
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    lib = ctypes.windll.kernel32
    upT = lib.GetTickCount64()
    upT = int(str(upT)[:-3])
    mins, sec = divmod(upT, 60)
    hour, mins = divmod(mins, 60)
    days, hour = divmod(hour, 24)

    virtual_mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    disk = psutil.disk_usage('/')

    main()
