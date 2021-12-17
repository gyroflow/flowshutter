## Hardware specification

Sony multi terminal USB is a custom USB connector with Sony defined pins based on a micro USB connector.

Micro USB part is same as the standard micro USB pin definition. Note that A5 is the GND.

Sony pin part's definition is here:

(Look from the connector side) from right to left is 1-10:
- 1: Power on/off (triggerd by shorting to ground)
- 2: GND (without circuit it's NC)
- 3: Video out
- 4: Audio L out
- 5: Audio R out
- 6: Select (for remote use case there should be a 100k resistor against to GND)
- 7: UART_TX
- 8: UART_RX
- 9: NC
- 10: 3V3

UART with:
- 9600 baud rate
- 8 bits per byte
- 1 stop bit
- EVEN parity
- LSB first
- Big endian
- ASCII format

## Communication mode

- Begin with a symbol [``#``, ``$``, ``%``, ``&``], followed by some data, ending with ``*``.
    - ``#``: (Remote -> Camera) Command
    - ``$``: (Camera -> Remote) Command ACK
    - ``%``: (Camera -> Remote) Detect Message?
    - ``&``: (Remote -> Camera) Detect Message ACK?


### Power up

When the remote board was plugged in, the voltage on UART lines will be pulled to high level (3.3V). After around 323ms, the camera will send a ``%000*`` command to the remote board. The remote board should send a ``&00080*`` confirmation back to the camera 10ms after receiving the ``%000*`` command.

- Power up
- (323ms) (which means the remote must finish initialization after UART configured within 300ms)
- Camera: ``%000*``
- (10ms)
- Remote: ``&00080*``

### Heartbeat (?)

Same as above, camera send ``%000*`` command to remote board. The remote board should send a ``&00080*`` confirmation back to the camera 10ms after receiving the ``%000*`` command.

- Camera: ``%000*``
- (10ms)
- Remote: ``&00080*``

### Record

(Press video record button)
- Remote: ``#7100*``
- (no delay)
- Camera: ``&71000*``

(Release video record button)
- Remote: ``#7110*``
- (no delay)
- Camera: ``&71100*``

During recording, the camera will firstly send an ``%000*`` to the remote (I guess for querying? ) , then remote need to send a ``&00080*`` confirmation back to the camera 10ms after receiving the ``%000*`` command. The camera then will send a ``%7610*`` immediately, followed with ``%7611*``, ``%7612*``, ``%7613*`` and ``%7614*``, around [I forget] ms after receiving the ``%7614*``, the camera will send a ``&76140*`` command to the remote board.

- Camera: ``%000*``
- (10ms)
- Remote: ``&00080*``
- Camera: ``%7610*``
- (I forget this timing)
- Camera: ``%7611*``
- (I forget this timing)
- Camera: ``%7612*``
- (I forget this timing)
- Camera: ``%7613*``
- (I forget this timing)
- Camera: ``%7614*``
- (I forget this timing)
- Remote: ``&76140*``

Sometimes it is quite difficult to stop recording, I'm currently digging into it.