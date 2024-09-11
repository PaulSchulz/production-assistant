from flask import Flask, render_template, request
import subprocess
import socket # Used to get hostname

from yamldb import YamlDB    # Configuration and Data DB

db = YamlDB(filename="data/db.yaml")

app = Flask(__name__)

main_title = "Production Assistant"
main_content = "Device Details"
hostname = socket.gethostname()

@app.route('/', methods=['GET','POST'])
def home():
    title = main_title
    data = db
    return render_template('index.html', hostname=hostname, title=title, data=data)

@app.route('/setup', methods=['GET'])
def setup_get():
    title = main_title+" (GET)"
    data = db
    return render_template('setup.html', hostname=hostname, title=title, data=data)

@app.route('/setup', methods=['POST'])
def setup_post():
    title = main_title+" (POST)"
    db["device"]   = request.form.get("device")
    db["customer"] = request.form.get("customer")
    db["site"]     = request.form.get("site")
    db["comment"]  = request.form.get("comment")
    db.save()
    data = db
    result = "Saved"
    return render_template('setup.html', hostname=hostname, title=title, data=data, result=result)

@app.route('/programming')
def programming():
    title = main_title
    data = {}
    return render_template('programming.html', hostname=hostname, title=title, data=data)

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
    data = db

    # Run your Python script here
    result = run_status_script()
    # Render the template with the result
    return render_template('index.html',
                           hostname=hostname,
                           title=main_title,
                           result=result,
                           data=data)

def run_status_script():
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
