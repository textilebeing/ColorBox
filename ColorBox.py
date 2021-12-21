'''
                               o
                          o    |
                           \   |
                            \  |
                             \.|-.
                             (\|  )
                    .==================.
                    | .--------------. |
                    | |::.::.::.::.::| |
                    | |'::'::'::'::':| |
                    | |::.::.::.::.::| |
                    | |:'::'::'::'::'| |
                    | |::.::.::.::.::| |
                    | '--------------'o|
                    | LI LI """""""   o|
                    |==================|
                    |  .------------.  |
                    | /              \ |
                    |/                \|
                    "                  "


░█████╗░░█████╗░██╗░░░░░░█████╗░██████╗░██████╗░░█████╗░██╗░░██╗
██╔══██╗██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝
██║░░╚═╝██║░░██║██║░░░░░██║░░██║██████╔╝██████╦╝██║░░██║░╚███╔╝░
██║░░██╗██║░░██║██║░░░░░██║░░██║██╔══██╗██╔══██╗██║░░██║░██╔██╗░
╚█████╔╝╚█████╔╝███████╗╚█████╔╝██║░░██║██████╦╝╚█████╔╝██╔╝╚██╗
░╚════╝░░╚════╝░╚══════╝░╚════╝░╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝

'''


from Graphics50 import *
from ColorBox_funcs import *
import random
from PIL import *


"""
Calls all functions together so the workflow is this:
- User defines size of window
- User defines what shapes they want.
- Program generates a random number of shapes at a random number of sizes
- Program will generate this shapes with random colors as well
- Might develop a palette generator? Could be cool
- Program then writes these shapes to the window and displays them
- Program will save new image as collage.
"""

"""
Tasks/Functions needed:
1. Create GUI window for user inputs.
2. Get user inputs
3. Use user inputs for PIL canvas
4. Generate shapes and colors.
5. Put all shapes and colors onto PIL canvas
6. Display and Save PIL canvas

"""


class ColorBox:
    """
    Okay, my idea with ColorBox is that I wanted it all under one class,
    similar to my Annealing Simulator Final. This makes it so variables can
    be shared between functions.

    """

    def __init__(self, WIN_H=500, WIN_W=500, WIN_TITLE="ColorBox v2"):
        """
        with the __init__, the object establishes it's size and title.
        it also establishes some constants that will be used throughout the
        class objects functions.

        """
        if (WIN_W or WIN_H) < 500:
            self.WIN_W = self.WIN_H = 500
        else:
            self.WIN_H = WIN_H
            self.WIN_W = WIN_W

        self.WIN_TITLE = WIN_TITLE
        self.BOTTOM = 50
        self.COLORS = [
            "black",
            "red",
            "green",
            "blue",
            "white",
            "beige",
            "blue violet",
            "dark olive green",
            "dark orange",
            "deep pink",
            "forest green",
            "lavender",
            "khaki",
            "rebecca purple",
            "plum",
            "peru",
            "powder blue",
        ]

        self._GUI_setup()  # Set up GUI elements

    def btn_check(self):
        """
        Checks for click within buttons and performs appropriate actions if true
        """

        if btn_clicked(self.pt, self.btn_Gen):
            self.click_info.setText("GENERATING...")
            self.click_info.setTextColor(color_rgb(235, 219, 178))
            # self.pt = self.win.getMouse()        # Get click, delays quit
            return True  # Indicates to main that quit clicked

        if btn_clicked(self.pt, self.btn_Quit):
            self.click_info.setText("QUITTING...")
            # self.pt = self.win.getMouse()        # Get click, delays quit
            return False  # Indicates to main that quit clicked

    def display(self, palette=-1):
        """
        Main display function for the color box, contains the main While loop
        for display and GUI functions. Maybe temporary?
        """

        self.palette = palette
        self.click_info.setText("Enter a Number")
        self.click_info.setTextColor(color_rgb(235, 219, 178))

        while True:  # Main While Loop
            self.pt = self.win.getMouse()
            n = self._getEntryNum()
            if n == None:
                n = 0

            if self.btn_check() == False:
                break

            if self.btn_check() == True:
                self.drawer(n)

    def _getEntryNum(self):
        """
        function for returning number from the entrybox for number of shapes.

        # TODO
        # Add in selection for shapes. with feedback eg.  "{shape} off"
        """
        try:
            n = self.entryBox.getText()
            n = int(n)
            return n
        except:
            self.click_info.setText("Error, Try Again")

    def _GUI_setup(self):
        """
        user defines the size of "drawing" that they want generated
        """

        self.win = GraphWin(
            self.WIN_TITLE, self.WIN_W, self.WIN_H + self.BOTTOM
        )

        background = Rectangle(Point(0, 0), Point(self.WIN_W, self.WIN_H))
        background.setFill(color_rgb(60, 56, 54))
        background.draw(self.win)

        self.bottom = Rectangle(
            Point(0, self.WIN_H), Point(self.WIN_W, self.WIN_H + 50)
        )
        self.bottom.setFill(color_rgb(146, 131, 116))
        self.bottom.draw(self.win)

        self.btn_Gen = btn_create(
            self.win, 0, self.WIN_H, self.WIN_W * 0.33, 50, "GENERATE"
        )  # Gen btn

        self.btn_Quit = btn_create(
            self.win,
            self.WIN_W * 0.66,
            self.WIN_H,
            self.WIN_W * 0.34,
            50,
            "QUIT",
        )  # Reset btn

        self.click_info = Text(Point(self.WIN_W * 0.5, self.WIN_H + 20), " ")
        self.click_info.draw(self.win)  # Display click_info

        self.entryBox = Entry(Point(self.WIN_W * 0.5, self.WIN_H + 40), 5)
        self.entryBox.draw(self.win)

        return

    def circ_gen(self):
        """
        Randomly generates a circle and places it within the window,
        one circle is generated each time the function is called.
        """

        x1 = random.randint(0, self.WIN_W)
        y1 = random.randint(0, self.WIN_H - 30)
        r = random.randint(0, (self.WIN_H + self.WIN_W) // 4)
        c = Circle(Point(x1, y1), r)

        self._color_set_and_fill(c)

    def _color_set_and_fill(self, shape):
        if self.palette == -1:
            color = self._color_gen()
        else:
            color = self._palette(self.palette)

        shape.setFill(color_rgb(color[0], color[1], color[2]))
        shape.setOutline(color_rgb(color[0], color[1], color[2]))
        shape.draw(self.win)

    def tri_gen(self):
        """
        Function generates amount of triangles, sizes, and placement
        in the window.
        """

        p1x = random.randint(0, self.WIN_W)
        p2x = random.randint(0, self.WIN_W)
        p3x = random.randint(0, self.WIN_W)
        p1y = random.randint(0, self.WIN_H)
        p2y = random.randint(0, self.WIN_H)
        p3y = random.randint(0, self.WIN_H)

        p = Polygon(Point(p1x, p1y), Point(p2x, p2y), Point(p3x, p3y))
        self._color_set_and_fill(p)

    def oval_gen(self):
        x1 = random.randint(0, self.WIN_W)
        y1 = random.randint(0, self.WIN_H)
        y2 = random.randint(y1, self.WIN_H)
        x2 = random.randint(x1, self.WIN_W)

        if (abs(x1 - x2)) < 100:
            x1 -= 20
        if (abs(y1 - y2)) < 100:
            y1 -= 20

        o = Oval(Point(x1, y1), Point(x2, y2))
        self._color_set_and_fill(o)

    def poly_gen(self):
        """
        Function generates amount of polygons, sizes, and placement
        in the window.
        """
        poly_coords = self._random_coord_generator(4)

        p = Polygon(
            Point(poly_coords[0][0], poly_coords[1][0]),
            Point(poly_coords[0][1], poly_coords[1][1]),
            Point(poly_coords[0][2], poly_coords[1][2]),
            Point(poly_coords[0][3], poly_coords[1][3]),
        )

        self._color_set_and_fill(p)

    def _random_coord_generator(self, n):
        """
        Generates a pair of x and y coordinates, times n amount.
        """
        px = []
        py = []
        for x in range(n):
            px.append(random.randint(0, self.WIN_W))
            py.append(random.randint(0, self.WIN_H))
        return (px, py)

    def rect_gen(self):

        self.rect_coords = self._random_coord_generator(2)

        r = Rectangle(
            (Point(self.rect_coords[0][0], self.rect_coords[1][0])),
            (Point(self.rect_coords[0][1], self.rect_coords[1][1])),
        )

        self._color_set_and_fill(r)

    def _rect_thickener(self):
        if (abs(self.rect_coords[0][0] - self.rect_coords[0][1])) < 100:
            self.rect_coords[0][0] -= 20

        if (abs(self.rect_coords[1][0] - self.rect_coords[1][1])) < 100:
            self.rect_coords[1][0] -= 20

    def _color_gen(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)
        return color

    def drawer(self, n):
        """
        function that draws the shapes to the window, can be called again with
        a click in the window, for another drawing.
        """
        background = Rectangle(Point(0, 0), Point(self.WIN_W, self.WIN_H))
        background.setFill(color_rgb(60, 56, 54))
        background.draw(self.win)

        for i in range(n):
            self.rect_gen()
            time.sleep(0.01)
            self.tri_gen()
            time.sleep(0.01)
            self.oval_gen()
            time.sleep(0.01)
            # self.poly_gen()
            # time.sleep(0.01)

        self.click_info.setTextColor(color_rgb(235, 219, 178))
        self.click_info.setText("Done.")

    def _palette(self, palette):
        """
        I guess I'll put palettes in here. It's annoying to add these,
        so gruvbox will be my test palette.
        """

        gruvbox = [
            (40, 40, 40),  # black
            (146, 131, 116),  # gray1
            (204, 36, 29),  # red1,
            (251, 73, 52),  # red2,
            (152, 151, 26),  # green1
            (184, 187, 38),  # green2
            (215, 153, 33),  # yellow1
            (250, 189, 47),  # yellow2
            (69, 133, 136),  # blue1
            (131, 165, 152),  # blue2
            (177, 98, 134),  # purple1
            (104, 157, 106),  # purple2
            (142, 192, 124),  # aqua1
            (168, 153, 132),  # aqua2
            (235, 219, 178),  # gray2
            (214, 93, 14),  # orange1
            (254, 128, 25),  # orange2
        ]

        if palette == "gruvbox":
            return random.choice(gruvbox)


def test():
    color_box = ColorBox(100, 100, "ColorBox v2 - NEW (With Buttons!)")
    color_box._random_coord_generator(4)
    color_box.display("gruvbox")

    # color_box.win.getMouse()
    color_box.win.close()


test()
