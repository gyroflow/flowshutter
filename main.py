from machine import Pin, UART, Timer
import crsf, oled, target, sony_multiport
import uasyncio as asyncio
from time import sleep

oled1 = oled.oled_init()

uart1, uart2, _, button1 = target.init_pins()
fc_arm_packet, fc_disarm_packet = crsf.init_packet()
record_press_packet, record_release_packet, camera_verify_packet, camera_verify_packet_ack, camera_recording_packet, camrea_recording_packet_ack = sony_multiport.init_multiport_packet()
# this part should be fixed in future, too ugly :(
def change_arm_flag():
    global arm_flag
    if arm_flag == 0:
        arm_flag = 1
        oled.show_arm_info(oled1)
    else:
        arm_flag = 0
        oled.show_disarm_info(oled1)

press_count = 0
def check_cmd(t):
    global press_count
    if button1.value() == 0:
        if press_count <=100:
            press_count += 1
        else:
            press_count = 0
            change_arm_flag()
    else:
        press_count = 0

timer0 = Timer(0)
timer0.init(period=5, mode=Timer.PERIODIC, callback=check_cmd)

arm_flag=0
def send_crsf_packet(t):
    global arm_flag
    if arm_flag == 1:
        uart1.write(fc_arm_packet)
    else:
        uart1.write(fc_disarm_packet)

timer1 = Timer(1)
timer1.init(period=4, mode=Timer.PERIODIC, callback=send_crsf_packet)


cam_press_frame = '#7100*' #ASCII is needed here
cam_release_frame = '#7110*'
test_button_flag = 0

async def sender():
    swriter = asyncio.StreamWriter(uart2, {})
    while True:
        await swriter.awrite('hhhh')
        await asyncio.sleep_ms(40)
        # never mind this, it's just for test, will be deleted soon

async def receiver():
    swriter = asyncio.StreamWriter(uart2, {})
    sreader = asyncio.StreamReader(uart2)
    while True:
        res = await sreader.read(n=-1)
        print('Cam sent:', res)
        if res == b'%000*':
            await asyncio.sleep_ms(10)
            await swriter.awrite(camera_verify_packet_ack)
        elif res == b'%7614*':
            await asyncio.sleep_ms(10)# I don't know if this timing is good, should look into it later
            await swriter.awrite(camrea_recording_packet_ack)

loop = asyncio.get_event_loop()
loop.create_task(sender())
loop.create_task(receiver())
loop.run_forever()
# def test_change_button_flag():
#     global test_button_flag
#     if test_button_flag == 0:
#         test_button_flag = 1
#         uart2.write(cam_press_frame)
#         oled.show_cam_press_info(oled1)
#     else:
#         test_button_flag = 0
#         uart2.write(cam_release_frame)
#         oled.show_cam_release_info(oled1)

# def test_check_button():
#     global press_count
#     if p19.value() == 0:
#         if press_count <=100:
#             press_count += 1
#         else:
#             press_count = 0
#             test_change_button_flag()