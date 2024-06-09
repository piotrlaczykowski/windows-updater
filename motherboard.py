from dell_support_assist import *
from msi import *
from utilities import *


def motherboard_launcher():
    motherboard = mobo_manufacturer()
    if "Dell" in motherboard:
        dell()
    elif "Micro-Star" in motherboard:
        msi()

