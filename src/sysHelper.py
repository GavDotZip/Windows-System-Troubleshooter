import platform
import psutil
import wmi


def print_separator():
    print("\n", "-" * 100)


def print_system_information():
    print(f"\nSystem: {uname.system}")


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

    main()
