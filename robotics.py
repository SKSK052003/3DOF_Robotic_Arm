import telebot
import RPi.GPIO as GPIO
import time

TOKEN = '6207477097:AAHG08fCkb0Xgl9NRovbd43_YlODa4fjNBo'
SERVO_PIN = 11
PWM_FREQ = 50
MIN_DUTY_CYCLE = 2.5
MAX_DUTY_CYCLE = 12.5

bot = telebot.TeleBot(TOKEN)

def set_servo_angle(angle):
    duty_cycle = MIN_DUTY_CYCLE + (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE) * angle / 180
    GPIO.output(SERVO_PIN, True)
    pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
    pwm.start(duty_cycle)
    time.sleep(1)
    pwm.stop()
    GPIO.output(SERVO_PIN, False)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Use the /setangle command to set the angle of the servo motor.')

@bot.message_handler(commands=['setangle'])
def setangle(message):
    try:
        angle = int(message.text.split()[1])
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, 'Usage: /setangle angle')
        return
    if angle < 0 or angle > 180:
        bot.send_message(message.chat.id, 'Angle must be between 0 and 180 degrees.')
        return
    set_servo_angle(angle)
    bot.send_message(message.chat.id, 'Set angle to {} degrees.'.format(angle))

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.output(SERVO_PIN, False)
    bot.polling()

if __name__ == '__main__':
    main()

