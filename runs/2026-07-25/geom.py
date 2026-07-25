"""geom.py — the one projection, shared by the generator and the slide code.

AXONOMETRIC ORTHOGRAPHIC. Azimuth 14 deg, pitch 31.75 deg.

The first build used azimuth 0, which projects the slab's top face to an
axis-aligned RECTANGLE. It rendered flat: no left wall, no visible corner, no
volume, and the contact sheet read as pale bands rather than a milled solid.
Adding a 14 deg azimuth turns every face into a parallelogram, so the object
gains a visible second side face and every recess shows two interior walls
instead of one. Still a PARALLEL projection, so cut lengths keep encoding
dollars honestly (doctrine forbids perspective on quantities).

    screen_x = 540 + S * (0.9703 x - 0.2419 z)
    screen_y = ACY + S * (0.1273 x + 0.5106 z - 0.8505 y)

Derivation: right = (cos14, 0, -sin14); the screen-down basis picks up
sin(pitch) on both x and z through the azimuth rotation, and cos(pitch) on y.
A unit length along the slab's x axis projects to S * 0.9786 px, so the money
scale below is stated in screen px and converted once.
"""
import math

S = 259.1
ACY = 905.0
AZ = math.radians(14.0)
PITCH = math.radians(31.75)
KX, KZ = math.cos(AZ), -math.sin(AZ)                      # 0.9703, -0.2419
MX = math.sin(PITCH) * math.sin(AZ)                       # 0.1273
MZ = math.sin(PITCH) * math.cos(AZ)                       # 0.5106
MY = math.cos(PITCH)                                      # 0.8505

# slab, world units
SLAB_X, SLAB_Z, SLAB_TH = 1.50, 1.15, 0.30
RECESS = 0.16                                             # 35.3 px of wall

# money: 165.6 screen px per 1 million dollars, measured along the slab x axis
PX_PER_M = 165.6
XSCALE = S * math.hypot(KX, MX)                           # 253.6 px per unit x
W_PER_M = PX_PER_M / XSCALE                               # 0.6530 units per M
WELL_X0 = -1.42                                           # every well left-aligns


def sx(x, z):
    return 540.0 + S * (KX * x + KZ * z)


def sy(x, y, z):
    return ACY + S * (MX * x + MZ * z - MY * y)


def wend(m):
    """x where a well encoding m million dollars ends."""
    return WELL_X0 + m * W_PER_M
