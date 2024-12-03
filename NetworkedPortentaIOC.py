import logging
import socket
import struct
import sys

from datetime import datetime, timezone
from caproto import ChannelData
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
    Communicates with the pressure guage
    """

    message = f"GET {bus} {pin}\n"
    sock = connection(address, port)
    sock.sendall(message)
    message_received = sock.recv(1024)
    sock.close()

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
        for DOPort in range(8):
            tempattr = pvproperty(
                value=0,
                name="do{DOPort}",
                doc=f"Digital output {DOPort}, can be 'Low' or 'High'",
                record='bo',
                enum_strings=['Low', 'High']
            )

            @tempattr.putter
            async def tempattr(self, instance, value):
                print(f"Setting DO{DOPort} to {value}")
                await instance.write(value)

            setattr(self, f"do{DOPort}", tempattr)

    timestamp = pvproperty(
        value=str(datetime.now(timezone.utc).isoformat()),
        name="timestamp",
        doc="Timestamp of portenta readout",
        dtype=PvpropertyString,
    )

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