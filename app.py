import RPi.GPIO as GPIO
import mq7module as MQ7
import bh1750module as BH
import threading 
from flask import Flask, render_template, request
from time import sleep

import function
from werkzeug.serving import run_simple

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)

ledYellow = GPIO.PWM(12, 1000)
ledYellow.start(0)
value = 0
ledRed = 26
ledRedSts = 0
ledAlarm = 21
relay = 19
relaySts = 0
mq7SetValue = 0
mq7Analog = 0
bh1750 = 0
stat = "out"        
function.setPin(ledRed, stat)
function.setPin(relay, stat)
function.setPin(ledAlarm, stat) 


@app.route('/')
def index():  
    global mq7Analog  
    ledREDSts = GPIO.input(ledRed)
    relaySts = GPIO.input(relay)
    templateData = { 'ledRed' : ledRedSts, 'relay' : relaySts, "submitValue" : value, "mq7Value" : mq7Analog}
    return render_template('index.html', **templateData)
@app.route('/checkBox', methods=["POST"])
def checkBox():
    print("jestem")
    data = request.form["check"]
    print(data)
    templateData = { 'ledRed' : ledRedSts, 'relay' : relaySts, "submitValue" : value, "mq7Value" : mq7Analog}
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
    templateData = { 'ledRed' : ledRedSts, 'relay' : relaySts, "submitValue" : value, "mq7Value" : mq7Analog }
    return render_template('index.html', **templateData )
@app.route('/<read>')
def readMq7(read):
    if read == "readFromMq7":
             templateData = { 'ledRed' : ledRedSts, 'relay' : relaySts, "submitValue" : value, "mq7Value" : mq7Analog }
    return render_template('index.html', **templateData )
        
@app.route('/setValue', methods=['POST'])
def setAlarmValue():
    global mq7SetValue
    mq7SetValue = int(request.form['text'])
    templateData = { 'ledRed' : ledRedSts, 'relay' : relaySts, "submitValue" : value, "mq7Value" : mq7Analog }
    return render_template('index.html', **templateData )
def mh():
    while True:
        BH.main()
        sleep(2)
def modules():
    while 1:
        MQ7.main()
        global mq7Analog
        mq7Analog = MQ7.output
        if mq7Analog > mq7SetValue:
            GPIO.output(ledAlarm, GPIO.HIGH)
        else:
            GPIO.output(ledAlarm, GPIO.LOW)
        sleep(2)
      
if __name__ == '__main__':
    thread1 = threading.Thread(target = modules)
    thread2 = threading.Thread(target = mh)
    thread2.start()
    thread1.start()
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    
    
 
    
   
