import RPi.GPIO as GPIO     
import time

GPIO.setmode(GPIO.GROUND)  
GPIO.setup(led, GPIO.OUT)      
GPIO.setup(trigger, GPIO.OUT)  
GPIO.setup(echo, GPIO.IN)     


led = 40                
trigger = 12                
echo = 18 

pwm = GPIO.PWM(led, 100)       
pwm.start(0)                 

def distance():

    GPIO.output(trigger, True) 
    time.sleep(0.01)
    GPIO.output(trigger, False)

    Start = time.time()
    Stop = time.time()

    while GPIO.input(echo) == 0:
        Start = time.time()
    while GPIO.input(echo) == 1:
        Stop = time.time()

    Timetaken = Stop - Start
    distance = (Timetaken * 34300) / 2
    return distance

try:
    while 1:                    

        dist = distance()
        print (" Distance = %.1f cm" % dist)         
       if(dist > 40):
          pwm.ChangeDutyCycle(30)
          time.sleep(2)
       elif(dist > 25 and dist <40):
          pwm.ChangeDutyCycle(60)
          time.sleep(2)
       elif(dist > 15 and dist <25):
          pwm.ChangeDutyCycle(100) 
          time.sleep(2)
       else:
          pwm.ChangeDutyCycle(20)
          time.sleep(2)


except KeyboardInterrupt:
    pwm.stop()    
    GPIO.cleanup()  
