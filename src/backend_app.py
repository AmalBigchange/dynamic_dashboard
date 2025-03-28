# app.py
from flask import Flask, render_template, jsonify
import psutil
import platform
import time

app = Flask(__name__)

def get_system_info():
    # CPU temperature (Linux only, for Windows/Mac this might not work)
    temps = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}
    cpu_temp = None
    if "coretemp" in temps:
        cpu_temp = temps["coretemp"][0].current

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

@app.route('/api/system')
def system_api():
    return jsonify(get_system_info())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
