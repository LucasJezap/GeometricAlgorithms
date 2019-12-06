import numpy as np
import data_structures


# klasa Math zawierająca pomocne metody do obliczeń
class Math:
    # metoda obliczająca odległość
    @staticmethod
    def distance(point_a, point_b):
        x1 = point_a.x
        x2 = point_b.x
        y1 = point_a.y
        y2 = point_b.y

        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # metoda obliczająca długość wektora
    @staticmethod
    def magnitude(vector):
        return np.sqrt(np.dot(np.array(vector), np.array(vector)))

    # metoda zwracająca normę wektora
    @staticmethod
    def norm(vector):
        if Math.magnitude(np.array(vector)) == 0:
            return np.array(vector)
        return np.array(vector) / Math.magnitude(np.array(vector))

    # metoda zwracająca punkt przecięcia odcinkow jeśli istnieje
    @staticmethod
    def line_ray_intersection_point(ray_orig, ray_end, point_1, point_2):
        orig = np.array(ray_orig, dtype=np.float)
        end = np.array(ray_end)
        direction = np.array(Math.norm(end - orig), dtype=np.float)
        point_1 = np.array(point_1, dtype=np.float)
        point_2 = np.array(point_2, dtype=np.float)

        v1 = orig - point_1
        v2 = point_2 - point_1
        v3 = np.array([-direction[1], direction[0]])

        if np.dot(v2, v3) == 0:
            return []

        t1 = np.cross(v2, v1) / np.dot(v2, v3)
        t2 = np.dot(v1, v3) / np.dot(v2, v3)

        if t1 > 0.0 and 0.0 <= t2 <= 1.0:
            return [orig + t1 * direction]
        return []

    # metoda zwracajaca punkt przeciecia odcinkow jesli istnieje
    @staticmethod
    def get_intersection(orig, end, p1, p2):
        if not orig or not end:
            return None

        point = Math.line_ray_intersection_point([orig.x, orig.y], [end.x, end.y], [p1.x, p1.y], [p2.x, p2.y])

        if len(point) == 0:
            return None

        return data_structures.Coordinate(point[0][0], point[0][1])

    # metoda obliczająca kąt
    @staticmethod
    def calculate_angle(point, center):
        dx = point.x - center.x
        dy = point.y - center.y
        return np.math.degrees(np.math.atan2(dy, dx)) % 360

    # metoda sprawdzająca czy punkty są ułożone zgodnie z kierunkiem ruchu wskazówek zegara
    @staticmethod
    def check_clockwise(a, b, c, center):
        angle_1 = Math.calculate_angle(a, center)
        angle_2 = Math.calculate_angle(b, center)
        angle_3 = Math.calculate_angle(c, center)

        counter_clockwise = (angle_3 - angle_1) % 360 > (angle_3 - angle_2) % 360

        if counter_clockwise:
            return False

        return True