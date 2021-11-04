import RPi.GPIO as GPIO       
import time

led = 21                       # the GPIO pin 21 for LED
trigger = 18                   # the GPIO pin 18 for HC-SR04 trigger pin
echo = 24                      # the GPIO pin 24 for HC-SR04 echo pin


GPIO.setmode(GPIO.BCM)      

GPIO.setup(led, GPIO.OUT)     
GPIO.setup(trigger, GPIO.OUT)  
GPIO.setup(echo, GPIO.IN)     


pwm = GPIO.PWM(led, 100)      
pwm.start(0)                   # Start PWM at 0% duty cycle (off)

def distance():

    GPIO.output(trigger, True) # set Trigger to HIGH

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    Start = time.time()
    Stop = time.time()

    # recprd the  StartTime
    while GPIO.input(echo) == 0:
        Start = time.time()

    # save time of arrival
    while GPIO.input(echo) == 1:
        Stop = time.time()

    TimeElapsed = Stop - Start
    # multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

try:
    while 1:                     # Loop will until interrupted

        dist = distance()
        print ("Measured Distance = %.1f cm" % dist) # print the distance so we can check the behaviour

        if (dist > 400):         # 400cm is the range of the sensor
            x = 0                # 0 is 'off', when the distance is greater than the range of the sensor we want it to appear off
        else:
            x = 100 - (dist / 4) # 100 is fully 'on', want the led to get brighter as the object becomes closer
                                 # divide by 4 as the range is 400 and we want the brightness to change between 0 and 100 over 400cm

        pwm.ChangeDutyCycle(x)   # Change duty cycle
        time.sleep(0.01)         # Delay of 10mS

# If keyboard Interrupt (CTRL-C) is pressed
except KeyboardInterrupt:
    pass        # Go to next line
pwm.stop()      # Stop the PWM
GPIO.cleanup()  # Make all the output pins LOW
