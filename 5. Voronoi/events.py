from decimal import Decimal
import math
from data_structures import *

# klasa symbolizująca zdarzenie
class Event:

    def __init__(self, circle_event=False):
        self.circle_event = circle_event

    # obiekt mniejszy gdy większa współrzędna y, w przypadku remisu mniejsza współrzędna x
    def __lt__(self, other):
        if self.y == other.y and self.x == other.x:
            return self.circle_event and not other.circle_event

        if self.y == other.y:
            return self.x < other.x

        return self.y > other.y

    # obiekty równe, gdy równe współrzędne
    def __eq__(self, other):
        if other is None:
            return None
        return self.y == other.y and self.x == other.x

    def __ne__(self, other):
        return not self.__eq__(other)


# klasa symbolizująca zdarzenie kołowe, dziedziczy z klasy Event
class CircleEvent(Event):
    def __init__(self, center, radius, arc_node, point_triple=None, arc_triple=None):
        super().__init__(True)
        self.center = center
        self.radius = radius
        self.arc_pointer = arc_node
        self.is_valid = True
        self.point_triple = point_triple
        self.arc_triple = arc_triple

    def __str__(self):
        return "CircleEvent " + str(self.point_triple) + " Radius " + str(self.center.y - self.radius)

    # metoda do zaznaczania "fałszywych" zdarzeń
    def remove(self):
        self.is_valid = False
        return self

    @property
    def x(self):
        return self.center.x

    @property
    def y(self):
        return self.center.y - self.radius

    # metoda tworząca nowe zdarzenie kołowe
    @staticmethod
    def create_circle_event(left_node, middle_node, right_node, sweep_line):

        if left_node is None or right_node is None or middle_node is None:
            return None

        left_arc = left_node.get_value()
        middle_arc = middle_node.get_value()
        right_arc = right_node.get_value()

        a, b, c = left_arc.origin, middle_arc.origin, right_arc.origin

        if CircleEvent.create_circle(a, b, c):
            x, y, radius = CircleEvent.create_circle(a, b, c)

            return CircleEvent(Coordinate(x, y), radius, middle_node, (a, b, c), (left_arc, middle_arc, right_arc))

        return None

    # metoda tworząca koło przy pomocy 3 punktów
    @staticmethod
    def create_circle(a, b, c):

        a, b, c = sorted((a, b, c), key=lambda item: item.x)

        A = Decimal(b.x - a.x)
        B = Decimal(b.y - a.y)
        C = Decimal(c.x - a.x)
        D = Decimal(c.y - a.y)
        E = Decimal((b.x - a.x) * (a.x + b.x) + (b.y - a.y) * (a.y + b.y))
        F = Decimal((c.x - a.x) * (a.x + c.x) + (c.y - a.y) * (a.y + c.y))
        G = Decimal(2 * ((b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x)))

        if G == 0:
            return False

        x = (D * E - B * F) / G
        y = (A * F - C * E) / G
        radius = Decimal(math.sqrt(math.pow(Decimal(a.x) - x, 2) + math.pow(Decimal(a.y) - y, 2)))

        return float(x), float(y), float(radius)

# klasa symbolizująca zdarzenie punktowe, dziedziczy po Event
class SiteEvent(Event):
    def __init__(self, point):
        super().__init__()
        self.point = point

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    def __str__(self):
        return "SiteEvent "+str(self.point)