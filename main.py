import uasyncio

from asyncserver.request import Request
from asyncserver.server import AsyncServer
from motor.servo import Servo
from utils.pin import PinNum

print('[starting]')
servo = Servo(PinNum.D7)
server = AsyncServer()

@server.route('/on')
async def on(r: Request):
    await servo.activate()
    return server.response(200, content='ON')

@server.route('/off')
async def off(r: Request):
    await servo.deactivate()
    return server.response(200, content='OFF')

@server.route('/move')
async def move(r: Request):
    await servo.deactivate()
    if 'angle' in r.args:
        await servo.angle(int(r.args['angle']))
        return server.response(200, content=f'ANGLE SET TO ' + r.args['angle'])
    return server.response(404)

@server.route('/servo')
async def servo_adjust(r: Request):
    if 'min' in r.args:
        servo._min_angle = int(r.args['min'])
    elif 'max' in r.args:
        servo._max_angle = int(r.args['max'])
    return server.response(200, content='SERVO ADJUSTED')

loop = uasyncio.get_event_loop()
loop.create_task(server.start())
loop.create_task(servo.start())

try: 
    loop.run_forever()
except Exception as e:
    print(f'[exception {e}]')
except KeyboardInterrupt:
    print('[stopping]')
    loop.close()
