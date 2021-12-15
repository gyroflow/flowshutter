## Hardware specification

UART with:
- 420000 baud rate
- 8 bits per byte
- 1 stop bit
- no parity
- LSB first
- Big endian

## Frame structure

Each frame has a sam structure:
```
<Device address> <Length> <Type> <Payload> <CRC>
```
- Device address: refers to the target device address. 1 byte.
- Length: the length of (``<type> + <Payload> + <CRC>``). 1 byte.
- Type: the type of the frame. 1 byte.
- Payload: length depends on the frame type.
- CRC: the CRC of the frame. 2 bytes.

For RX => FC:
- Device address: 0xC8 (FLIGHT_CONTROLLER)
- Length: 0x18 (1+22+1=24 = 0x18)
- Type: 0x16 (RC_CHANNELS_PACKED)
- Payload: 22 bytes.
- CRC: generic CRC8 with poly 0xD5.


