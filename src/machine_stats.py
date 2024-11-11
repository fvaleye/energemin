import contextlib
import platform
import socket

import psutil


def get_stats_sensors() -> dict[str, int]:
    """
    Get the sensors data from the system
    """
    sensors = {}
    with contextlib.suppress(AttributeError):
        sensors["fans"] = psutil.sensors_fans()

    try:
        temps = psutil.sensors_temperatures()
        sensors["temperatures"] = {name: sensors[0].current
                        for name, sensors in temps.items() if sensors}
    except AttributeError:
        pass

    try:
        battery = psutil.sensors_battery()
        sensors['battery_percent'] = battery.percent
        sensors['battery_power_plugged'] = battery.power_plugged

    except AttributeError:
        pass

    return sensors

def get_machine_information() -> dict[str, str]:
    """
    Get the machine information
    """
    machine_info = {}
    try:
        machine_info["machine_name"] = socket.gethostname()
        machine_info["machine_type"] = platform.machine()
        machine_info["machine_arch"] = platform.architecture()
        machine_info["machine_processor"] = platform.processor()
        machine_info["machine_platform"] = platform.platform()
    except Exception:
        pass
    return machine_info

def get_running_processes() -> dict[str, int]:
    """
    Get the running processes
    """
    return psutil.process_iter()


def get_network_information() -> dict[str, int]:
    """
    Get the network information
    """
    return psutil.net_io_counters()._asdict()

def get_cpu_information() -> dict:
    """
    Get the cpu information
    """
    cpu_info = {}
    cpu_info["cpu_percent"] = psutil.cpu_percent(interval=1)
    cpu_info["cpu_count_physical"] = psutil.cpu_count(logical=False)
    cpu_info["cpu_count_logical"] = psutil.cpu_count(logical=True)
    return cpu_info

def get_disk_information() -> dict[str, int]:
    """
    Get the disk information
    """
    disk_info = {}
    try:
        swap = psutil.swap_memory()
        disk_info["swap_total"] = swap.total
        disk_info["swap_used"] = swap.used
        disk_info["swap_percent"] = swap.percent
    except AttributeError:
        pass

    try:
        disk = psutil.disk_usage("/")
        disk_info["disk_total"] = disk.total
        disk_info["disk_used"] = disk.used
        disk_info["disk_percent"] = disk.percent
    except AttributeError:
        pass

    return disk_info

def get_memory_information() -> dict[str, int]:
    """
    Get the memory information
    """
    memory_info = {}
    try:
        mem = psutil.virtual_memory()
        memory_info["memory_total"] = mem.total
        memory_info["memory_available"] = mem.available
        memory_info["memory_used"] = mem.used
        memory_info["memory_percent"] = mem.percent
    except AttributeError:
        pass
    return memory_info

def get_battery_information() -> dict[str, int]:
    """
    Get the battery information
    """
    battery_info = {}
    try:
        battery = psutil.sensors_battery()
        battery_info["battery_percent"] = battery.percent
        battery_info["battery_power_plugged"] = battery.power_plugged
    except AttributeError:
        pass
    return battery_info


def get_list_of_running_processes(limit: int = 10) -> dict[str, int]:
    """
    Get a list of running processes sorted by memory usage (RSS).

    Args:
    limit (int, optional): The maximum number of processes to return. If None, returns all processes.

    Returns:
    list: A list of dictionaries containing process information, sorted by RSS memory usage.
    """
    processes_info = {}
    proc_list = []
    current_limit = 0
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
        if current_limit >= limit:
            break
        try:
            mem_info = proc.memory_info()
            proc_info = {
                'pid': proc.pid,
                'name': proc.name(),
                'username': proc.username(),
                'rss': mem_info.rss / (1024 * 1024),  # RSS in MB
                'vms': mem_info.vms / (1024 * 1024),  # VMS in MB
                'cpu_percent': proc.cpu_percent(interval=0.1)
            }
            proc_list.append(proc_info)
            current_limit += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    proc_list.sort(key=lambda x: x['rss'], reverse=True)
    processes_info['running_processes'] = proc_list

    return processes_info


def get_stats_network() -> dict[str, int]:
    """
    Get the network information
    """
    network_info = {}
    net = psutil.net_io_counters()
    network_info["bytes_sent"] = net.bytes_sent
    network_info["bytes_recv"] = net.bytes_recv
    return network_info
