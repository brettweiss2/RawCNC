from time import sleep
import RPi.GPIO as GPIO

class ring:
	def __init__(self):
		self.DIR = 20	# Direction Pin
		self.STEP = 21	# Step Pin
		self.SLEEP = 26	# Sleep Pin
		self.LIMIT = 17	# Limit Switch Pin
		self.MODE = (14,15,18) # Step Mode Pins

		self.RESOLUTION = (1,1,0) # 1/8 Step
		self.CW = 0		# Clockwise
		self.CCW = 1	# Counterclockwise
		self.stepsPerRing = 25333
		self.position = 0 # in steps

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.DIR, GPIO.OUT)
		GPIO.setup(self.STEP, GPIO.OUT)
		GPIO.setup(self.MODE, GPIO.OUT)
		GPIO.setup(self.SLEEP, GPIO.OUT)
		GPIO.setup(self.LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.output(self.DIR, self.CW)
		GPIO.output(self.MODE, self.RESOLUTION)
		self.home(self.CCW)

	def stepOne(self, slow=False):
		delay = .00025
		if slow:
			delay = .0007
		GPIO.output(self.STEP, GPIO.HIGH)
		sleep(delay)
		GPIO.output(self.STEP, GPIO.LOW)
		sleep(delay)

	def step(self, n, direction):
		GPIO.output(self.DIR, direction)
		GPIO.output(self.SLEEP, GPIO.HIGH)
		if n <= 100:
			for _ in range(n):
				self.stepOne(True)
		else:
			for _ in range(100):
				self.stepOne(True)
			for _ in range(n-100):
				self.stepOne()
		GPIO.output(self.SLEEP, GPIO.LOW)
		newPosition = self.position
		if direction:
			newPosition -= n
		else:
			newPosition += n
		newPosition %= self.stepsPerRing
		self.position = newPosition

	def goto(self, degree):
		move = self.position - self.degreeToPosition(degree % 360)
		if move == self.position:
			return
		direction = move > 0
		move = abs(move)
		if move > self.stepsPerRing/2:
			direction = not direction
			move = self.stepsPerRing/2 - move
		self.step(int(move), direction)

	def home(self, direction, done=False):
		GPIO.output(self.DIR, direction)
		GPIO.output(self.SLEEP, GPIO.HIGH)
		count = 0
		while GPIO.input(self.LIMIT) and count <= 100:
			self.stepOne(True)
			count += 1
		while GPIO.input(self.LIMIT):
			self.stepOne(done)
		GPIO.output(self.SLEEP, GPIO.LOW)
		if done:
			self.position = 0
			return
		if direction:
			self.step(500, self.CCW)
			sleep(0.2)
			self.home(self.CW, True)
		else:
			self.step(500, self.CW)
			sleep(0.2)
			self.home(self.CCW)

	def degreePosition(self):
		return self.position / self.stepsPerRing * 360

	def degreeToPosition(self, degree):
		return (degree / 360) * self.stepsPerRing

	def closest(self):
		return self.position < self.stepsPerRing / 2
