
import logging
import socket
import sys
import attrs
from datetime import datetime, timezone
from caproto.server import PVGroup, pvproperty, PvpropertyString, run, template_arg_parser, AsyncLibraryLayer
from caproto import ChannelData

import logging

logger = logging.getLogger("PortentaIOC")
logger.setLevel(logging.INFO)

# Validators for IP and Port
def validate_ip_address(instance, attribute, value):
    try:
        socket.inet_aton(value)
    except socket.error:
        raise ValueError(f"Invalid IP address: {value}")


def validate_port_number(instance, attribute, value):
    if not (0 <= value <= 65535):
        raise ValueError(f"Port number must be between 0 and 65535, got {value}")


# PortentaClient encapsulates connection logic
class PortentaClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def read(self, bus: str, pin: int) -> float:
        message = f"GET {bus} {pin}\n"
        with self._connect() as sock:
            sock.sendall(message.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
        return float(response.strip().split()[-1])

    def write(self, bus: str, pin: int, value: int | float | str):
        if isinstance(value, str):
            value = 1 if value.lower() in {'on', '1', 'true'} else 0
        message = f"SET {bus} {pin} {value}\n"
        logger.info(f"Writing message: {message}")
        with self._connect() as sock:
            sock.sendall(message.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
        if response != "OK":
            raise ValueError(f"Unexpected response: {response}")



@attrs.define
class PortentaIOC(PVGroup):
    host: str = attrs.field(default="172.17.1.124", validator=validate_ip_address, converter=str)
    port: int = attrs.field(default=1111, validator=validate_port_number, converter=int)
    client: PortentaClient = attrs.field(init=False)

    def __init__(self, *args, **kwargs) -> None:
        for k in list(kwargs.keys()):
            if k in ['host', 'port']:
                setattr(self, k, kwargs.pop(k))
        self.client = PortentaClient(self.host, self.port)
        super().__init__(*args, **kwargs)

    do0 = pvproperty(name="do0", doc="Digital output 0, can be 0 or 1", dtype=bool, record='bi')
    do0_RBV = pvproperty(name="do0_RBV", doc="Readback value for digital output 0", dtype=bool, record='bi')
    @do0.putter
    async def do0(self, instance, value: bool):
        self.client.write("DO", 0, value)
    @do0.scan(period=6, use_scan_field=True)
    async def do0(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.do0_RBV.write(self.client.read("DO", 0))

    # Repeat for DO1 to DO7
    do1 = pvproperty(name="do1", doc="Digital output 1, can be 0 or 1", dtype=bool, record='bi')
    do1_RBV = pvproperty(name="do1_RBV", doc="Readback value for digital output 1", dtype=bool, record='bi')
    @do1.putter
    async def do1(self, instance, value: bool):
        self.client.write("DO", 1, value)
    @do1.scan(period=6, use_scan_field=True)
    async def do1(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.do1_RBV.write(self.client.read("DO", 1))

    do2 = pvproperty(name="do2", doc="Digital output 2, can be 0 or 1", dtype=bool, record='bi')
    do2_RBV = pvproperty(name="do2_RBV", doc="Readback value for digital output 2", dtype=bool, record='bi')
    @do2.putter
    async def do2(self, instance, value: bool):
        self.client.write("DO", 2, value)
    @do2.scan(period=6, use_scan_field=True)
    async def do2(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.do2_RBV.write(self.client.read("DO", 2))

    do3 = pvproperty(name="do3", doc="Digital output 3, can be 0 or 1", dtype=bool, record='bi')
    do3_RBV = pvproperty(name="do3_RBV", doc="Readback value for digital output 3", dtype=bool, record='bi')
    @do3.putter
    async def do3(self, instance, value: bool):
        self.client.write("DO", 3, value)
    @do3.scan(period=6, use_scan_field=True)
    async def do3(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.do3_RBV.write(self.client.read("DO", 3))

    do4 = pvproperty(name="do4", doc="Digital output 4, can be 0 or 1", dtype=bool, record='bi')
    do4_RBV = pvproperty(name="do4_RBV", doc="Readback value for digital output 4", dtype=bool, record='bi')
    @do4.putter
    async def do4(self, instance, value: bool):
        self.client.write("DO", 4, value)
    @do4.scan(period=6, use_scan_field=True)
    async def do4(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.do4_RBV.write(self.client.read("DO", 4))

    do5 = pvproperty(name="do5", doc="Digital output 5, can be 0 or 1", dtype=bool, record='bi')
    do5_RBV = pvproperty(name="do5_RBV", doc="Readback value for digital output 5", dtype=bool, record='bi')
    @do5.putter
    async def do5(self, instance, value: bool):
        self.client.write("DO", 5, value)
    @do5.scan(period=6, use_scan_field=True)
    async def do5(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.do5_RBV.write(self.client.read("DO", 5))

    do6 = pvproperty(name="do6", doc="Digital output 6, can be 0 or 1", dtype=bool, record='bi')
    do6_RBV = pvproperty(name="do6_RBV", doc="Readback value for digital output 6", dtype=bool, record='bi')
    @do6.putter
    async def do6(self, instance, value: bool):
        self.client.write("DO", 6, value)
    @do6.scan(period=6, use_scan_field=True)
    async def do6(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.do6_RBV.write(self.client.read("DO", 6))

    do7 = pvproperty(name="do7", doc="Digital output 7, can be 0 or 1", dtype=bool, record='bi')
    do7_RBV = pvproperty(name="do7_RBV", doc="Readback value for digital output 7", dtype=bool, record='bi')
    @do7.putter
    async def do7(self, instance, value: bool):
        self.client.write("DO", 7, value)
    @do7.scan(period=6, use_scan_field=True)
    async def do7(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.do7_RBV.write(self.client.read("DO", 7))

    dio0 = pvproperty(name="dio0", doc="Bidirectional digital in/out pin 0", dtype=bool, record='bi')   
    @dio0.putter
    async def dio0(self, instance, value: bool):
        self.client.write("DIO", 0, value)
    @dio0.scan(period=6, use_scan_field=True)
    async def dio0(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio0.write(self.client.read("DIO", 0))



    dio0 = pvproperty(name="dio0", doc="Bidirectional digital in/out pin 0", dtype=bool, record='bi')
    dio0_RBV = pvproperty(name="dio0_RBV", doc="Readback value for bidirectional digital in/out pin 0", dtype=bool, record='bi')
    @dio0.putter
    async def dio0(self, instance, value: bool):
        self.client.write("DIO", 0, value)
    @dio0.scan(period=6, use_scan_field=True)
    async def dio0(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio0_RBV.write(self.client.read("DIO", 0))

    dio1 = pvproperty(name="dio1", doc="Bidirectional digital in/out pin 1", dtype=bool, record='bi')
    dio1_RBV = pvproperty(name="dio1_RBV", doc="Readback value for bidirectional digital in/out pin 1", dtype=bool, record='bi')
    @dio1.putter
    async def dio1(self, instance, value: bool):
        self.client.write("DIO", 1, value)
    @dio1.scan(period=6, use_scan_field=True)
    async def dio1(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio1_RBV.write(self.client.read("DIO", 1))

    dio2 = pvproperty(name="dio2", doc="Bidirectional digital in/out pin 2", dtype=bool, record='bi')
    dio2_RBV = pvproperty(name="dio2_RBV", doc="Readback value for bidirectional digital in/out pin 2", dtype=bool, record='bi')
    @dio2.putter
    async def dio2(self, instance, value: bool):
        self.client.write("DIO", 2, value)
    @dio2.scan(period=6, use_scan_field=True)
    async def dio2(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio2_RBV.write(self.client.read("DIO", 2))

    dio3 = pvproperty(name="dio3", doc="Bidirectional digital in/out pin 3", dtype=bool, record='bi')
    dio3_RBV = pvproperty(name="dio3_RBV", doc="Readback value for bidirectional digital in/out pin 3", dtype=bool, record='bi')
    @dio3.putter
    async def dio3(self, instance, value: bool):
        self.client.write("DIO", 3, value)
    @dio3.scan(period=6, use_scan_field=True)
    async def dio3(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio3_RBV.write(self.client.read("DIO", 3))

    dio4 = pvproperty(name="dio4", doc="Bidirectional digital in/out pin 4", dtype=bool, record='bi')
    dio4_RBV = pvproperty(name="dio4_RBV", doc="Readback value for bidirectional digital in/out pin 4", dtype=bool, record='bi')
    @dio4.putter
    async def dio4(self, instance, value: bool):
        self.client.write("DIO", 4, value)
    @dio4.scan(period=6, use_scan_field=True)
    async def dio4(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio4_RBV.write(self.client.read("DIO", 4))

    dio5 = pvproperty(name="dio5", doc="Bidirectional digital in/out pin 5", dtype=bool, record='bi')
    dio5_RBV = pvproperty(name="dio5_RBV", doc="Readback value for bidirectional digital in/out pin 5", dtype=bool, record='bi')
    @dio5.putter
    async def dio5(self, instance, value: bool):
        self.client.write("DIO", 5, value)
    @dio5.scan(period=6, use_scan_field=True)
    async def dio5(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio5_RBV.write(self.client.read("DIO", 5))

    dio6 = pvproperty(name="dio6", doc="Bidirectional digital in/out pin 6", dtype=bool, record='bi')
    dio6_RBV = pvproperty(name="dio6_RBV", doc="Readback value for bidirectional digital in/out pin 6", dtype=bool, record='bi')
    @dio6.putter
    async def dio6(self, instance, value: bool):
        self.client.write("DIO", 6, value)
    @dio6.scan(period=6, use_scan_field=True)
    async def dio6(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio6_RBV.write(self.client.read("DIO", 6))

    dio7 = pvproperty(name="dio7", doc="Bidirectional digital in/out pin 7", dtype=bool, record='bi')
    dio7_RBV = pvproperty(name="dio7_RBV", doc="Readback value for bidirectional digital in/out pin 7", dtype=bool, record='bi')
    @dio7.putter
    async def dio7(self, instance, value: bool):
        self.client.write("DIO", 7, value)
    @dio7.scan(period=6, use_scan_field=True)
    async def dio7(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.dio7_RBV.write(self.client.read("DIO", 7))


    di0 = pvproperty(name="di0", doc="Digital input pin 0", dtype=bool, record='bo')   
    @di0.scan(period=6, use_scan_field=True)
    async def di0(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.di0.write(self.client.read("DI", 0))

    di1 = pvproperty(name="di1", doc="Digital input pin 1", dtype=bool, record='bo')   
    @di1.scan(period=6, use_scan_field=True)
    async def di1(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.di1.write(self.client.read("DI", 1))

    di2 = pvproperty(name="di2", doc="Digital input pin 2", dtype=bool, record='bo')   
    @di2.scan(period=6, use_scan_field=True)
    async def di2(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.di2.write(self.client.read("DI", 2))

    di3 = pvproperty(name="di3", doc="Digital input pin 3", dtype=bool, record='bo')   
    @di3.scan(period=6, use_scan_field=True)
    async def di3(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.di3.write(self.client.read("DI", 3))

    di4 = pvproperty(name="di4", doc="Digital input pin 4", dtype=bool, record='bo')   
    @di4.scan(period=6, use_scan_field=True)
    async def di4(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.di4.write(self.client.read("DI", 4))

    di5 = pvproperty(name="di5", doc="Digital input pin 5", dtype=bool, record='bo')   
    @di5.scan(period=6, use_scan_field=True)
    async def di5(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.di5.write(self.client.read("DI", 5))

    di6 = pvproperty(name="di6", doc="Digital input pin 6", dtype=bool, record='bo')   
    @di6.scan(period=6, use_scan_field=True)
    async def di6(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.di6.write(self.client.read("DI", 6))

    di7 = pvproperty(name="di7", doc="Digital input pin 7", dtype=bool, record='bo')   
    @di7.scan(period=6, use_scan_field=True)
    async def di7(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.di7.write(self.client.read("DI", 7))

    ao0 = pvproperty(name="ao0", doc="Analog output 0, can be 0-10V", dtype=float, record='ai')
    ao0_RBV = pvproperty(name="ao0_RBV", doc="Readback value for analog output 0", dtype=float, record='ai')
    @ao0.putter
    async def ao0(self, instance, value: float):
        self.client.write("AO", 0, value)
    @ao0.scan(period=6, use_scan_field=True)
    async def ao0(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.ao0_RBV.write(self.client.read("AO", 0))

    ao1 = pvproperty(name="ao1", doc="Analog output 1, can be 0-10V", dtype=float, record='ai')
    ao1_RBV = pvproperty(name="ao1_RBV", doc="Readback value for analog output 1", dtype=float, record='ai')
    @ao1.putter
    async def ao1(self, instance, value: float):
        self.client.write("AO", 1, value)
    @ao1.scan(period=6, use_scan_field=True)
    async def ao1(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.ao1_RBV.write(self.client.read("AO", 1))

    ao2 = pvproperty(name="ao2", doc="Analog output 2, can be 0-10V", dtype=float, record='ai')
    ao2_RBV = pvproperty(name="ao2_RBV", doc="Readback value for analog output 2", dtype=float, record='ai')
    @ao2.putter
    async def ao2(self, instance, value: float):
        self.client.write("AO", 2, value)
    @ao2.scan(period=6, use_scan_field=True)
    async def ao2(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.ao2_RBV.write(self.client.read("AO", 2))

    ao3 = pvproperty(name="ao3", doc="Analog output 3, can be 0-10V", dtype=float, record='ai')
    ao3_RBV = pvproperty(name="ao3_RBV", doc="Readback value for analog output 3", dtype=float, record='ai')
    @ao3.putter
    async def ao3(self, instance, value: float):
        self.client.write("AO", 3, value)
    @ao3.scan(period=6, use_scan_field=True)
    async def ao3(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.ao3_RBV.write(self.client.read("AO", 3))


    ai0 = pvproperty(name="ai0", doc="Analog input 0, can be 0-10V", dtype=float, record='ao')
    @ai0.scan(period=6, use_scan_field=True)
    async def ai0(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.ai0.write(self.client.read("AI", 0))

    ai1 = pvproperty(name="ai1", doc="Analog input 1, can be 0-10V", dtype=float, record='ao')
    @ai1.scan(period=6, use_scan_field=True)
    async def ai1(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.ai1.write(self.client.read("AI", 1))

    ai2 = pvproperty(name="ai2", doc="Analog input 2, can be 0-10V", dtype=float, record='ao')
    @ai2.scan(period=6, use_scan_field=True)
    async def ai2(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.ai2.write(self.client.read("AI", 2))

    t0 = pvproperty(name="t0", doc="Temperature sensor 0 (degrees C)", dtype=float, record='ao')
    @t0.scan(period=6, use_scan_field=True)
    async def t0(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.t0.write(self.client.read("SENSOR temp", 0))

    t1 = pvproperty(name="t1", doc="Temperature sensor 1 (degrees C)", dtype=float, record='ao')
    @t1.scan(period=6, use_scan_field=True)
    async def t1(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.t1.write(self.client.read("SENSOR temp", 1))

    t2 = pvproperty(name="t2", doc="Temperature sensor 2 (degrees C)", dtype=float, record='ao')
    @t2.scan(period=6, use_scan_field=True)
    async def t2(self, instance: ChannelData, async_lib: AsyncLibraryLayer):
        await self.t2.write(self.client.read("SENSOR temp", 2))


def main(args=None):
    parser, split_args = template_arg_parser(
        default_prefix="Portenta:",
        desc="EPICS IOC for accessing I/O on the Arduino Portenta Machine Control (PMC) over network",
    )

    if args is None:
        args = sys.argv[1:]

    parser.add_argument("--host", required=True, type=str, help="IP address of the host/device")
    parser.add_argument("--port", required=True, type=int, help="Port number of the device")

    args = parser.parse_args()

    logging.info("Running Networked Portenta IOC")

    ioc_options, run_options = split_args(args)
    ioc = PortentaIOC(host=args.host, port=args.port, **ioc_options)
    run(ioc.pvdb, **run_options)


if __name__ == "__main__":
    main()
