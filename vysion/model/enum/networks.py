from enum import Enum

class Network(str, Enum):

    tor = "tor"
    i2p = "i2p"
    zeronet = "zeronet"
    freenet = "freenet"
    paste = "paste"
    clearnet = "clearnet"
    graynet = "graynet"