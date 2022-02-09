# Flowshutter

Flowshutter is a customize camera remote written in micropython.

It can synchronize vedio recording of the camera and blackbox logging of your motion logger (in most cases betaflight/emuflight controller with flash chip or SD card). 

It was designed to be used with gyroflow software to provide you the best open source video stabilization experience.

## Hardware

Community version can be found on [here](https://oshwhub.com/AirFleet/xiang-ji-kong-zhi-ban). Checkout our [Build Video](https://www.youtube.com/watch?v=ELaQPYE9ncA)!

## Supported camera

- Sony camera: only with Multiport USB protocol (works beautifully on my A6300)
- Others is on the way

## Supported FC

- flowbox (highly recommended)
- any other FC that support CRSF protocol

## License

- documents under ``/doc`` are licensed under MIT
- micropython binary  ``/tool/esp32-20210902-v1.17.bin`` comes from micropython, licensed under MIT
- SSD1306 driver ``/ssd1306.py`` comes from micropython, licensed under MIT
- uPyCraft_V1.1.exe ``/tool/uPyCraft_V1.1.exe`` is no licensed
- other code is under AGPL-v3.0 **ONLY**

This software is provided as is, and please feel free to use this on your own camera which will be used for shooting comercial images/videos. For any other commercial usage, please contact [DusKing1](1483569698@qq.com).