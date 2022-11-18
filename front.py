import RPi.GPIO  as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
print("Distance Measurement In Progress")
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

print("Waiting For Sensor To Settle")

time.sleep(2)
GPIO.output(TRIG, True)

time.sleep(0.00001)

GPIO.output(TRIG, False)
while GPIO.input(ECHO)==0:
  pulse_start=time.time()
while GPIO.input(ECHO)==1:

  pulse_end = time.time()    
pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150
distance = round(distance, 2)


if distance < 10:
   db=1
else:
   db=0;
print(db)
if db==1:
    import cv2
    import imutils
    import RPi.GPIO as GPIO
    import time
    from gpiozero import DistanceSensor, TonalBuzzer
    from gpiozero.tones import Tone
    from time import sleep

    uds = DistanceSensor(trigger=21, echo=20)
    buzzer = TonalBuzzer(16, octaves=3)

    servoPIN = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 21 for PWM with 50Hz
    p.start(2.5) # Initialization

    def distance_to_tone(distance_value):
        min_tone = buzzer.min_tone.midi
        max_tone = buzzer.max_tone.midi
        tone_range = max_tone - min_tone
        return min_tone + int(tone_range * distance_value)


    while True:
        distance_value = uds.distance
        tone = distance_to_tone(distance_value)
        buzzer.play(Tone(midi=tone))
        sleep(0.01)
   
        print ("Waiting for 1 second")
        time.sleep(1)
        print ("Rotating at intervals of 12 degrees")
        duty = 2
   
        if distance_value <=5:
       
            while duty <= 7:
                p.ChangeDutyCycle(duty)
                time.sleep(1)
                duty = duty + 1

            print ("Turning back to 0 degrees")
            p.ChangeDutyCycle(2)
            time.sleep(1)
            p.ChangeDutyCycle(0)

            p.stop()

GPIO.cleanup()
