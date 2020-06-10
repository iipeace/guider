import os
from .guider import main

# set main environment #
os.environ["ISMAIN"] = "True"

main(args=None)

