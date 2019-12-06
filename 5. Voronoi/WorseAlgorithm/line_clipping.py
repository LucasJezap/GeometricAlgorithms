from DataStructures import *
# Python program to implement Cohen Sutherland algorithm
# for line clipping.

# Defining region codes
INSIDE = 0  #0000
LEFT = 1    #0001
RIGHT = 2   #0010
BOTTOM = 4  #0100
TOP = 8     #1000

# Function to compute region code for a point(x,y)
def computeCode(x, y, x0, y0, x1, y1):
    code = INSIDE
    if x < x0:      # to the left of rectangle
        code |= LEFT
    elif x > x1:    # to the right of rectangle
        code |= RIGHT
    if y < y0:      # below the rectangle
        code |= BOTTOM
    elif y > y1:    # above the rectangle
        code |= TOP

    return code


# Implementing Cohen-Sutherland algorithm
# Clipping a line from P1 = (x1, y1) to P2 = (x2, y2)
def cohenSutherlandClip(p1,p2,x0,y0,x1,y1):
    x_max = x1
    y_max = y1
    x_min = x0
    y_min = y0
    # Compute region codes for P1, P2
    code1 = computeCode(p1.x, p1.y, x0, y0, x1, y1)
    code2 = computeCode(p2.x, p2.y, x0, y0, x1, y1)

    while True:

        # If both endpoints lie within rectangle
        if code1 == 0 and code2 == 0:
            return True

        # If both endpoints are outside rectangle
        elif (code1 & code2) != 0:
            return False

        # Some segment lies within the rectangle
        else:

            # Line Needs clipping
            # At least one of the points is outside,
            # select it
            x = 1.0
            y = 1.0
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

                # Find intersection point
            # using formulas y = y1 + slope * (x - x1),
            # x = x1 + (1 / slope) * (y - y1)
            if code_out & TOP:
                # point is above the clip rectangle
                x = p1.x + (p2.x - p1.x) * (y_max - p1.y) / (p2.y - p1.y)
                y = y_max

            elif code_out & BOTTOM:
                # point is below the clip rectangle
                x = p1.x + (p2.x - p1.x) * (y_min - p1.y) / (p2.y - p1.y)
                y = y_min

            elif code_out & RIGHT:
                # point is to the right of the clip rectangle
                y = p1.y + (p2.y - p1.y) * (x_max - p1.x) / (p2.x - p1.x)
                x = x_max
            elif code_out & LEFT:
                # point is to the left of the clip rectangle
                y = p1.y + (p2.y - p1.y) * (x_min - p1.x) / (p2.x - p1.x)
                x = x_min
                # Now intersection point x,y is found
            # We replace point outside clipping rectangle
            # by intersection point
            if code_out == code1:
                p1.x = x
                p1.y = y
                code1=computeCode(p1.x,p1.y,x0,y0,x1,y1)
            else:
                p2.x = x
                p2.y = y
                code2=computeCode(p2.x,p2.y,x0,y0,x1,y1)
