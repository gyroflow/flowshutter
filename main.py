from machine import Pin, UART, Timer
import crsf, oled
from time import sleep

oled1 = oled.oled_init()

uart1 = UART(1, baudrate=420000, bits = 8, parity = None, stop = 1, tx = 33, rx = 32)
uart2 = UART(2, baudrate = 9600, bits = 8, parity = 0,    stop = 1, tx = 25, rx = 26)
p19 = Pin(19, Pin.IN, Pin.PULL_UP)

fc_arm_frame, fc_disarm_frame = crsf.create_frames()
arm_flag=0
def send_crsf_packet(t):
    global arm_flag
    if arm_flag == 1:
        uart1.write(fc_arm_frame)
    else:
        uart1.write(fc_disarm_frame)

timer1 = Timer(1)
timer1.init(period=4, mode=Timer.PERIODIC, callback=send_crsf_packet)

press_count = 0


def change_arm_flag():
    global arm_flag
    if arm_flag == 0:
        arm_flag = 1
        oled.show_arm_info(oled1)
    else:
        arm_flag = 0
        oled.show_disarm_info(oled1)

def check_cmd():
    global press_count
    if p19.value() == 0:
        if press_count <=100:
            press_count += 1
        else:
            press_count = 0
            change_arm_flag()
    else:
        press_count = 0

cam_press_frame = '#7100*' #ASCII is needed here
cam_release_frame = '#7110*'
test_button_flag = 0
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



while(1):
    
    # test_check_button()


    check_cmd()

    # send_cam_frame()
    # send_fc_frame(arm_flag)

    sleep(0.005)
