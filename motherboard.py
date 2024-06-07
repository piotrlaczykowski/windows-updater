from dell import *
from msi import *
from utilities import *


def motherboard_launcher():
    if "Dell "in mobo_manufacturer():
        dell() # type: ignore
    elif "Micro-Star" in mobo_manufacturer:
        msi()

