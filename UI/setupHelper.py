#!/usr/bin/python3

# /**
# * @author Abhijeet Padwal
# * @email apadwal@tibco.com
# * @create date 2020-07-02 16: 19: 02
# * @modify date 2020-07-02 16: 19: 02
# * @desc[description]
# */

import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
