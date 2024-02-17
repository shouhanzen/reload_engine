from pydantic import BaseModel
from typing import Optional, Tuple
from reload_core.types import Vector2

class Circle2D(BaseModel):
    p: Vector2
    r: float

class Edge2D(BaseModel):
    a: Vector2
    b: Vector2
    
    def orientation(self, p: Vector2, q: Vector2, r: Vector2) -> int:
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0: return 0  # Collinear
        return 1 if val > 0 else 2  # Clock or counterclock wise

    def on_segment(self, p: Vector2, q: Vector2, r: Vector2) -> bool:
        return min(p.x, r.x) <= q.x <= max(p.x, r.x) and min(p.y, r.y) <= q.y <= max(p.y, r.y)


    def intersects(self, other: 'Edge2D') -> Tuple[bool, Optional[Vector2]]:
        """Check if the edge intersects with another edge 'other' and return the intersection point if they do."""
        # The four orientations needed for general and special cases
        o1 = self.orientation(self.a, self.b, other.a)
        o2 = self.orientation(self.a, self.b, other.b)
        o3 = self.orientation(other.a, other.b, self.a)
        o4 = self.orientation(other.a, other.b, self.b)

        # General case
        if o1 != o2 and o3 != o4:
            # Calculate the intersection point
            denominator = (self.a.x - self.b.x) * (other.a.y - other.b.y) - (self.a.y - self.b.y) * (other.a.x - other.b.x)
            if denominator == 0:
                return False, None  # Lines are parallel or collinear

            x_numerator = (self.a.x*self.b.y - self.a.y*self.b.x)*(other.a.x - other.b.x) - (self.a.x - self.b.x)*(other.a.x*other.b.y - other.a.y*other.b.x)
            y_numerator = (self.a.x*self.b.y - self.a.y*self.b.x)*(other.a.y - other.b.y) - (self.a.y - self.b.y)*(other.a.x*other.b.y - other.a.y*other.b.x)
            X = x_numerator / denominator
            Y = y_numerator / denominator

            return True, Vector2(x=X, y=Y)

        # Handle special cases of collinearity.
        if o1 == 0 and self.on_segment(self.a, other.a, self.b): return True, None
        if o2 == 0 and self.on_segment(self.a, other.b, self.b): return True, None
        if o3 == 0 and self.on_segment(other.a, self.a, other.b): return True, None
        if o4 == 0 and self.on_segment(other.a, self.b, other.b): return True, None

        return False, None  # No intersection

    def get_parallel_component(self, other: 'Edge2D') -> Vector2:
        # Get the projection of self onto other
        l = (self.b - self.a).normalize()
        return l * (l.dot(other.b - other.a))
        
class Box2D(BaseModel):
    pos: Vector2
    dims: Vector2
    
    def collides_with(self, other: 'Box2D') -> bool:
        if self.pos.x < other.pos.x + other.dims.x and self.pos.x + self.dims.x > other.pos.x and self.pos.y < other.pos.y + other.dims.y and self.pos.y + self.dims.y > other.pos.y:
            return True
        return False
    
    def collides_with_circle(self, other: Circle2D) -> bool:
        # Find the closest point to the circle within the rectangle
        closest_x = max(self.pos.x, min(other.p.x, self.pos.x + self.dims.x))
        closest_y = max(self.pos.y, min(other.p.y, self.pos.y + self.dims.y))
        # Calculate the distance between the circle's center and this closest point
        distance_x = other.p.x - closest_x
        distance_y = other.p.y - closest_y
        # If the distance is less than the circle's radius, an intersection occurs
        distance_squared = (distance_x * distance_x) + (distance_y * distance_y)
        return distance_squared < (other.r * other.r)