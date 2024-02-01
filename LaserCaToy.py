from machine import Pin, PWM
from utime import sleep
import urandom

def init_servo(pin):
    servo = PWM(Pin(pin))
    servo.freq(50)  # 设置PWM频率为50Hz，适合大多数舵机。
    return servo

def set_servo_angle(servo, angle):
    duty = int(((angle / 180) * (6553 - 2457)) + 2457)
    servo.duty_u16(duty)

def smooth_move(servo, current_angle, target_angle, steps=10):
    step_angle = (target_angle - current_angle) / steps
    for _ in range(steps):
        current_angle += step_angle
        set_servo_angle(servo, current_angle)
        sleep(0.02)  # 短暂延时以实现平滑移动

def run_laser_toy(pan_servo, tilt_servo, laser_pin, pan_range=(40, 140), tilt_range=(80, 120), pause_range=(100, 300)):
    laser_pin.value(1)  # 激活激光
    current_pan = 90
    current_tilt = 100

    while True:
        pan_target = current_pan + urandom.randint(-20, 20)  # 限制平移位移距离
        tilt_target = current_tilt + urandom.randint(-20, 20)  # 限制倾斜位移距离
        
        # 确保目标角度在有效范围内
        pan_target = max(min(pan_target, pan_range[1]), pan_range[0])
        tilt_target = max(min(tilt_target, tilt_range[1]), tilt_range[0])
        
        # 平滑移动到目标角度
        smooth_move(pan_servo, current_pan, pan_target)
        smooth_move(tilt_servo, current_tilt, tilt_target)
        
        # 更新当前角度
        current_pan = pan_target
        current_tilt = tilt_target
        
        # 随机暂停时间
        pause_time = urandom.randint(*pause_range) / 1000.0
        sleep(pause_time)

# 定义引脚
PAN, TILT, LASER = 10, 11, 2
pan_servo = init_servo(PAN)
tilt_servo = init_servo(TILT)
laser = Pin(LASER, Pin.OUT)

# 运行逗猫玩具
run_laser_toy(pan_servo, tilt_servo, laser)
