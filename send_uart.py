import argparse
import serial
import time
from datetime import datetime

INPUT_TIMEOUT = 10

def read_bytes(s):
	received_bytes = ''
	while s.in_waiting:
		received_bytes += s.read()
		time.sleep(.3)
	return received_bytes


def main(args):

	s = serial.Serial("/dev/ttyS0",
						baudrate = 9600,
						parity = serial.PARITY_NONE,
						stopbits = serial.STOPBITS_ONE,
						bytesize=serial.EIGHTBITS,
						timeout = 1)
	s.write(args.send +'\n')
	print('waiting for return bytes')
	start_time = datetime.now()
	while (datetime.now() - start_time).seconds < INPUT_TIMEOUT:
		time.sleep(.3)
		if s.in_waiting:
			print(read_bytes(s))
			break

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('send', help='string to send via. UART')
	args = parser.parse_args()
	main(args)
