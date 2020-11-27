"""Very simple example of grabbing your coordinates every second and printing them to the console."""

from time import sleep
from uoa import UOA

uoa = UOA()
while True:
    coords = uoa.get_coords()
    ns = coords["ns"]
    ew = coords["ew"]
    print(f"{ew}, {ns}")
    sleep(1)