import RPi.GPIO as GPIO
import mq7module as MQ7
from threading import Thread
from flask import Flask, render_template, request
import function
from werkzeug.serving import run_simple

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)

ledYellow = GPIO.PWM(14, 9000)
ledYellow.start(0)
value = 0
ledRed = 26
ledRedSts = 0
ledAlarm = 21;
relay = 19
relaySts = 0


stat = "out"        
function.setPin(ledRed, stat)
function.setPin(relay, stat)
function.setPin(ledAlarm, stat) 


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
    thread1 = Thread(target = MQ7.Main)
    thread1.start()
    app.run(debug=True, host='0.0.0.0', port=5000)
    
  
    
    
 
    
   
