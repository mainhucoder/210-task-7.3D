import RPi.GPIO as GPIO
import time

send_pulse = 18  #Pin for sending signal to sensor
receive_pulse = 22  #Pin for receiving signal from sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)      #GPIO pin for controlling LED
GPIO.setup(send_pulse, GPIO.OUT)  
GPIO.setup(receive_pulse, GPIO.OUT)  


led = GPIO.PWM(17, 600)  #Initialize PWM on pin 17 with frequency of 600Hz
led.start(0) #This will make the LED start with 0 brightness

#Function for measuring distance using the sensor
def dist_monitor():
    GPIO.output(send_pulse, True) #Send a pulse to trigger the sensor
    time.sleep(0.002)
    GPIO.output(send_pulse, False)
    pulse_start = time.time()  #Tells time when the sensor sends the pulse
    pulse_end = time.time()

    while GPIO.input(receive_pulse) == 0: #Check time it takes for the sensor to receive the pulse back
        pulse_start = time.time()
    while GPIO.input(receive_pulse) == 1:
        pulse_end = time.time()

    #Calculate the duration of pulse
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  
    return distance

#Monitor and control the LED on basis of distance
while True:
    distance = dist_monitor()

    # Map the distance to LED brightness (0% to 100%)
    brightness = max(0, min(100, int(100 - (distance / 10))))
    led.ChangeDutyCycle(brightness)  #Adjust LED brightness on basis of distance
    time.sleep(0.1)  #Wait for given time before the next measurement takes place
