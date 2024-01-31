from machine import Pin, PWM
from utime import sleep
import urandom

def init_servo(pin):

    servo = PWM(Pin(pin))
    servo.freq(50)  # 设置PWM频率为50Hz，适合大多数舵机。
    return servo

def set_servo_angle(servo, angle):

    duty = int(((angle / 180) * (6553 - 2457)) + 2457)  # 调整PWM脉冲宽度
    servo.duty_u16(duty)

def run_laser_toy(pan_servo, tilt_servo, laser_pin, pan_range=(40, 140), tilt_range=(80, 120), pause_range=(300, 800)):

    laser_pin.value(1)  # 激活激光

    while True:
        # 随机选择平移和倾斜的目标角度，以及暂停时间
        pan_angle = urandom.randint(*pan_range)
        tilt_angle = urandom.randint(*tilt_range)
        pause_time = urandom.randint(*pause_range) / 1000.0
        
        # 调整舵机角度并暂停
        set_servo_angle(pan_servo, pan_angle)
        set_servo_angle(tilt_servo, tilt_angle)
        sleep(pause_time)

# 定义引脚(需要根据实际接线情况填写GPIO引脚编号)
PAN, TILT, LASER = 10, 11, 2
pan_servo = init_servo(PAN)
tilt_servo = init_servo(TILT)
laser = Pin(LASER, Pin.OUT)

# 运行逗猫玩具
run_laser_toy(pan_servo, tilt_servo, laser)
