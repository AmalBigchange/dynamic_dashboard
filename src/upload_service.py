# system_uploader.py

import psutil
import platform
import time
import requests
import json

API_ENDPOINT = "https://8mj767oeu1.execute-api.eu-west-2.amazonaws.com/test/update"  # Replace with your real endpoint

def get_system_info():
    # CPU temperature (Linux only)
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps["coretemp"][0].current if "coretemp" in temps else None
    except:
        cpu_temp = None

    # Memory usage
    mem = psutil.virtual_memory()

    # Disk usage
    disk = psutil.disk_usage('/')

    # Network usage
    net_io = psutil.net_io_counters()

    return {
        "platform": platform.system(),
        "cpu_temp": cpu_temp,
        "memory": {
            "total": mem.total,
            "used": mem.used,
            "percent": mem.percent
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "percent": disk.percent
        },
        "network": {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv
        },
        "timestamp": time.time()
    }

def send_data():
    while True:
        try:
            data = get_system_info()
            response = requests.post(API_ENDPOINT, json=data)
            print(f"[{time.strftime('%H:%M:%S')}] Uploaded: {response.status_code} | {response.text}")
        except Exception as e:
            print(f"Error sending data: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    send_data()
