# Flowshutter

<p align="center">
  <a href="https://gyroflow.xyz">Homepage</a> •
  <a href="https://docs.gyroflow.xyz/logging/flowshutter/flowshutter/">Documentation</a> •
  <a href="https://discord.gg/WfxZZXjpke">Discord</a> •
  <a href="https://github.com/gyroflow/flowshutter/issues">Report bug</a> •
  <a href="https://github.com/gyroflow/flowshutter/issues">Request feature</a>
</p>

<p align="center">
  <a href="https://github.com/gyroflow/flowshutter/languages/top">
    <img src="https://img.shields.io/github/languages/top/gyroflow/flowshutter" alt="Languages">
  </a>
  <a href="https://github.com/gyroflow/flowshutter/">
    <img src="https://img.shields.io/github/contributors/gyroflow/flowshutter?color=dark-green" alt="Contributors">
  </a>
  <a href="https://github.com/gyroflow/flowshutter/issues/">
    <img src="https://img.shields.io/github/issues/gyroflow/flowshutter" alt="Issues">
  </a>
  <a href="https://github.com/gyroflow/flowshutter/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/gyroflow/flowshutter" alt="License">
  </a>
</p>

Flowshutter is a custom camera remote. When used in conjunction with readily available hardware, this results in a flexible and reliable external camera motion logger for Gyroflow. It can provide precise synchronization of camera video recording and motion logger (betaflight/emuflight FC) recording. 

It was designed to be used with the [Gyroflow](https://github.com/gyroflow/gyroflow) software to provide you one of the best open source video stabilization experiences.


## Features

Flowshutter has the following features:

- '1-click' - (1) start/stop camera recording and (2) arm/disarm FC, via one click 
- Camera recording start/stop control
- FC arm/disarm control
- OLED display

with many more features on the way!

## Supported Hardware

Currently we are working with a manufacturer that will produce flowshutter hardware. We will disclose more relevant information in the future.

At the same time you can try to DIY your own flowshutter hardware. We have two open sourced designs:

- [Credit card sized design](https://oshwhub.com/AirFleet/xiang-ji-kong-zhi-ban):

[![build](images/flowshutter-credit-card-sized.png)](https://youtu.be/ELaQPYE9ncA)

- [FC sized design](https://oshwhub.com/AirFleet/xiang-ji-kong-zhi-ban_copy_copy): 

[![build](images/flowshutter-fc-sized.png)](https://youtu.be/ry7Ey54Z7s8)


### Compatible camera protocol/trigger mechanisms

- [x] Sony MULTI Terminal protocol
- [x] Momentary Ground
- [x] 3.3V Schmitt trigger
- (WIP) 5V Schmitt trigger
- (WIP) Sony LANC protocol
- (WIP) HDMI CEC protocol

For more information about support camera list, please check the [list](https://docs.gyroflow.xyz/logging/flowshutter/camera%20list/) on the [documentation website](https://docs.gyroflow.xyz/).

### Compatible FC

FC is short for flight controller, more specifically with betaflight/emuflight running on.

- flowbox (highly recommended)
- modern FC with BMI270 gyroscope (recommended)
- any other FC that support CRSF protocol

## Development Guide
### Flash micropython firmware

The micropython firmware we used is [v1.18](https://micropython.org/resources/firmware/esp32-20220117-v1.18.bin), You can find a copy in the `/tools` directory. Also, a `uPyCraft` windows version is also provided in the `/tools` directory. You can try to use that to flash your ESP32 without the help of ESP-idf.

### Set up environment

`Visual Studio Code` with `Pymakr` extension is recommended.

1. Install `node`
2. Manually install `Visual Studio Code` [1.64.2](https://code.visualstudio.com/updates/v1_64)
3. Install `Pymakr` extension in `Visual Studio Code`
4. Update `Visual Studio Code` to the latest version (currently 1.6.0)
5. Manually install `Pymakr` ([v1.18.0-beta.0](https://github.com/pycom/pymakr-vsc/releases/tag/v1.1.18-beta.0) or newer) extension in `Visual Studio Code`
6. Edit `Pymakr`'s global settings that add `"wch.cn",` to `"autoconnect_comport_manufacturers"`
7. Modify content of `"address"` to `"address": "",`
8. Pull flowshutter code from `https://github.com/gyroflow/flowshutter`
9. Then you can connect and upload the flowshutter code


## License

- micropython binary  ``/tool/esp32-20210902-v1.18.bin`` comes from micropython, licensed under MIT
- uPyCraft_V1.1.exe ``/tool/uPyCraft_V1.1.exe`` is no licensed
- documents under ``/doc`` are licensed under MIT
- SSD1306 driver ``/ssd1306.py`` is licensed under MIT
- `wlan.py` is licensed under MIT and AGLPv3
- other code is under AGPL-v3.0 **ONLY**

This software is provided as is, and please feel free to use this on your own camera which will be used for shooting comercial images/videos. For any other commercial usage, please contact [DusKing1](1483569698@qq.com).

**Due to egregious abuse of open source in Wuxi, China, this project refuses to provide any support to any user in Wuxi, or to cooperate in any form with any company or individual in Wuxi. Please do something worthy of your conscience.**
