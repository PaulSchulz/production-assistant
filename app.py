from flask import Flask, render_template
import subprocess
import socket # Used to get hostname

app = Flask(__name__)

main_title = "Production Assistant"
main_content = "Device Details"
hostname = socket.gethostname()

@app.route('/')
def home():
    title = main_title
    return render_template('index.html', hostname=hostname, title=title)

@app.route('/repos')
def repos():
    title = main_title
    data = {}
    return render_template('repos.html', hostname=hostname, title=title, data=data)

@app.route('/devices')
def devices():
    title = main_title
    data = {}
    return render_template('devices.html', hostname=hostname, title=title, data=data)

@app.route('/units')
def units():
    title = main_title
    data = {}
    data = get_units();
    return render_template('units.html', hostname=hostname, title=title, data=data)

@app.route('/about')
def about():
    title = main_title
    data = {}
    return render_template('about.html', hostname=hostname, title=title, data=data)


@app.route('/esp-status', methods=['POST'])
def run_script():
    data = {}

    # Run your Python script here
    result = run_script()
    # Render the template with the result
    return render_template('index.html',
                           hostname=hostname,
                           title=main_title,
                           result=result,
                           data={})

def run_script():
    # Run the Bash script and capture the output
    result = subprocess.run(['./bin/esp-status.py'],
                            capture_output=True,
                            text=True,
                            shell=True)

    # Capture the stdout from the script
    output = result.stdout.strip()

    return output

def get_units():
    data = {"headers": ["id", "name", "description", "customer", "date"],
            "headers_str": {
                "id": "Id",
                "name": "Name",
                "description": "Description",
                "customer": "Customer",
                "date": "Date"},
            "data": [
                {"id": "receiver-abcdef",
                 "name": "receiver",
                 "description": "Receiver Unit for Inverter",
                 "customer": "V3G Internal",
                 "date": "(now)"}
            ]
    }

    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True)
