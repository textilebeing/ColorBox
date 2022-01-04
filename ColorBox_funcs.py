# print("GUI_Funcs_L6F21.py  1.03  211015  S. T. U. Dent") # VER TO BE FIXED
"""*****************************************************************************
 This provides a few constants and support functions for the graphics.py-based 
 GUI labs, to be completed, as well as a bit of test code at the bottom:
 - COLORS = ( 'black' ... )
 - [ Rect, Text ] = btn_create(win, x, y, w, h, txt)
 
 The following functions return True ... if:
 - in_Rectangle(pt, r)      : Point pt is inside Rectangle r
 - btn_clicked(pt, btn)     : Point pt is inside button btn
 - in_Circle(pt, c)         : Point pt is inside Circle c
 - in_Triangle(pt, A, B, C) : pt inside triangle A-B-C.  Complete.
 
EX. USAGE
- run this to see short test code
- from GUI_Funcs_L6F21 import *
 
DEPENDENCIES
 - Graphics50.py
*****************************************************************************"""

from Graphics50 import *

COLORS = ["black", "red", "green", "bluie", "white"]


"""-----------------------------------------------------------------------------
 SYNTAX: (Rect, Text) = btn_create(win, x, y, w, h, txt)
 This returns a tuple consisting of a Rectangle and Text objects, defined by
 the supplied parameters:
  - win          : GraphWin-type window in which to crreate the button
  - x1, y1, w, h : upper-left corner, width, height of Rectangle object
  - txt          : string displayed centered inside Rectangle
-----------------------------------------------------------------------------"""


def btn_create(win, x, y, w, h, txt, modifier=-1):
    rect = Rectangle(Point(x, y), Point(x + w, y + h))
    rect.draw(win)
    rect.setFill(color_rgb(146, 131, 116))
    text = Text(rect.getCenter(), txt)
    text.setStyle("bold")
    text.setFace("helvetica")
    text.setSize(18)
    text.setFill(color_rgb(235, 219, 178))
    text.draw(win)

    if modifier == "small":
        text.setSize(10)
        text.setStyle("normal")
    return (rect, text)  # Call this tuple a "button"


"""-----------------------------------------------------------------------------
 SYNTAX: bool = in_Rectangle(pt, r) : returns True if pt is inside Rectangle r
 IMP'T this assumes that r.P2() returns (x, y) coordinates which are to the
 right and down relative to r.P1().
-----------------------------------------------------------------------------"""


def in_Rectangle(pt, r):
    x1, y1 = r.getP1().x, r.getP1().y
    x2, y2 = r.getP2().x, r.getP2().y
    return x1 < pt.x < x2 and y1 < pt.y < y2


"""-----------------------------------------------------------------------------
 SYNTAX: bool = btn_clicked(pt, btn) : returns True if pt.x and pt.y are within
 the boundaries of the Rectangle component of btn, where: btn: [Rectangle, Text]
-----------------------------------------------------------------------------"""


def btn_clicked(pt, btn):
    r = btn[0]  # Recall: btn: (Rectangel, Text)
    p1x, p1y = r.getP1().x, r.getP1().y  # P1: Upper left corner
    p2x, p2y = r.getP2().x, r.getP2().y  # P2: Lower right corner
    x, y = pt.x, pt.y
    return p1x < x < p2x and p1y < y < p2y


"""-----------------------------------------------------------------------------
SYNTAX: bool = in_Circle(pt, c) : returns True if Point pt is inside Circle c
i.e. (pt.x - c.getCircle().x)^2 + (pt.y - c.getCircle().y)^2  <  c.getRadius()^2
REFs
- Khan Academy - Circle equation 
  https://www.khanacademy.org/math/geometry/hs-geo-circles
         /hs-geo-circle-expanded-equation/a/circle-equation-review
-----------------------------------------------------------------------------"""


def in_Circle(pt, c):
    center = c.getCenter()
    distance = (
        (pt.getX() - center.getX()) ** 2 + (pt.getY() - center.getY()) ** 2
    ) ** 0.5

    return distance < c.radius


"""-----------------------------------------------------------------------------
 SYNTAX: bool = in_Triangle(pt, A, B, C)     1.03  190908
 Returns True if Point pt is inside triangle defined by Point objects A, B, C.
 
 Underlying principle: linear algebra.
 a) given: origin of triangle defined at A, relative to (0, 0), and independent
    vectors B and C, relative to A, identified by respective points B and C 
    (yes, purposely named the same): B and C define a line going thru them both
 b) any other point D on that line can be defined in terms of B and C by:
      D  = A  +  u * (B-A)  +  v * (C-A) = weighted combin. of vecs B-A and C-A
    (x,y) components:
      Dx = Ax + u * (Bx - Ax) + v * (Cx - Ax)                  (1)
      Dy = Ay + u * (By - Ay) + v * (Cy - Ay)                  (2)
 c) then: any point between A and B can be defined by: 0 < u < 1 and v = 0
          any point between A and C can be defined by: 0 < v < 1 and u = 0
          any point between B and C can be defined by: u + v = 1
 d) thus any point with u or v outside above ranges is outside triangle A-B-C
 e) so, given points D, A, B, C, we must determine u and v, starting from (1-2)
    in matrix form:
       [ Dx-Ax ] = [ Bx-Ax  Cx-Ax ] x [ u ] := Z x [u]  ==>  [u] = inv(Z) x [Dx]
       [ Dy-Ax ]   [ By-Ay  Cy-Ay ]   [ v ]        [v]       [v]            [Dy]
        
    ==> [u] = [ Cy-Ay  Ax-Cx ] x [Dx-Ax]
        [v]   [ Ay-By  Bx-Ax ]   [Dy-Ax]
              ----------------
                   det(Z)
    where: det(Z) = (Cy-Ay)*(Bx-Ax) - (Ay-By)*(Ax-Cx)
    Thus:  u = ( (Cy-Ay)*(Dx-Ax) + (Ax-Cx)*(Dy-Ay) ) / det(Z)
           v = ( (Ay-By)*(Dx-Ax) + (Bx-Ax)*(Dy-Ay) ) / det(Z)
           
    THEREFORE, point D is INSIDE the triangle A-B-C, IF:
        u > 0 and v > 0 and (u + v < 1)
        
 REFs: 
 - Barycentric Technique, at: http://blackpawn.com/texts/pointinpoly
 - Barycentric Coordinates and Point in Triangle Tests 
   https://blogs.msdn.microsoft.com/rezanour/2011/08/07
          /barycentric-coordinates-and-point-in-triangle-tests/ 
-----------------------------------------------------------------------------"""


def in_Triangle(pt, A, B, C):
    Ax, Bx, Cx, Dx = A.getX(), B.getX(), C.getX(), pt.getX()
    Ay, By, Cy, Dy = A.getY(), B.getY(), C.getY(), pt.getY()
    det = (Cy - Ay) * (Bx - Ax) - (Ay - By) * (Ax - Cx)
    u = ((Cy - Ay) * (Dx - Ax) + (Ax - Cx) * (Dy - Ay)) / det
    v = ((Ay - By) * (Dx - Ax) + (Bx - Ax) * (Dy - Ay)) / det
    # print('u, v = ' + str((u, v)))                         # Dev check

    return u > 0 and v > 0 and (u + v < 1)


# ===============================================================================
# QK TEST CODE
if __name__ == "__main__":
    WIN_W, WIN_H = 400, 400
    win = GraphWin("GUI_Funcs  2021/10/15", WIN_W, WIN_H)

    A, B, C = Point(200, 100), Point(300, 200), Point(100, 300)
    p = Polygon(A, B, C).draw(win)

    t = Text(
        Point(WIN_W // 2, WIN_H - 40),
        "Click anywhere\non triangle\nor near here to Quit!",
    ).draw(win)

    while True:
        pt = win.getMouse()

        if (
            t.getAnchor().x - 10 < pt.x < t.getAnchor().x + 10
            and t.getAnchor().y - 10 < pt.y < t.getAnchor().y + 10
        ):
            t.setText("CLICK ONCE MORE TO EXIT")
            break

        # if in_Triangle(pt, A, B, C):            # A, B, C: triangle vertices
        # Python trick: Polygon.getPoints() gets list of Point's, and the star
        # "unpacks" to 3 separate Point objects for the 3 parameters:
        if in_Triangle(pt, *p.getPoints()):
            if p.config["fill"] == "red":
                p.setFill("green")
            else:
                p.setFill("red")

    pt = win.getMouse()
    win.close()

# GUI_Funcs_L6F21.py - LOS ENDOS **********************************************
