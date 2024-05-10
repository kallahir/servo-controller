import uasyncio

from machine import Pin, PWM

class Servo:
    def __init__(self, pin_num, activated=True):
        self._servo = PWM(Pin(pin_num, Pin.OUT))
        self._servo.freq(50)
        self._servo.duty(0)
        self._min_angle = 115
        self._max_angle = 160
        self._interval = 0.5
        self._activated = activated

    async def angle(self, value):
        self._servo.duty(Servo.__map(value,0,180,20,125))

    async def activate(self):
        self._activated = True

    async def deactivate(self):
        self._activated = False 
    
    async def start(self):
        status = True
        while True:
            if self._activated:
                if status:
                    status = False
                    await self.angle(self._max_angle)
                else:
                    status = True
                    await self.angle(self._min_angle)
            await uasyncio.sleep(self._interval)

    def __map(x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
