## Hardware specification

UART with:
- 9600 baud rate
- 8 bits per byte
- 1 stop bit
- no parity
- LSB first
- Big endian

# Timing Diagram:
| Byte 0 | Byte 1 | Byte 2 | Byte 3 | Byte 4 | Byte 5 | Byte 6 | Byte 7 | nodata | Byte 0 | ... |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
|  0x18  |  0x33  |  0xxx  |  0xxx  |  0xxx  |  0xxx  |  0xxx  |  0xxx  |  delay |  0x18  | ... |

- Timp gap between two start bit is 1.2ms.
- Time gap between Byte 7 and the next Byte 0 is 20ms(PAL) or 16.6ms(NTSC).

## Bytes

For link remote -> camera:

- Byte 0 = 0x18

For start/stop recording:

- Byte 1 = 0x33

Then we can just don't care about the rest of the bytes.

## Frame

The same command frame must be repeated by 5 times.
