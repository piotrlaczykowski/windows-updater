from dell_support_assist import *
from msi import *
from utilities import *


def motherboard_launcher():
    if "Dell" in mobo_manufacturer():
        dell()
    elif "Micro-Star" in mobo_manufacturer():
        msi()

