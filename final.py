
import telebot
import RPi.GPIO as GPIO
import time

TOKEN = '6207477097:AAHG08fCkb0Xgl9NRovbd43_YlODa4fjNBo'
SERVO_PINS = [18, 22, 24, 26]
PWM_FREQ = 50
MIN_DUTY_CYCLE = 2.5
MAX_DUTY_CYCLE = 12.5
MOTOR_PINS = [12, 16, 19, 23]
STEP_DELAY = 0.05

bot = telebot.TeleBot(TOKEN)

def set_servo_angle(pin, angle):
    duty_cycle = MIN_DUTY_CYCLE + (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE) * angle / 180
    GPIO.output(pin, True)
    pwm = GPIO.PWM(pin, PWM_FREQ)
    pwm.start(duty_cycle)
    time.sleep(1)
    pwm.stop()
    GPIO.output(pin, False)

def move_forward(steps):
    GPIO.output(MOTOR_PINS[0], True)
    GPIO.output(MOTOR_PINS[1], False)
    GPIO.output(MOTOR_PINS[2], True)
    GPIO.output(MOTOR_PINS[3], False)
    for _ in range(steps):
        time.sleep(STEP_DELAY)
        GPIO.output(MOTOR_PINS[0], False)
        GPIO.output(MOTOR_PINS[1], True)
        GPIO.output(MOTOR_PINS[2], True)
        GPIO.output(MOTOR_PINS[3], False)
        time.sleep(STEP_DELAY)
        GPIO.output(MOTOR_PINS[0], True)
        GPIO.output(MOTOR_PINS[1], False)
        GPIO.output(MOTOR_PINS[2], True)
        GPIO.output(MOTOR_PINS[3], False)
    GPIO.output(MOTOR_PINS[0], False)
    GPIO.output(MOTOR_PINS[1], False)
    GPIO.output(MOTOR_PINS[2], False)
    GPIO.output(MOTOR_PINS[3], False)

def move_backward(steps):
    GPIO.output(MOTOR_PINS[0], False)
    GPIO.output(MOTOR_PINS[1], True)
    GPIO.output(MOTOR_PINS[2], False)
    GPIO.output(MOTOR_PINS[3], True)
    for _ in range(steps):
        time.sleep(STEP_DELAY)
        GPIO.output(MOTOR_PINS[0], True)
        GPIO.output(MOTOR_PINS[1], False)
        GPIO.output(MOTOR_PINS[2], False)
        GPIO.output(MOTOR_PINS[3], True)
        time.sleep(STEP_DELAY)
        GPIO.output(MOTOR_PINS[0], False)
        GPIO.output(MOTOR_PINS[1], True)
        GPIO.output(MOTOR_PINS[2], False)
        GPIO.output(MOTOR_PINS[3], True)
    GPIO.output(MOTOR_PINS[0], False)
    GPIO.output(MOTOR_PINS[1], False)
    GPIO.output(MOTOR_PINS[2], False)
    GPIO.output(MOTOR_PINS[3], False)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Use the /setangle command to set the angle of a servo motor, or the /forward or /backward command to move the robot forward or backward.')

@bot.message_handler(commands=['setangle'])
def setangle(message):
    try:
        servo_pin, angle = map(int, message.text.split()[1:])
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, 'Usage: /setangle pin angle')
        return
    if servo_pin not in SERVO_PINS or angle < 0 or angle > 180:
        bot.send_message(message.chat.id, 'Invalid servo pin or angle.')
        return
    set_servo_angle(servo_pin, angle)
    bot.send_message(message.chat.id, 'Set angle of pin {} to {}.'.format(servo_pin, angle))
@bot.message_handler(commands=['forward'])
def forward(message):
    try:
        steps = int(message.text.split()[1])
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, 'Usage: /forward steps')
        return
    move_forward(steps)
    bot.send_message(message.chat.id, f'Moved forward {steps} steps')

@bot.message_handler(commands=['backward'])
def backward(message):
    try:
        steps = int(message.text.split()[1])
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, 'Usage: /backward steps')
        return
    move_backward(steps)
    bot.send_message(message.chat.id, f'Moved backward {steps} steps')


def main():
    GPIO.setmode(GPIO.BOARD)
    for pin in SERVO_PINS:
        GPIO.setup(pin, GPIO.OUT)
    for pin in MOTOR_PINS:
        GPIO.setup(pin, GPIO.OUT)
    bot.polling()
    
if __name__ == '__main__':
    main()
    
    







