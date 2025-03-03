import json

import psutil
import GPUtil
import pynvml

from app.utils.settings.get_config import get_config
from app.utils.settings.save_config import save_config
from app.utils.merge_dicts import merge_dicts
from .asked_devices import get_asked_devices
from app.utils.platform import is_linux
from app.utils.logger import log


def get_usage(get_all=None, asked_devices=[]):
    config = get_config()
    if get_all is None:
        get_all = not config["settings"]["optimized_usage_display"]
    if not asked_devices and not get_all:
        asked_devices = get_asked_devices()
        
    computer_info = {}
    
    # CPU
    if get_all or any(item[0] == 'cpu' for item in asked_devices):
        cpu_percent = psutil.cpu_percent()
        computer_info["cpu"] = {"usage_percent": cpu_percent}

    # Memory
    if get_all or any(item[0] == 'memory' for item in asked_devices):
        memory = psutil.virtual_memory()
        computer_info["memory"] = {}
        
        if get_all or any(item[1] == 'total_gb' for item in asked_devices):
            computer_info["memory"]["total_gb"] = round(memory.total / 1024**3, 2)
        if get_all or any(item[1] == 'used_gb' for item in asked_devices):
            computer_info["memory"]["used_gb"] = round(memory.total / 1024**3 - memory.available / 1024**3, 2)
        if get_all or any(item[1] == 'available_gb' for item in asked_devices):
            computer_info["memory"]["available_gb"] = round(memory.available / 1024**3, 2)
        if get_all or any(item[1] == 'usage_percent' for item in asked_devices):
            computer_info["memory"]["usage_percent"] = memory[2]

    # Hard disk
    if get_all or any(item[0] == 'disks' for item in asked_devices):
        computer_info["disks"] = {}
        disks = psutil.disk_partitions(all=True)
        for disk in disks:
            try:
                disk_name = disk.device.replace("\\", "").replace(":", "").strip()
                
                # Skip loop devices (Linux) (e.g. /dev/loop0)
                if is_linux and (disk_name.startswith("/dev/loop") or "snap" in disk.mountpoint):
                    continue
                
                # Skip boot partition (Linux)
                # if is_linux and disk.mountpoint == "/boot":
                #     continue
                
                # Skip duplicates entries
                if computer_info["disks"].get(disk_name):
                    continue
                
                if get_all or any(item[1] == disk_name for item in asked_devices or "squashfs" in disk.fstype):
                    
                    computer_info["disks"][disk_name] = {}
                    disk_usage = psutil.disk_usage(disk.mountpoint)
                    
                    if get_all or any(item[2] == "total_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["total_gb"] = round(disk_usage.total / 1024**3, 2)
                    if get_all or any(item[2] == "used_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["used_gb"] = round(disk_usage.used / 1024**3, 2)
                    if get_all or any(item[2] == "free_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["free_gb"] = round(disk_usage.free / 1024**3, 2)
                    if get_all or any(item[2] == "usage_percent" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["usage_percent"] = disk_usage.percent
                    
                    if not computer_info["disks"][disk_name].get("total_gb"):
                        computer_info["disks"].pop(disk_name)
                        
            except Exception as e:
                # log.exception(e, "Usage Disks Error", log_traceback=False)
                pass
            
        # Sort the disks by total size
        computer_info["disks"] = dict(sorted(computer_info["disks"].items(), key=lambda item: item[1].get("total_gb", 0), reverse=True))
        
    # Network
    if get_all or any(item[0] == 'network' for item in asked_devices):
        network_io_counters = psutil.net_io_counters()
        computer_info["network"] = {
            "bytes_sent": network_io_counters.bytes_sent,
            "bytes_recv": network_io_counters.bytes_recv,
        }

    # GPU
    if get_all or any(item[0] == 'gpus' for item in asked_devices):
        computer_info["gpus"] = {}
        if config["settings"]["gpu_method"] == "nvidia (pynvml)":
            try:
                num_gpus = pynvml.nvmlDeviceGetCount()
                for count in range(num_gpus):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(count)
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    computer_info["gpus"][f"GPU{count + 1}"] = {
                        "usage_percent": int(utilization.gpu),
                    }
            # Unsupported graphics cards
            except Exception:
                computer_info["gpus"]["defaultGPU"] = {}
                
                config["settings"]["gpu_method"] = "None"
                save_config(config)
                    
        elif config["settings"]["gpu_method"] == "nvidia (GPUtil)":

            gpus = GPUtil.getGPUs()
            computer_info["gpus"] = {}
            for count, gpu in enumerate(gpus):
                computer_info["gpus"][f"GPU{count + 1}"] = {
                    "name": gpu.name,
                    "used_mb": gpu.memoryUsed,
                    "total_mb": gpu.memoryTotal,
                    "available_mb": gpu.memoryTotal - gpu.memoryUsed,
                    "usage_percent": int(gpu.load * 100),
                }
                
        else:
            computer_info["gpus"]["defaultGPU"] = {}
            
        if "GPU1" in computer_info["gpus"]:
            computer_info["gpus"]["defaultGPU"] = computer_info["gpus"]["GPU1"]
            
    if get_all == False:
        computer_info = merge_dicts(get_usage(True), computer_info)
    return computer_info