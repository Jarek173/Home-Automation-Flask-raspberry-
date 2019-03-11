import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import function
import time
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)

ledYellow = GPIO.PWM(14, 2000)
ledYellow.start(0)
value = 0;
ledRed = 26
ledRedSts = 0;
relay = 19;
relaySts = 0;

stat = "out"        
function.setPin(ledRed, stat)
function.setPin(relay, stat)    

 


@app.route('/')
def index():    
    ledREDSts = GPIO.input(ledRed)
    relaySts = GPIO.input(relay)
    templateData = { 'ledRed' : ledRedSts, 'relay' : relaySts, "submitValue" : value}
    return render_template('index.html', **templateData)

@app.route("/getValue", methods=["POST"])
def getValue():
    slider = request.form["slider"]
    value = float(slider)
    print(value)
    ledYellow.ChangeDutyCycle(value)
    templateData = { 'ledRed' : ledRedSts, 'relay' : relaySts, "submitValue" : value}
    return render_template('index.html', **templateData)
    
@app.route('/<deviceName>/<action>')
def do(deviceName, action):
    if deviceName == "ledRed":
        actuator = ledRed
    if deviceName == "relay":
        actuator = relay;
    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)
    
    ledRedSts = GPIO.input(ledRed)
    relaySts = GPIO.input(relay)
    templateData = { 'ledRed' : ledRedSts, 'relay' : relaySts, "submitValue" : value }
    return render_template('index.html', **templateData )

if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0', port=5000)
