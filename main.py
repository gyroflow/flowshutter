from machine import Pin, UART, Timer
import crsf, oled, target, sony_multiport
import uasyncio as asyncio
from time import sleep

oled1 = oled.oled_init()

uart1, uart2, _, button1, button2 = target.init_pins()
fc_arm_packet, fc_disarm_packet = crsf.init_packet()
rcd_prs, rcd_rls, cm_hdsk, cm_hdsk_ack, cm_rcd_start, cm_rcd_start_ack, cm_rcd_stop, cm_rcd_stop_ack = sony_multiport.init_multiport_packet()
state = ['idle', 'starting', 'recording', 'stopping', 'stopped']

button1_press_count = 0
button1_trigger = 0
button2_press_count = 0
button2_trigger = 0
arm_flag=0
switching_flag = 0
def check_button(t):
    global button1_press_count
    global button1_trigger
    global button2_press_count
    global button2_trigger
    global switching_flag
    if button1.value() == 0:
        if button1_press_count <=100:
            button1_press_count += 1
        else:
            button1_press_count = 0
            button1_trigger = 1
            if current_state == state[0]:
                switching_flag = 1
            print('button1 tiggered', button1_trigger)
            print('switching_flag', switching_flag)
    else:
        button1_press_count = 0
    if button2.value() == 0:
        if button2_press_count <=100:
            button2_press_count += 1
        else:
            button2_press_count = 0
            button2_trigger = 1

timer0 = Timer(0)
timer0.init(period=5, mode=Timer.PERIODIC, callback=check_button)

current_state = state[0]

async def check_state():
    global current_state
    global button1_trigger
    global button2_trigger
    global arm_flag
    global switching_flag
    swriter = asyncio.StreamWriter(uart2, {})
    while switching_flag == 1:
        if current_state == state[0]: # idle
            current_state = state[1] # next is starting
            oled.show_starting_info(oled1)
        if current_state == state[1]: # starting
            await swriter.awrite(rcd_prs)
            print('rcd_prs sent')
            await asyncio.sleep_ms(40)
            await swriter.awrite(rcd_rls)
            print('rcd_rls sent')
        if current_state == state[2]: # recording
            current_state = state[3]  # next is stopping
        if current_state == state[3]: # stopping
            await swriter.awrite(rcd_prs)
            await asyncio.sleep_ms(40)
            await swriter.awrite(rcd_rls)
        if current_state == state[4]: # stopped
            await asyncio.sleep_ms(1000)
            current_state = state[0]  # next is idle

        # if current_state == state[0]: # idle state
        #     switching_flag = 0
        #     arm_flag = 0
        #     print('idle')
        #     oled.show_idle_info(oled1)
        #     if button1_trigger == 1:
        #         switching_flag = 1
        #         current_state = state[1]
        # elif current_state == state[1]: # starting state
        #     button1_trigger = 0
        #     switching_flag = 0
        #     print('starting')
        #     oled.show_starting_info(oled1)
        #     await swriter.awrite(rcd_prs)
        #     await asyncio.sleep_ms(40)
        #     await swriter.awrite(rcd_rls)
        #     current_state = state[2]
        # elif current_state == state[2]: # recording state
        #     arm_flag = 1
        #     switching_flag = 0
        #     # print('recording')
        #     oled.show_arm_info(oled1)
        #     if button1_trigger == 1:
        #         switching_flag = 1
        #         current_state = state[3]
        # elif current_state == state[3]: # stopping state      
        #     button1_trigger = 0
        #     switching_flag = 0
        #     print('stopping')
        #     oled.show_stopping_info(oled1)
        #     await swriter.awrite(rcd_prs)
        #     await asyncio.sleep_ms(40)
        #     await swriter.awrite(rcd_rls)
        #     current_state = state[4]
        # elif current_state == state[4]: # stopped state
        #     arm_flag = 0
        #     switching_flag = 0
        #     print('stopped')
        #     oled.show_disarm_info(oled1)
        #     await asyncio.sleep_ms(1000)
        #     current_state = state[0] # back to idle state
        #     switching_flag = 1


async def receive_and_response():
    global switching_flag
    global arm_flag
    swriter = asyncio.StreamWriter(uart2, {})
    sreader = asyncio.StreamReader(uart2)
    while True:
        res = await sreader.read(n=-1)
        print('Cam sent:', res)
        if res == cm_hdsk:
            await asyncio.sleep_ms(10)
            await swriter.awrite(cm_hdsk_ack)
        elif res == cm_rcd_start:
            await asyncio.sleep_ms(9)# I don't know if this timing is good, should look into it later
            switching_flag = 0
            arm_flag = 1
            await swriter.awrite(cm_rcd_start_ack)
            print('camera is recording')
            oled.show_arm_info(oled1)
        elif res == cm_rcd_stop:
            await asyncio.sleep_ms(10)
            switching_flag = 0
            arm_flag = 0
            await swriter.awrite(cm_rcd_stop_ack)
            print('camera is stopped')
            oled.show_disarm_info(oled1)

def send_crsf_packet(t):
    global arm_flag
    if arm_flag == 1:
        uart1.write(fc_arm_packet)
    else:
        uart1.write(fc_disarm_packet)
timer1 = Timer(1)
timer1.init(period=4, mode=Timer.PERIODIC, callback=send_crsf_packet)



loop = asyncio.get_event_loop()
# loop.create_task(sender())
loop.create_task(check_state())
loop.create_task(receive_and_response())
loop.run_forever()