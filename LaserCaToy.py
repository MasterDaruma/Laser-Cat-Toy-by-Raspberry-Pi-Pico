from machine import Pin, PWM
from utime import sleep
import urandom

def init_servo(pin):
    servo = PWM(Pin(pin))
    servo.freq(50)
    return servo

def set_servo_angle(servo, angle):
    duty = int(((angle / 180) * (6553 - 2457)) + 2457)
    servo.duty_u16(duty)

def calculate_new_angle(current_angle, velocity, angle_range):
    new_angle = current_angle + velocity
    if new_angle < angle_range[0] or new_angle > angle_range[1]:
        velocity = -velocity  # 反转方向
        new_angle = current_angle + velocity
    return new_angle, velocity

def run_laser_toy(pan_servo, tilt_servo, laser_pin, pan_range=(40, 140), tilt_range=(80, 120)):
    laser_pin.value(1)
    
    pan_angle, tilt_angle = 90, 100  # 初始角度
    pan_velocity, tilt_velocity = 2, 2  # 初始速度

    while True:
        pan_angle, pan_velocity = calculate_new_angle(pan_angle, pan_velocity + urandom.uniform(-1, 1), pan_range)
        tilt_angle, tilt_velocity = calculate_new_angle(tilt_angle, tilt_velocity + urandom.uniform(-1, 1), tilt_range)
        
        set_servo_angle(pan_servo, pan_angle)
        set_servo_angle(tilt_servo, tilt_angle)
        
        sleep(0.05)  # 短暂延时以实现更平滑的运动

# 定义引脚
PAN, TILT, LASER = 10, 11, 2
pan_servo = init_servo(PAN)
tilt_servo = init_servo(TILT)
laser = Pin(LASER, Pin.OUT)

run_laser_toy(pan_servo, tilt_servo, laser)
