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
    sock.sendall(message.encode('utf-8'))
    message_received = sock.recv(1024).decode('utf-8')
    sock.close()
    print(f"Received: {message_received}")
    value_received = message_received.strip().split(' ')[-1]
    # print(f"value received: {value_received}")
    return value_received

def portenta_write(host: str, port: int, bus: str, pin: int, value: int|float):
    """
    Communicates with the Arduino PMC
    """

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
        # await self.do0.write(value)
    @do1.putter
    async def do1(self, instance, value):
        print(f"Setting do1 to {value}")
        portenta_write(self.host, self.port, "DO", 1, value)
        # await self.do1.write(value)
    @do2.putter
    async def do2(self, instance, value):
        print(f"Setting do2 to {value}")
        portenta_write(self.host, self.port, "DO", 2, value)
        # await self.do2.write(value)
    @do3.putter
    async def do3(self, instance, value):
        print(f"Setting do3 to {value}")
        portenta_write(self.host, self.port, "DO", 3, value)
        # await self.do3.write(value)
    @do4.putter
    async def do4(self, instance, value):
        print(f"Setting do4 to {value}")
        portenta_write(self.host, self.port, "DO", 4, value)
        # await self.do4.write(value)
    @do5.putter
    async def do5(self, instance, value):
        print(f"Setting do5 to {value}")
        portenta_write(self.host, self.port, "DO", 5, value)
        # await self.do5.write(value)
    @do6.putter
    async def do6(self, instance, value):
        print(f"Setting do6 to {value}")
        portenta_write(self.host, self.port, "DO", 6, value)
        # await self.do6.write(value)
    @do7.putter
    async def do7(self, instance, value):
        print(f"Setting do7 to {value}")
        portenta_write(self.host, self.port, "DO", 7, value)
        # await self.do7.write(value)

    async def update_pin_status(self):
        for DOPort in range(8):
            value = portenta_read(self.host, self.port, "DO", DOPort)
            await getattr(self, f"do{DOPort}_RBV").write(value)

    update_hook = pvproperty(value=5.0, name="update_hook", doc="Update hook for the IOC", read_only=True)
    @update_hook.scan(period=10)
    async def update_hook(self, instance, async_lib):
        await self.timestamp.write(datetime.now(timezone.utc).isoformat())
        await self.update_pin_status()


    # @pressure.scan(period=6)
    # async def pressure(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
    #     host = self.host
    #     port = self.port
    #     await self.pressure.write(portenta_read(host, port))
    #     await self.timestamp.write(datetime.now(timezone.utc).isoformat())


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