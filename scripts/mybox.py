import sys

sys.path.append('..')  # uncomments and adjust if your Boxes.py copy in not in the Python path
from boxes import *
from boxes import lids
from boxes.lids import _TopEdge


class MyUniversalBox(_TopEdge):
    """Box with various options for different styles and lids"""

    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addTopEdgeSettings(roundedtriangle={"outset": 1},
                                hinge={"outset": True})
        self.addSettingsArgs(edges.FlexSettings)
        self.addSettingsArgs(lids.LidSettings)
        self.buildArgParser("top_edge", "bottom_edge",
                            "x", "y", "h", "outside")
        self.argparser.add_argument(
            "--vertical_edges", action="store", type=str,
            default="finger joints",
            choices=("finger joints", "finger holes"),
            help="connections used for the vertical edges")

    def left_wall_holes(self, h_hole_usb=7.5):
        hole_width = 16
        self.rectangularHole(self.y - hole_width - 0.1, self.h - h_hole_usb + self.thickness, hole_width + 1, h_hole_usb + 1, center_y=False,
                             center_x=False)
        x_step, hole_size = 4, 1.5
        nc = 14
        offset = (self.y - nc * x_step) / 2
        for i in range(nc):
            self.rectangularHole(offset + i * x_step, self.h / 2, hole_size, self.h / 4)

    def render(self):
        x, y, h = self.x, self.y, self.h

        tl, tb, tr, tf = self.topEdges(self.top_edge)
        b = self.edges.get(self.bottom_edge, self.edges["F"])

        sideedge = "F" if self.vertical_edges == "finger joints" else "h"

        if self.outside:
            self.x = x = self.adjustSize(x, sideedge, sideedge)
            self.y = y = self.adjustSize(y)
            self.h = h = self.adjustSize(h, b, self.top_edge)

        with self.saved_context():
            self.rectangularWall(x, h, [b, sideedge, tf, sideedge],
                                 ignore_widths=[1, 6],
                                 move="up", label="front", callback=[])
            self.rectangularWall(x, h, [b, sideedge, tb, sideedge],
                                 ignore_widths=[1, 6],
                                 move="up", label="back", callback=[])

            callback_bottom = lambda: self.hole(self.x / 2, 70, r=7.05)
            self.rectangularWall(x, y, "ffff", move="up", label="Bottom", callback=[callback_bottom])
            self.lid(x, y, self.top_edge)

        self.rectangularWall(x, h, [b, sideedge, tf, sideedge],
                             ignore_widths=[1, 6],
                             move="right only", label="invisible")
        self.rectangularWall(y, h, [b, "f", tl, "f"],
                             ignore_widths=[1, 6],
                             move="up", label="left", callback=[self.left_wall_holes])
        self.rectangularWall(y, h, [b, "f", tr, "f"],
                             ignore_widths=[1, 6],
                             move="up", label="right", callback=[])


thickness = 4.0
x = 45
y = 120
z = 30

file_format = "svg"

b = MyUniversalBox()
b.parseArgs(['--reference=0', '--FingerJoint_finger=4', '--FingerJoint_surroundingspaces=2', '--FingerJoint_space=4',
             f'--format={file_format}', '--debug=0', f'--thickness={thickness}', '--top_edge=F', '--bottom_edge=F',
             f'--x={x}', f'--y={y}', f'--h={z}', '--outside=1', '--Hinge_style=flush'])
# b.parseArgs()
b.open()
b.render()
data = b.close()

with open(f'flashlight.{file_format}', "wb") as f:
    f.write(data.getbuffer())
