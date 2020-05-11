import time
from machine import Pin, I2C
from servo import Servos
i2c = I2C(sda=Pin(26), scl=Pin(25), freq=10000)
servos = Servos(i2c, address=0x40)
# HC-SR04超声波模块测距原理是：给模块1个最少10us的高电平，模块接受到高电平后开始发射8个40KHz的声波，
# echo脚会由0变为1,MCU开始计时，当超声波模块接收到返回的声波时，echo由1变为0,MCU停止计时，
# 这时间差就是测距总时间，在乘声音的传播速度340米/秒，除2就是距离。

# 定义IO口模式，以及初始状态
trig = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN)
led = Pin(2, Pin.OUT)
trig.off()
echo.off()
onOff = 'off'

# 构建函数
def juli():
    # 触发HC-SR04超声波模块测距
    trig.on()
    time.sleep_us(10)
    trig.off()
    # 检测回响信号，为低时，测距完成
    while (echo.value() == 0):
        # 开始不断递增的微秒计数器 1
        t1 = time.ticks_us()
    # 检测回响信号，为高时，测距开始
    while (echo.value() == 1):
        # 开始不断递增的微秒计数器 2
        t2 = time.ticks_us()
    # 计算两次调用 ticks_ms(), ticks_us(), 或 ticks_cpu()之间的时间，这里是ticks_us()
    t3 = time.ticks_diff(t2, t1) / 10000
    # 返回一个值给调用方，不带表达式的return相当于返回 None。
    # 这里返回的是：开始测距的时间减测距完成的时间*声音的速度/2（来回）
    return t3 * 340 / 2

def open():
    for i in range(10, 170):
        servos.position(0, i)
        time.sleep_ms(10)

def close():
    for i in range(170, 10, -1):
        servos.position(0, i)
        time.sleep_ms(10)

# try/except语句用来检测try语句块中的错误，从而让except语句捕获异常信息并处理
# 判断状态是否为关，
#   如果为关，检测距离小于10cm，
#       执行打开舵机停留170度，将状态改为开
#   如果为关，检测距离大于10cm
#       将状态改为关，舵机为10度
#   如果为开，检测距离小于10cm
#       舵机停留170度，状态为开
#   如果为开，检测距离大于10cm
#       执行关闭舵机停留10度，状态改为关
try:
    while 1:
        # print("JuLi:%0.2f cm" % fasong())
        if (onOff == 'off'):
            if (juli() < 10):
                led.value(1)
                open()
                servos.position(170)
                onOff = 'on'
            else:
                servos.position(10)
                onOff = 'off'
        else:
            if (juli() < 10):
                servos.position(170)
                onOff = 'on'
            else:
                time.sleep(5)
                led.value(0)
                close()
                onOff = 'off'

except KeyboardInterrupt:
    pass
