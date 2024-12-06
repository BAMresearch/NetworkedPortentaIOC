
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

    # digital outputs ("DO")
    do0 = pvproperty(name="do0", doc="Digital output 0, can be 0 or 1", dtype=bool, record='bi')   
    @do0.putter
    async def do0(self, instance, value: bool):
        self.client.write("DO", 0, value)
    @do0.scan(period=6, use_scan_field=True)
    async def do0(self, instance:ChannelData, async_lib: AsyncLibraryLayer):
        self.do0.write(self.client.read("DO", 0))
    # do1 = pvproperty(name="do1", doc="Digital output 1, can be 0 or 1", dtype=bool, record='bi')
    # do2 = pvproperty(name="do2", doc="Digital output 2, can be 0 or 1", dtype=bool, record='bi')
    # do3 = pvproperty(name="do3", doc="Digital output 3, can be 0 or 1", dtype=bool, record='bi')
    # do4 = pvproperty(name="do4", doc="Digital output 4, can be 0 or 1", dtype=bool, record='bi')
    # do5 = pvproperty(name="do5", doc="Digital output 5, can be 0 or 1", dtype=bool, record='bi')
    # do6 = pvproperty(name="do6", doc="Digital output 6, can be 0 or 1", dtype=bool, record='bi')
    # do7 = pvproperty(name="do7", doc="Digital output 7, can be 0 or 1", dtype=bool, record='bi')
    # do0_RBV = pvproperty(name="do0_RBV", doc="Digital output 0 readback value, can be 0 or 1", dtype=bool, record='bo')   
    # do1_RBV = pvproperty(name="do1_RBV", doc="Digital output 1 readback value, can be 0 or 1", dtype=bool, record='bo')
    # do2_RBV = pvproperty(name="do2_RBV", doc="Digital output 2 readback value, can be 0 or 1", dtype=bool, record='bo')
    # do3_RBV = pvproperty(name="do3_RBV", doc="Digital output 3 readback value, can be 0 or 1", dtype=bool, record='bo')
    # do4_RBV = pvproperty(name="do4_RBV", doc="Digital output 4 readback value, can be 0 or 1", dtype=bool, record='bo')
    # do5_RBV = pvproperty(name="do5_RBV", doc="Digital output 5 readback value, can be 0 or 1", dtype=bool, record='bo')
    # do6_RBV = pvproperty(name="do6_RBV", doc="Digital output 6 readback value, can be 0 or 1", dtype=bool, record='bo')
    # do7_RBV = pvproperty(name="do7_RBV", doc="Digital output 7 readback value, can be 0 or 1", dtype=bool, record='bo')

    # # bidirectional digital pins (input/output) ("DIO")
    # dio0 = pvproperty(name="dio0", doc="Digital i/o 0, can be 0 or 1", dtype=bool, record='bi')   
    # dio1 = pvproperty(name="dio1", doc="Digital i/o 1, can be 0 or 1", dtype=bool, record='bi')
    # dio2 = pvproperty(name="dio2", doc="Digital i/o 2, can be 0 or 1", dtype=bool, record='bi')
    # dio3 = pvproperty(name="dio3", doc="Digital i/o 3, can be 0 or 1", dtype=bool, record='bi')
    # dio4 = pvproperty(name="dio4", doc="Digital i/o 4, can be 0 or 1", dtype=bool, record='bi')
    # dio5 = pvproperty(name="dio5", doc="Digital i/o 5, can be 0 or 1", dtype=bool, record='bi')
    # dio6 = pvproperty(name="dio6", doc="Digital i/o 6, can be 0 or 1", dtype=bool, record='bi')
    # dio7 = pvproperty(name="dio7", doc="Digital i/o 7, can be 0 or 1", dtype=bool, record='bi')
    # dio0_RBV = pvproperty(name="dio0_RBV", doc="Digital i/o 0 readback value, can be 0 or 1", dtype=bool, record='bo')   
    # dio1_RBV = pvproperty(name="dio1_RBV", doc="Digital i/o 1 readback value, can be 0 or 1", dtype=bool, record='bo')
    # dio2_RBV = pvproperty(name="dio2_RBV", doc="Digital i/o 2 readback value, can be 0 or 1", dtype=bool, record='bo')
    # dio3_RBV = pvproperty(name="dio3_RBV", doc="Digital i/o 3 readback value, can be 0 or 1", dtype=bool, record='bo')
    # dio4_RBV = pvproperty(name="dio4_RBV", doc="Digital i/o 4 readback value, can be 0 or 1", dtype=bool, record='bo')
    # dio5_RBV = pvproperty(name="dio5_RBV", doc="Digital i/o 5 readback value, can be 0 or 1", dtype=bool, record='bo')
    # dio6_RBV = pvproperty(name="dio6_RBV", doc="Digital i/o 6 readback value, can be 0 or 1", dtype=bool, record='bo')
    # dio7_RBV = pvproperty(name="dio7_RBV", doc="Digital i/o 7 readback value, can be 0 or 1", dtype=bool, record='bo')

    # # digital inputs ("DI")
    # di0_RBV = pvproperty(name="di0_RBV", doc="Digital input 0 readback value, can be 0 or 1", dtype=bool, record='bo')   
    # di1_RBV = pvproperty(name="di1_RBV", doc="Digital input 1 readback value, can be 0 or 1", dtype=bool, record='bo')
    # di2_RBV = pvproperty(name="di2_RBV", doc="Digital input 2 readback value, can be 0 or 1", dtype=bool, record='bo')
    # di3_RBV = pvproperty(name="di3_RBV", doc="Digital input 3 readback value, can be 0 or 1", dtype=bool, record='bo')
    # di4_RBV = pvproperty(name="di4_RBV", doc="Digital input 4 readback value, can be 0 or 1", dtype=bool, record='bo')
    # di5_RBV = pvproperty(name="di5_RBV", doc="Digital input 5 readback value, can be 0 or 1", dtype=bool, record='bo')
    # di6_RBV = pvproperty(name="di6_RBV", doc="Digital input 6 readback value, can be 0 or 1", dtype=bool, record='bo')
    # di7_RBV = pvproperty(name="di7_RBV", doc="Digital input 7 readback value, can be 0 or 1", dtype=bool, record='bo')

    # # analog outputs ("AO")
    # ao0 = pvproperty(name="ao0", doc="Analog output 0, can be 0-10V", dtype=float, record='ai')   
    # ao1 = pvproperty(name="ao1", doc="Analog output 1, can be 0-10V", dtype=float, record='ai')
    # ao2 = pvproperty(name="ao2", doc="Analog output 2, can be 0-10V", dtype=float, record='ai')
    # ao3 = pvproperty(name="ao3", doc="Analog output 3, can be 0-10V", dtype=float, record='ai')

    # # analog inputs ("AI")
    # ai0_RBV = pvproperty(name="ai0_RBV", doc="Analog input 0 readback value, can be 0-10V", dtype=float, record='ao')   
    # ai1_RBV = pvproperty(name="ai1_RBV", doc="Analog input 1 readback value, can be 0-10V", dtype=float, record='ao')
    # ai2_RBV = pvproperty(name="ai2_RBV", doc="Analog input 2 readback value, can be 0-10V", dtype=float, record='ao')

    # # temperature sensors (PT100)
    # t0_RBV = pvproperty(name="t0_RBV", doc="temperature sensor 0 (degrees C)", dtype=float, record='ao')
    # t1_RBV = pvproperty(name="t1_RBV", doc="temperature sensor 1 (degrees C)", dtype=float, record='ao')
    # t2_RBV = pvproperty(name="t2_RBV", doc="temperature sensor 2 (degrees C)", dtype=float, record='ao')


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
