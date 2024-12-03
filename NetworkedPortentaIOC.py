import logging
import socket
import struct
import sys

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

def portenta_read(address: str, port: int, bus: str, pin: int):
    """
    Communicates with the Arduino PMC
    """

    message = f"GET {bus} {pin}\n"
    sock = connection(address, port)
    sock.sendall(message.encode('utf-8'))
    message_received = sock.recv(1024).decode('utf-8')
    sock.close()
    print(f"Received: {message_received}")
    value_received = message_received.strip().split(' ')[-1]
    print(f"value received: {value_received}")
    return value_received

def portenta_write(address: str, port: int, bus: str, pin: int, value: int|float):
    """
    Communicates with the Arduino PMC
    """

    message = f"SET {bus} {pin} {value}\n"
    sock = connection(address, port)
    sock.sendall(message.encode('utf-8'))
    message_received = sock.recv(1024)
    sock.close()
    if message_received != b"OK":
        print(f"Unexpected response received: {message_received}")
    return message_received


def connection(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))
    return sock


class PortentaIOC(PVGroup):
    """
    A group of PVs regarding reading the pressure.
    """

    def __init__(self, address, port, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.address: str = address
        self.port: str = port

    timestamp = pvproperty(
        value=str(datetime.now(timezone.utc).isoformat()),
        name="timestamp",
        doc="Timestamp of portenta readout",
        dtype=PvpropertyString,
    )

    do0 = pvproperty(name="do0", doc="Digital output 0, can be 'Low' or 'High'", enum_strings=['Low', 'High'], dtype=ChannelType.ENUM, record='bo')   
    do1 = pvproperty(name="do1", doc="Digital output 1, can be 'Low' or 'High'", enum_strings=['Low', 'High'], dtype=ChannelType.ENUM, record='bo')
    do2 = pvproperty(name="do2", doc="Digital output 2, can be 'Low' or 'High'", enum_strings=['Low', 'High'], dtype=ChannelType.ENUM, record='bo')
    do3 = pvproperty(name="do3", doc="Digital output 3, can be 'Low' or 'High'", enum_strings=['Low', 'High'], dtype=ChannelType.ENUM, record='bo')
    do4 = pvproperty(name="do4", doc="Digital output 4, can be 'Low' or 'High'", enum_strings=['Low', 'High'], dtype=ChannelType.ENUM, record='bo')
    do5 = pvproperty(name="do5", doc="Digital output 5, can be 'Low' or 'High'", enum_strings=['Low', 'High'], dtype=ChannelType.ENUM, record='bo')
    do6 = pvproperty(name="do6", doc="Digital output 6, can be 'Low' or 'High'", enum_strings=['Low', 'High'], dtype=ChannelType.ENUM, record='bo')
    do7 = pvproperty(name="do7", doc="Digital output 7, can be 'Low' or 'High'", enum_strings=['Low', 'High'], dtype=ChannelType.ENUM, record='bo')
    @do0.putter
    async def do0(self, instance, value):
        print(f"Setting DO0 to {value}")
        portenta_write(self.address, self.port, "DO", 0, value)
        # await self.do0.write(value)
    @do1.putter
    async def do1(self, instance, value):
        print(f"Setting DO1 to {value}")
        portenta_write(self.address, self.port, "DO", 1, value)
        # await self.do1.write(value)
    @do2.putter
    async def do2(self, instance, value):
        print(f"Setting DO2 to {value}")
        portenta_write(self.address, self.port, "DO", 2, value)
        # await self.do2.write(value)
    @do3.putter
    async def do3(self, instance, value):
        print(f"Setting DO3 to {value}")
        portenta_write(self.address, self.port, "DO", 3, value)
        # await self.do3.write(value)
    @do4.putter
    async def do4(self, instance, value):
        print(f"Setting DO4 to {value}")
        portenta_write(self.address, self.port, "DO", 4, value)
        # await self.do4.write(value)
    @do5.putter
    async def do5(self, instance, value):
        print(f"Setting DO5 to {value}")
        portenta_write(self.address, self.port, "DO", 5, value)
        # await self.do5.write(value)
    @do6.putter
    async def do6(self, instance, value):
        print(f"Setting DO6 to {value}")
        portenta_write(self.address, self.port, "DO", 6, value)
        # await self.do6.write(value)
    @do7.putter
    async def do7(self, instance, value):
        print(f"Setting DO7 to {value}")
        portenta_write(self.address, self.port, "DO", 7, value)
        # await self.do7.write(value)

    update_hook = pvproperty(value=0, name="update_hook", doc="Update hook for the IOC", read_only=True)
    @update_hook.scan(period=10)
    async def update_hook(self, instance, async_lib):
        for DOPort in range(8):
            message = portenta_read(self.address, self.port, "DO", DOPort)
            await getattr(self, f"do{DOPort}").write(int(message))

    # @pressure.scan(period=6)
    # async def pressure(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
    #     address = self.address
    #     port = self.port
    #     await self.pressure.write(portenta_read(address, port))
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
    ioc = PortentaIOC(address=args.host, port=args.port, **ioc_options)
    run(ioc.pvdb, **run_options)


if __name__ == "__main__":
    main()