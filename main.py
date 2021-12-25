from machine import Pin, UART, Timer
import crsf, oled, target, sony_multiport
import uasyncio as asyncio
from time import sleep

oled1 = oled.oled_init()

uart1, uart2, _, button1, button2 = target.init_pins()
fc_arm_packet, fc_disarm_packet = crsf.init_packet()
rcd_prs, rcd_rls, cm_hdsk, cm_hdsk_ack, cm_rcd_hb, cm_rcd_hb_ack = sony_multiport.init_multiport_packet()
# this part should be fixed in future, too ugly :(

button1_flag = 0
button2_flag = 0

def change_button1_flag():
    global button1_flag
    if button1_flag == 0:
        button1_flag = 1
        print('button1 tiggered')
    else:
        button1_flag = 0

def change_button2_flag():
    global button2_flag
    if button2_flag == 0:
        button2_flag = 1
        print('button2 tiggered')
    else:
        button2_flag = 0


def change_arm_flag():
    global arm_flag
    if arm_flag == 0:
        arm_flag = 1
        oled.show_arm_info(oled1)
    else:
        arm_flag = 0
        oled.show_disarm_info(oled1)

button1_press_count = 0
button2_press_count = 0
def check_cmd(t):
    global button1_press_count
    global button2_press_count
    if button1.value() == 0:
        if button1_press_count <=100:
            button1_press_count += 1
        else:
            button1_press_count = 0
            change_button1_flag()
            # change_arm_flag()
    else:
        button1_press_count = 0
    if button2.value() == 0:
        if button2_press_count <=100:
            button2_press_count += 1
        else:
            button2_press_count = 0
            change_button2_flag()

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
        if res == cm_hdsk:
            await asyncio.sleep_ms(10)
            await swriter.awrite(cm_hdsk_ack)
        elif res == b'%7610*':
            await asyncio.sleep_ms(9)# I don't know if this timing is good, should look into it later
            await swriter.awrite(b'&76100*')
        elif res == b'%7600*':
            await asyncio.sleep_ms(10)
            await swriter.awrite(b'&76000*')

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