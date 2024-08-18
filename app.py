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
    content = main_content
    return render_template('index.html', hostname=hostname, title=title, content=content)

@app.route('/esp-status', methods=['POST'])
def run_script():
    # Run your Python script here
    result = run_script()

    # Render the template with the result
    return render_template('index.html',
                           hostname=hostname,
                           title=main_title,
                           content="Details of ESP Device",
                           result=result)

def run_script():
    # Run the Bash script and capture the output
    result = subprocess.run(['./bin/esp-status.py'],
                            capture_output=True,
                            text=True,
                            shell=True)

    # Capture the stdout from the script
    output = result.stdout.strip()

    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True)
