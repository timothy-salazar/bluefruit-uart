import argparse
import serial
import time
import RPi.GPIO as GPIO
from datetime import datetime

INPUT_TIMEOUT = 10
MODE_PIN = 18

def read_bytes(s):
	received_bytes = ''
	while s.in_waiting:
		received_bytes += s.read()
	return received_bytes

def set_mode(mode):
	if GPIO.getmode() != GPIO.BCM:
		GPIO.setmode(GPIO.BCM)
	if GPIO.gpio_function(MODE_PIN) == GPIO.OUT:
		return
	GPIO.setup(MODE_PIN, GPIO.OUT)
	if not mode:
		print("UART Mode")
		GPIO.output(MODE_PIN, GPIO.LOW)
	else:
		print("Command Mode")
		GPIO.output(MODE_PIN, GPIO.HIGH)



def main(mode,msg):
	set_mode(mode)
	time.sleep(.3)
	s = serial.Serial("/dev/ttyS0",
						baudrate = 9600,
						timeout = INPUT_TIMEOUT)
	s.write(msg+'\r\n')
	print('> '+msg)
	print('waiting for return bytes')
	start_time = datetime.now()
	while (datetime.now() - start_time).seconds < INPUT_TIMEOUT:
		time.sleep(.3)
		if s.in_waiting:
			print(read_bytes(s))
			break
	GPIO.cleanup()
	s.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('send', help='string to send via. UART')
	parser.add_argument('-c', '--command', action='store_true', 
						help='run in command mode')
	args = parser.parse_args()
	main(args.command, args.send)
