import argparse
import serial
import time
import RPi.GPIO as GPIO
from datetime import datetime

INPUT_TIMEOUT = 10
MODE_PIN = 18

def gpio_setup():
	"""	This makes sure we're in BCM mode for addressing
		GPIO pins.
		It also makes sure that the pin we're using to set
		the mode is set as an output.
	"""
	if GPIO.getmode() != GPIO.BCM:
		GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(MODE_PIN, GPIO.OUT)

def set_mode(mode):
	"""	Input:
			mode: bool - if True, we will set the mode
				pin to command mode. If False, it will
				be set to UART mode.
		This sets the mode. While we're doing setup, it
		also checks to see that the GPIO mode is set to BCM.
	"""
	if not mode:
		print("UART Mode")
		GPIO.output(MODE_PIN, GPIO.LOW)
	else:
		print("Command Mode")
		GPIO.output(MODE_PIN, GPIO.HIGH)

def read_bytes(s):
	"""	Input:
			s: Serial.serial
		This takes bytes from Serial port and appends them to
		a string for as long as there are bytes waiting.
	"""
	received_bytes = ''
	while s.in_waiting:
		received_bytes += s.read().decode()
	return received_bytes

def get_serial():
	""" Returns a Serial.serial object, which lets us read from
		and write to the Bluefruit using UART
	"""
	s = serial.Serial("/dev/ttyS0",
						baudrate = 9600,
						timeout = INPUT_TIMEOUT)
	return s

def wait_for_reply(s):
	"""	Input:
			s: serial.Serial object
		Output:
			s
	This function waits INPUT_TIMEOUT seconds for a reply. Every
	.3 seconds it checks to see if it's received a response, if
	it has, it passes s to the read_bytes() function, prints
	the result, and returns.
	"""
	start_time = datetime.now()
	while (datetime.now() - start_time).seconds < INPUT_TIMEOUT:
		time.sleep(.3)
		if s.in_waiting:
			print(read_bytes(s))
			return s
	return s

def format_message(msg, cmd, key):
	"""	Inputs:
			msg: string - what message should we send?
			cmd: bool - are we in command mode?
			key: bool - are we in keyboard mode?
	"""
	if key:
		cmd = True
		msg = f'AT+BLEKEYBOARD={msg}'
	if cmd:
		msg = msg + '\r\n'
	return msg.encode(), cmd

def main(msg, mode):
	""" Input:
			msg: string - the message to be sent to the Bluefruit
				 module
			mode: if True, the message is sent in command mode
				  if False, the message is sent over UART
	"""
	# Setup
	gpio_setup()
	set_mode(mode)
	time.sleep(.3)
	s = get_serial()
	# Write message
	s.write(msg)
	wait_for_reply(s)
	# Cleanup
	GPIO.cleanup()
	s.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('send', help='string to send via. UART')
	parser.add_argument('-c', '--command', action='store_true', 
						help='run in command mode')
	parser.add_argument('-k', '--keyboard', action='store_true',
						help='send string over blehiden')
	args = parser.parse_args()
	msg, mode = format_message(args.send, args.command, args.keyboard)
	main(msg, mode)
