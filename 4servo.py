
import telebot
import RPi.GPIO as GPIO
import time

TOKEN = '6207477097:AAHG08fCkb0Xgl9NRovbd43_YlODa4fjNBo'
SERVO_PINS = [11, 13, 15, 42]
PWM_FREQ = 50
MIN_DUTY_CYCLE = 2.5
MAX_DUTY_CYCLE = 12.5

bot = telebot.TeleBot(TOKEN)

def set_servo_angle(pin, angle):
    duty_cycle = MIN_DUTY_CYCLE + (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE) * angle / 180
    GPIO.output(pin, True)
    pwm = GPIO.PWM(pin, PWM_FREQ)
    pwm.start(duty_cycle)
    time.sleep(1)
    pwm.stop()
    GPIO.output(pin, False)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Use the /setangle command to set the angle of a servo motor.')

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

def main():
    GPIO.setmode(GPIO.BOARD)
    for pin in SERVO_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)
    bot.polling()

if __name__ == '__main__':
    main()

