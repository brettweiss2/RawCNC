#this is completely untested
from time import sleep
import RPi.GP as GPIO
import config

class motor:
	def __init__(self):
		self.DIR = config.DIR
		self.STEP = config.STEP
		self.SPR = config.SPR
		self.LIM = config.LIM
		self.defaultRPS = config.defaultRPS
		self.stepsPerRing = config.stepsPerRing
		self.ringPosition = 0 #in steps

		GPIO.setmode(GPIO.BCM)		# BroadCOM memory
		GPIO.setup(self.DIR, GPIO.OUT)	# Set Direction pin as output
		GPIO.setup(self.STEP, GPIO.OUT)	# Set Direction pin as output
		GPIO.setup(self.DIR, GPIO.IN)#Set Limit Switch pin as input
		GPIO.output(DIR, 1)

		self.resetRing()

	def rotate(self, direcrtion, steps, rps):
		GPIO.output(self.DIR, direcrtion)
		delay = 1/(2*self.SPR*rps)
		for x in range(steps):
			GPIO.output(self.STEP, 1)
			sleep(delay)
			GPIO.output(self.STEP, 0)
			sleep(delay)
		
		if direction:
			self.ringPosition = (self.ringPosition + steps) % 1000
		else:
			self.ringPosition = (self.ringPosition - steps) % 1000

	def resetRing():
		GPIO.output(self.DIR, 0)
		delay = 1/(2*self.defaultRPS)
		while(not GPIO.input(self.LIM)):
			GPIO.output(self.STEP, 1)
			sleep(delay)
			GPIO.output(self.STEP, 0)
			sleep(delay)
		self.ringPosition = 0