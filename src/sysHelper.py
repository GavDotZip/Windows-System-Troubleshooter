import ctypes
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


def main():
    print_separator()
    print_system_information()


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
