import logging
import socket
import struct
import sys
import attrs
from datetime import datetime, timezone
from caproto import ChannelData, ChannelType
from caproto.server import (
    AsyncLibraryLayer,
    PVGroup,
    pvproperty,
    PvpropertyString,
    run,
    template_arg_parser,
)

def validate_ip_address(instance, attribute, value):
    try:
        socket.inet_aton(value)
    except socket.error:
        raise ValueError(f"Invalid IP address: {value}")

def validate_port_number(instance, attribute, value):
    if not (0 <= value <= 65535):
        raise ValueError(f"Port number must be between 0 and 65535, got {value}")

def portenta_read(host: str, port: int, bus: str, pin: int):
    """
    Communicates with the Arduino PMC
    """

    message = f"GET {bus} {pin}\n"
    sock = connection(host, port)
    print(f'{message=}') 
    sock.sendall(message.encode('utf-8'))
    message_received = sock.recv(1024).decode('utf-8')
    sock.close()
    # print(f"Received: {message_received}")
    value_received = message_received.strip().split(' ')[-1]
    # print(f"value received: {value_received}")
    return value_received

def portenta_write(host: str, port: int, bus: str, pin: int, value: int|float|str):
    """
    Communicates with the Arduino PMC
    """

    if isinstance(value, str):
        # assuming bool
        value = 1 if value in ['On', 'ON', 'on', '1', 'True', 'true'] else 0
    message = f"SET {bus} {pin} {value}\n"
    sock = connection(host, port)
    print(f"Sending: {message}")
    sock.sendall(message.encode('utf-8'))
    message_received = sock.recv(1024).decode('utf-8')
    sock.close()
    if message_received != "OK":
        print(f"Unexpected response received: {message_received}")
    else:
        print(f"Expected message received: {message_received}")
    # return message_received


def connection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

@attrs.define
class PortentaIOC(PVGroup):
    """
    A group of PVs regarding reading the pressure.
    """
    # IP address of the board
    host: str = attrs.field(default = "192.168.2.114", validator=validate_ip_address, converter=str)

    # Port number for communication
    port: int = attrs.field(default = 502, validator=validate_port_number, converter=int)

    do0 = pvproperty(name="do0", doc="Digital output 0, can be 0 or 1", dtype=bool, record='bo')   
    do1 = pvproperty(name="do1", doc="Digital output 1, can be 0 or 1", dtype=bool, record='bo')
    do2 = pvproperty(name="do2", doc="Digital output 2, can be 0 or 1", dtype=bool, record='bo')
    do3 = pvproperty(name="do3", doc="Digital output 3, can be 0 or 1", dtype=bool, record='bo')
    do4 = pvproperty(name="do4", doc="Digital output 4, can be 0 or 1", dtype=bool, record='bo')
    do5 = pvproperty(name="do5", doc="Digital output 5, can be 0 or 1", dtype=bool, record='bo')
    do6 = pvproperty(name="do6", doc="Digital output 6, can be 0 or 1", dtype=bool, record='bo')
    do7 = pvproperty(name="do7", doc="Digital output 7, can be 0 or 1", dtype=bool, record='bo')
    do0_RBV = pvproperty(name="do0_RBV", doc="Digital output 0 readback value, can be 0 or 1", dtype=bool, record='bo')   
    do1_RBV = pvproperty(name="do1_RBV", doc="Digital output 1 readback value, can be 0 or 1", dtype=bool, record='bo')
    do2_RBV = pvproperty(name="do2_RBV", doc="Digital output 2 readback value, can be 0 or 1", dtype=bool, record='bo')
    do3_RBV = pvproperty(name="do3_RBV", doc="Digital output 3 readback value, can be 0 or 1", dtype=bool, record='bo')
    do4_RBV = pvproperty(name="do4_RBV", doc="Digital output 4 readback value, can be 0 or 1", dtype=bool, record='bo')
    do5_RBV = pvproperty(name="do5_RBV", doc="Digital output 5 readback value, can be 0 or 1", dtype=bool, record='bo')
    do6_RBV = pvproperty(name="do6_RBV", doc="Digital output 6 readback value, can be 0 or 1", dtype=bool, record='bo')
    do7_RBV = pvproperty(name="do7_RBV", doc="Digital output 7 readback value, can be 0 or 1", dtype=bool, record='bo')
    ao0 = pvproperty(name="ao0", doc="Analog output 0, can be 0-10V", dtype=float, record='ao')   
    ao1 = pvproperty(name="ao1", doc="Analog output 1, can be 0-10V", dtype=float, record='ao')
    ao2 = pvproperty(name="ao2", doc="Analog output 2, can be 0-10V", dtype=float, record='ao')
    ao3 = pvproperty(name="ao3", doc="Analog output 3, can be 0-10V", dtype=float, record='ao')

    dio0 = pvproperty(name="dio0", doc="Digital i/o 0, can be 0 or 1", dtype=bool, record='bo')   
    dio1 = pvproperty(name="dio1", doc="Digital i/o 1, can be 0 or 1", dtype=bool, record='bo')
    dio2 = pvproperty(name="dio2", doc="Digital i/o 2, can be 0 or 1", dtype=bool, record='bo')
    dio3 = pvproperty(name="dio3", doc="Digital i/o 3, can be 0 or 1", dtype=bool, record='bo')
    dio4 = pvproperty(name="dio4", doc="Digital i/o 4, can be 0 or 1", dtype=bool, record='bo')
    dio5 = pvproperty(name="dio5", doc="Digital i/o 5, can be 0 or 1", dtype=bool, record='bo')
    dio6 = pvproperty(name="dio6", doc="Digital i/o 6, can be 0 or 1", dtype=bool, record='bo')
    dio7 = pvproperty(name="dio7", doc="Digital i/o 7, can be 0 or 1", dtype=bool, record='bo')
    dio0_RBV = pvproperty(name="dio0_RBV", doc="Digital i/o 0 readback value, can be 0 or 1", dtype=bool, record='bo')   
    dio1_RBV = pvproperty(name="dio1_RBV", doc="Digital i/o 1 readback value, can be 0 or 1", dtype=bool, record='bo')
    dio2_RBV = pvproperty(name="dio2_RBV", doc="Digital i/o 2 readback value, can be 0 or 1", dtype=bool, record='bo')
    dio3_RBV = pvproperty(name="dio3_RBV", doc="Digital i/o 3 readback value, can be 0 or 1", dtype=bool, record='bo')
    dio4_RBV = pvproperty(name="dio4_RBV", doc="Digital i/o 4 readback value, can be 0 or 1", dtype=bool, record='bo')
    dio5_RBV = pvproperty(name="dio5_RBV", doc="Digital i/o 5 readback value, can be 0 or 1", dtype=bool, record='bo')
    dio6_RBV = pvproperty(name="dio6_RBV", doc="Digital i/o 6 readback value, can be 0 or 1", dtype=bool, record='bo')
    dio7_RBV = pvproperty(name="dio7_RBV", doc="Digital i/o 7 readback value, can be 0 or 1", dtype=bool, record='bo')

    di0_RBV = pvproperty(name="di0_RBV", doc="Digital input 0 readback value, can be 0 or 1", dtype=bool, record='bo')   
    di1_RBV = pvproperty(name="di1_RBV", doc="Digital input 1 readback value, can be 0 or 1", dtype=bool, record='bo')
    di2_RBV = pvproperty(name="di2_RBV", doc="Digital input 2 readback value, can be 0 or 1", dtype=bool, record='bo')
    di3_RBV = pvproperty(name="di3_RBV", doc="Digital input 3 readback value, can be 0 or 1", dtype=bool, record='bo')
    di4_RBV = pvproperty(name="di4_RBV", doc="Digital input 4 readback value, can be 0 or 1", dtype=bool, record='bo')
    di5_RBV = pvproperty(name="di5_RBV", doc="Digital input 5 readback value, can be 0 or 1", dtype=bool, record='bo')
    di6_RBV = pvproperty(name="di6_RBV", doc="Digital input 6 readback value, can be 0 or 1", dtype=bool, record='bo')
    di7_RBV = pvproperty(name="di7_RBV", doc="Digital input 7 readback value, can be 0 or 1", dtype=bool, record='bo')

    ai0_RBV = pvproperty(name="ai0_RBV", doc="Analog input 0 readback value, can be 0-10V", dtype=float, record='ao')   
    ai1_RBV = pvproperty(name="ai1_RBV", doc="Analog input 1 readback value, can be 0-10V", dtype=float, record='ao')
    ai2_RBV = pvproperty(name="ai2_RBV", doc="Analog input 2 readback value, can be 0-10V", dtype=float, record='ao')
    ai3_RBV = pvproperty(name="ai3_RBV", doc="Analog input 3 readback value, can be 0-10V", dtype=float, record='ao')


    def __init__(self, *args, **kwargs) -> None:
        for k in list(kwargs.keys()):
            if k in ['host', 'port']:
                setattr(self, k, kwargs.pop(k))
        super().__init__(*args, **kwargs)

    timestamp = pvproperty(
        value=str(datetime.now(timezone.utc).isoformat()),
        name="timestamp",
        doc="Timestamp of portenta readout",
        dtype=PvpropertyString,
    )

    @do0.putter
    async def do0(self, instance, value):
        print(f"Setting do0 to {value}")
        portenta_write(self.host, self.port, "DO", 0, value)
    @do1.putter
    async def do1(self, instance, value):
        print(f"Setting do1 to {value}")
        portenta_write(self.host, self.port, "DO", 1, value)
    @do2.putter
    async def do2(self, instance, value):
        print(f"Setting do2 to {value}")
        portenta_write(self.host, self.port, "DO", 2, value)
    @do3.putter
    async def do3(self, instance, value):
        print(f"Setting do3 to {value}")
        portenta_write(self.host, self.port, "DO", 3, value)
    @do4.putter
    async def do4(self, instance, value):
        print(f"Setting do4 to {value}")
        portenta_write(self.host, self.port, "DO", 4, value)
    @do5.putter
    async def do5(self, instance, value):
        print(f"Setting do5 to {value}")
        portenta_write(self.host, self.port, "DO", 5, value)
    @do6.putter
    async def do6(self, instance, value):
        print(f"Setting do6 to {value}")
        portenta_write(self.host, self.port, "DO", 6, value)
    @do7.putter
    async def do7(self, instance, value):
        print(f"Setting do7 to {value}")
        portenta_write(self.host, self.port, "DO", 7, value)

    @ao0.putter
    async def ao0(self, instance, value):
        print(f"Setting ao0 to {value}")
        portenta_write(self.host, self.port, "AO", 0, value)
    @ao1.putter
    async def ao1(self, instance, value):
        print(f"Setting ao1 to {value}")
        portenta_write(self.host, self.port, "AO", 1, value)
    @ao2.putter
    async def ao2(self, instance, value):
        print(f"Setting ao2 to {value}")
        portenta_write(self.host, self.port, "AO", 2, value)
    @ao3.putter
    async def ao3(self, instance, value):
        print(f"Setting ao3 to {value}")
        portenta_write(self.host, self.port, "AO", 3, value)

    @dio0.putter
    async def dio0(self, instance, value):
        print(f"Setting dio0 to {value}")
        portenta_write(self.host, self.port, "DIO", 0, value)
    @dio1.putter
    async def dio1(self, instance, value):
        print(f"Setting dio1 to {value}")
        portenta_write(self.host, self.port, "DIO", 1, value)
    @dio2.putter
    async def dio2(self, instance, value):
        print(f"Setting dio2 to {value}")
        portenta_write(self.host, self.port, "DIO", 2, value)
    @dio3.putter
    async def dio3(self, instance, value):
        print(f"Setting dio3 to {value}")
        portenta_write(self.host, self.port, "DIO", 3, value)
    @dio4.putter
    async def dio4(self, instance, value):
        print(f"Setting dio4 to {value}")
        portenta_write(self.host, self.port, "DIO", 4, value)
    @dio5.putter
    async def dio5(self, instance, value):
        print(f"Setting dio5 to {value}")
        portenta_write(self.host, self.port, "DIO", 5, value)
    @dio6.putter
    async def dio6(self, instance, value):
        print(f"Setting dio6 to {value}")
        portenta_write(self.host, self.port, "DIO", 6, value)
    @dio7.putter
    async def dio7(self, instance, value):
        print(f"Setting dio7 to {value}")
        portenta_write(self.host, self.port, "DIO", 7, value)


    async def update_pin_status(self):
        for DOPort in range(8):
            value = portenta_read(self.host, self.port, "DO", DOPort)
            await getattr(self, f"do{DOPort}_RBV").write(value)
        for DIPort in range(8):
            value = portenta_read(self.host, self.port, "DI", DIPort)
            await getattr(self, f"do{DIPort}_RBV").write(value)
        for AIPort in range(3):
            value = portenta_read(self.host, self.port, "AI", AIPort)
            await getattr(self, f"do{AIPort}_RBV").write(value)
        for DIOPort in range(8):
            value = portenta_read(self.host, self.port, "DIO", DIPort)
            await getattr(self, f"dio{DIOPort}_RBV").write(value)

    update_hook = pvproperty(value=0, name="update_hook", doc="Update hook for the IOC", record = 'ai', read_only=True)
    
    # The .SCAN field should allow you to set a scan rate: caput Portenta:update_hook.SCAN '.5 second' for example
    @update_hook.scan(period=10, use_scan_field=True)
    async def update_hook(self, instance, async_lib):
        await self.timestamp.write(datetime.now(timezone.utc).isoformat())
        await self.update_pin_status()

def main(args=None):

    parser, split_args = template_arg_parser(
        default_prefix="Portenta:",
        desc="EPICS IOC for accessing I/O on the Arduino Portenta Machine Control (PMC) over network",
    )

    if args is None:
        args = sys.argv[1:]

    parser.add_argument(
        "--host", required=True, type=str, help="IP address of the host/device"
    )
    parser.add_argument(
        "--port", required=True, type=int, help="Port number of the device"
    )

    args = parser.parse_args()

    logging.info("Running Networked Portenta IOC")

    ioc_options, run_options = split_args(args)
    ioc = PortentaIOC(host=args.host, port=args.port, **ioc_options)
    run(ioc.pvdb, **run_options)


if __name__ == "__main__":
    main()