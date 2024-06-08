import json

import psutil
import GPUtil
import pynvml

from app.utils.merge_dicts import merge_dicts
from app.buttons.usage.asked_devices import get_asked_devices


with open(".config/config.json", encoding="utf-8") as f:
    config = json.load(f)
        
def get_usage(
    get_all=True if config["settings"]["optimized-usage-display"] == "false" else False,
    asked_devices=get_asked_devices()
):
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
        disks = psutil.disk_partitions()
        for disk in disks:
            try:
                disk_name = disk.device.replace("\\", "").replace(":", "")
                if get_all or any(item[1] == disk_name for item in asked_devices):
                    
                    computer_info["disks"][disk_name] = {}
                    disk_usage = psutil.disk_usage(disk.device)
                    
                    if get_all or any(item[2] == "total_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["total_gb"] = round(disk_usage.total / 1024**3, 2)
                    if get_all or any(item[2] == "used_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["used_gb"] = round(disk_usage.used / 1024**3, 2)
                    if get_all or any(item[2] == "free_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["free_gb"] = round(disk_usage.free / 1024**3, 2)
                    if get_all or any(item[2] == "usage_percent" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["usage_percent"] = disk_usage.percent
                        
            except Exception as e:
                print("Usage Disks Error:", e)
                
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
            except pynvml.nvml.NVML_ERROR_NOT_SUPPORTED:
                computer_info["gpus"]["defaultGPU"] = {}
                
                config["settings"]["gpu_method"] = "None"
                with open(".config/config.json", "w", encoding="utf-8") as json_file:
                    json.dump(config, json_file, indent=4)
                    
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