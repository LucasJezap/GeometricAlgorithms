import math_helper
import math
import numpy as np

# klasa symbolizująca punkt
class Coordinate:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __str__(self):
        return "("+str(self.x)+','+str(self.y)+')'


# klasa symbolizująca parabolę
class Arc:
    def __init__(self, origin, circle_event=None):
        self.origin = origin
        self.circle_event = circle_event

    def __str__(self):
        return "Arc with origin in " + str(self.origin)

    # metoda zwracająca liste [y1,y2,...] pozwalajacą narysować parabolę
    def get_plot(self, x, sweepline):
        i = self.origin

        if i.y - sweepline == 0:
            return None

        a = 2 * (i.y - sweepline)
        b = (x ** 2 - 2 * i.x * x + i.x ** 2 + i.y ** 2 - sweepline ** 2)
        y = b / a

        return y


# klasa symbolizująca breakpoint
class Breakpoint:
    def __init__(self, breakpoint, edge=None):
        self.breakpoint = breakpoint
        self.edge = edge

    def __str__(self):
        return "Breakpoint " + str(self.breakpoint[0]) + " and " + str(self.breakpoint[1])

    # metoda sprawdzająca czy istnieje punkt przecięcia
    def does_intersect(self):
        a, b = self.breakpoint
        return not (a.y == b.y and b.x < a.x)

    # metoda znajdująca punkt przecięcia, https://www.cs.hmc.edu/~mbrubeck/voronoi.html
    def get_intersection(self, l, max_y=None):
        i, j = self.breakpoint
        result = Coordinate(0, 0)
        p = i

        a = i.x
        b = i.y
        c = j.x
        d = j.y
        u = 2 * (b - l)
        v = 2 * (d - l)

        if i.y == j.y:
            result.x = (i.x + j.x) / 2

            if j.x < i.x:
                result.y = max_y or float('inf')
                return result

        elif i.y == l:
            result.x = i.x
            p = j
        elif j.y == l:
            result.x = j.x
        else:
            x = -(math.sqrt(
                v * (a ** 2 * u - 2 * a * c * u + b ** 2 * (u - v) + c ** 2 * u) + d ** 2 * u * (v - u) + l ** 2 * (
                        u - v) ** 2) + a * v - c * u) / (u - v)
            result.x = x

        a = p.x
        b = p.y
        x = result.x
        u = 2 * (b - l)

        if u == 0:
            result.y = float("inf")
            return result

        result.y = 1 / u * (x ** 2 - 2 * a * x + a ** 2 + b ** 2 - l ** 2)
        return result


# klasa symbolizująca półkrawędź
class HalfEdge:
    # origin może być zarówno obiektem klasy Vertex jak i Breakpoint
    def __init__(self, incident_point, twin=None, origin=None):
        self.origin = origin
        self.incident_point = incident_point
        self._twin = None
        self.twin = twin
        self.next = None
        self.prev = None
        self.removed = False

    def __str__(self):
        return "HalfEdge. Origin " + str(self.origin) + ", incident point " + str(self.incident_point)

    # metoda ustawia wskaźnik next
    def set_next(self, next):
        if next:
            next.prev = self
        self.next = next

    # metoda zwraca wierzchołek półkrawędzi
    def get_origin(self, y=None, max_y=None):
        if isinstance(self.origin, Vertex):
            return self.origin.position

        if y is not None:
            return self.origin.get_intersection(y, max_y)

        return None

    # getter i setter dla pola _twin
    @property
    def twin(self):
        return self._twin

    @twin.setter
    def twin(self, twin):

        if twin is not None:
            twin._twin = self

        self._twin = twin

# klasa symbolizująca punkt, dziedziczy z Coordinate
class Point(Coordinate):
    def __init__(self, x=None, y=None, first_edge=None):
        super().__init__(x, y)
        self.first_edge = first_edge

    def __str__(self):
        return "Point ("+str(self.x)+","+str(self.y)+")"


# klasa symbolizująca wielokąt
class Polygon:
    def __init__(self, tuples):
        self.points = [Coordinate(x, y) for x, y in tuples]
        self.min_y = min([p.y for p in self.points])
        self.min_x = min([p.x for p in self.points])
        self.max_y = max([p.y for p in self.points])
        self.max_x = max([p.x for p in self.points])
        self.center = Coordinate((self.max_x + self.min_x) / 2, (self.max_y + self.min_y) / 2)
        self.points = self.order_points(self.points)
        self.polygon_vertices = []
        for point in self.points:
            self.polygon_vertices.append(Vertex(point=point))

    # metoda ustawiająca punkty w porządku zgodnym ze wskazówkami zegara
    def order_points(self, points):
        clockwise = sorted(points, key=lambda point: (-180 - math_helper.Math.calculate_angle(point, self.center)) % 360)
        return clockwise

    # metoda zwracająca najbliższy wierzchołek do podanego
    def get_closest_point(self, position, points):
        distances = [math_helper.Math.distance(position, p) for p in points]
        index = np.argmin(distances)
        return points[index]

    # metoda dokańczająca lub skracająca linie by były zgodne z obramowaniem
    def finish_edges(self, edges):
        resulting_edges = []
        for edge in edges:
            if edge.get_origin() is None or not self.inside(edge.get_origin()):
                self.finish_edge(edge)

            if edge.twin.get_origin() is None or not self.inside(edge.twin.get_origin()):
                self.finish_edge(edge.twin)
            if edge.get_origin() is not None and edge.twin.get_origin() is not None:
                resulting_edges.append(edge)
            else:
                self.delete_edge(edge)

        return resulting_edges

    # metoda usuwająca linię
    def delete_edge(self, edge):
        prev_edge = edge.prev
        next_edge = edge.next

        if prev_edge:
            prev_edge.set_next(next_edge)

        if next_edge:
            next_edge.twin.set_next(prev_edge)

        if edge.incident_point.first_edge == edge:
            if prev_edge:
                edge.incident_point.first_edge = prev_edge
            elif next_edge:
                edge.incident_point.first_edge = next_edge

        if edge.twin.incident_point.first_edge == edge.twin:
            if prev_edge:
                edge.twin.incident_point.first_edge = prev_edge.twin
            elif next_edge:
                edge.twin.incident_point.first_edge = next_edge.twin

    # metoda kończąca linię
    def finish_edge(self, edge):
        start = edge.get_origin(y=2 * (self.min_y - self.max_y), max_y=self.max_y)

        end = edge.twin.get_origin(y=self.min_y - self.max_y, max_y=self.max_y)

        point = self.get_intersection_point(end, start)

        v = Vertex(point=point)
        v.incident_edges.append(edge)
        edge.origin = v
        self.polygon_vertices.append(v)

        return edge

    # metoda sprawdzająca czy punkt leży wewnątrz obramowania
    def inside(self, point):
        vertices = self.points + self.points[0:1]
        x = point.x
        y = point.y
        inside = False

        for i in range(0, len(vertices) - 1):
            j = i + 1
            xi = vertices[i].x
            yi = vertices[i].y
            xj = vertices[j].x
            yj = vertices[j].y

            intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside

        return inside

    # metoda znajdująca punkt przecięcia z obramowaniem
    def get_intersection_point(self, orig, end):
        p = self.points + [self.points[0]]
        points = []

        point = None

        for i in range(0, len(p) - 1):
            intersection_point = math_helper.Math.get_intersection(orig, end, p[i], p[i + 1])
            if intersection_point:
                points.append(intersection_point)

        if not points:
            return None

        max_distance = math_helper.Math.distance(orig, end)

        if points:
            distances = [math_helper.Math.distance(orig, p) for p in points]
            distances = [i for i in distances if i <= max_distance]
            if distances:
                point = points[np.argmax(distances)]

        return point

# klasa symbolizująca wierzchołek
class Vertex:
    def __init__(self, incident_edges=[], point=None):
        self.incident_edges = incident_edges
        self.position = point

    def __str__(self):
        return "Vertex " +str(self.point)
