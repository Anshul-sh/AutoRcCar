import RPi.GPIO as GPIO
import socket
import io


class Motor:

	def __init__(self, pinForward, pinBackward, pinControlStraight,pinLeft, pinRight, pinControlSteering):
		""" Initialize the motor with its control pins and start pulse-width
			 modulation """
		
		turn = 50

		self.pinForward = pinForward
		self.pinBackward = pinBackward
		self.pinControlStraight = pinControlStraight
		self.pinLeft = pinLeft
		self.pinRight = pinRight
		self.pinControlSteering = pinControlSteering
		GPIO.setup(self.pinForward, GPIO.OUT)
		GPIO.setup(self.pinBackward, GPIO.OUT)
		GPIO.setup(self.pinControlStraight, GPIO.OUT)

		GPIO.setup(self.pinLeft, GPIO.OUT)
		GPIO.setup(self.pinRight, GPIO.OUT)
		GPIO.setup(self.pinControlSteering, GPIO.OUT)

		self.pwm_forward = GPIO.PWM(self.pinForward, 100)
		self.pwm_backward = GPIO.PWM(self.pinBackward, 100)
		self.pwm_forward.start(0)
		self.pwm_backward.start(0)

		self.pwm_left = GPIO.PWM(self.pinLeft, turn)
		self.pwm_right = GPIO.PWM(self.pinRight, turn)
		self.pwm_left.start(0)
		self.pwm_right.start(0)

		GPIO.output(self.pinControlStraight,GPIO.HIGH) 
		GPIO.output(self.pinControlSteering,GPIO.HIGH) 

	def forward(self, speed):
		""" pinForward is the forward Pin, so we change its duty
			 cycle according to speed. """
		self.pwm_backward.ChangeDutyCycle(0)
		self.pwm_forward.ChangeDutyCycle(speed)    

	def forward_left(self, speed):
		""" pinForward is the forward Pin, so we change its duty
			 cycle according to speed. """
		self.pwm_backward.ChangeDutyCycle(0)
		self.pwm_forward.ChangeDutyCycle(speed)  
		self.pwm_right.ChangeDutyCycle(0)
		self.pwm_left.ChangeDutyCycle(turn)   

	def forward_right(self, speed):
		""" pinForward is the forward Pin, so we change its duty
			 cycle according to speed. """
		self.pwm_backward.ChangeDutyCycle(0)
		self.pwm_forward.ChangeDutyCycle(speed)
		self.pwm_left.ChangeDutyCycle(0)
		self.pwm_right.ChangeDutyCycle(turn)

	def backward(self, speed):
		""" pinBackward is the forward Pin, so we change its duty
			 cycle according to speed. """

		self.pwm_forward.ChangeDutyCycle(0)
		self.pwm_backward.ChangeDutyCycle(speed)
		
	def backward_left(self, speed):
		""" pinForward is the forward Pin, so we change its duty
			 cycle according to speed. """
		self.pwm_backward.ChangeDutyCycle(speed)
		self.pwm_forward.ChangeDutyCycle(0)  
		self.pwm_right.ChangeDutyCycle(0)
		self.pwm_left.ChangeDutyCycle(turn)   

	def backward_right(self, speed):
		""" pinForward is the forward Pin, so we change its duty
			 cycle according to speed. """
		self.pwm_backward.ChangeDutyCycle(speed)
		self.pwm_forward.ChangeDutyCycle(0)
		self.pwm_left.ChangeDutyCycle(0)
		self.pwm_right.ChangeDutyCycle(turn)

	def left(self, speed):
		""" pinForward is the forward Pin, so we change its duty
			 cycle according to speed. """
		self.pwm_right.ChangeDutyCycle(0)
		self.pwm_left.ChangeDutyCycle(turn)  

	def right(self, speed):
		""" pinForward is the forward Pin, so we change its duty
			 cycle according to speed. """
		self.pwm_left.ChangeDutyCycle(0)
		self.pwm_right.ChangeDutyCycle(turn)   

	def stop(self):
		""" Set the duty cycle of both control pins to zero to stop the motor. """

		self.pwm_forward.ChangeDutyCycle(0)
		self.pwm_backward.ChangeDutyCycle(0)
		self.pwm_left.ChangeDutyCycle(0)
		self.pwm_right.ChangeDutyCycle(0)


if __name__ == '__main__':
	host="192.168.2.101"
	driving_port=8013

	ss_drive = socket.socket()
	ss_drive.bind((host, driving_port))

	ss_drive.listen(1)

	con, client_add = ss_drive.accept()#[0].makefile('rb')

	host_name = socket.gethostname()
	host_ip = socket.gethostbyname(host_name)

	print("Host: ", host_name + ' ' + host_ip)
	print("con from: ", client_add)
	
	
	
	
	while True:
			print("Connection done")
			#Create motor object
			GPIO.setmode(GPIO.BOARD)
			motor = Motor(31, 29, 37, 35, 33, 37)

			try:
                            while True:
							
				key = con.recv(1024).decode()
				print("Key input recv : ", key)
				
				speed =100
				turn = 50
				
				
				#key_input = pygame.key.get_pressed()

				# complex orders
				
				if key == "6" :
					print("Forward Right")
					motor.forward_right(speed)

				elif key == "7":
					print("Forward Left")
					motor.forward_left(speed)

				elif key == "8":
					print("Reverse Right")
					motor.backward_right(speed)

				elif key == "9":
					print("Reverse Left")
					motor.backward_left(speed)

				# simple orders
				elif key == "1":
					print("Forward")
					motor.forward(speed)
					

				elif key == "2":
					print("Reverse")
					motor.backward(speed)

				elif key == "3":
					print("Right")
					motor.right(speed)

				elif key == "4":
					print("Left")
					motor.left(speed)
					
				elif key == "0":
					print("stop")
					motor.stop()
					
				elif key == "11":
					print("Exit")
					motor.stop()
					break
				else:
					print("stop")
					motor.stop()
				#	break

			finally:
		
                            con.close()
