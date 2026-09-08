import math

class Hands():
    
    def __init__(self,s,e,w):
        self.s = s
        self.e = e
        self.w = w
        

    @staticmethod
    def calc_angle(shoulder, elbow, wrist):
        """
        Calculates the relative angle at the elbow joint using the forearm as the baseline.
        Input parameters are tuples or lists of coordinates: [x, y]
        """
        # 1. Unpack coordinates
        sx, sy = shoulder[0], shoulder[1]
        ex, ey = elbow[0], elbow[1]
        wx, wy = wrist[0], wrist[1]
        
        # 2. Create vectors relative to the elbow as the origin (0,0)
        # Forearm Vector (Elbow -> Wrist)
        fx, fy = wx - ex, wy - ey
        # Upper Arm Vector (Elbow -> Shoulder)
        ux, uy = sx - ex, sy - ey
        
        # 3. Calculate dot product and 2D cross product manually
        dot_product = (fx * ux) + (fy * uy)
        cross_product = (fx * uy) - (fy * ux)
        
        # 4. Use math.atan2 to safely get the angle between them
        angle_radians = math.atan2(cross_product, dot_product)
        angle_degrees = abs(math.degrees(angle_radians))
        
        # 5. Enforce interior angle constraint
        if angle_degrees > 180:
            angle_degrees = 360 - angle_degrees
            
        return int(angle_degrees)

    def calc(self,person):
        shoulder = person[self.s]
        elbow = person[self.e]
        wrist = person[self.w]

        elbow_angle = self.calc_angle(shoulder, elbow, wrist)

        return elbow_angle