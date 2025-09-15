import svgwrite
import math
import random
import numpy as np
from typing import Dict, List, Tuple

class AuthenticKolamGenerator:
    """
    Authentic Kolam generator based on the exact patterns from SIH folder
    """
    
    def __init__(self):
        # Standard L-System from SIH files
        self.default_axiom = "FBFBFBFB"
        self.default_rules = {
            "A": "AFBFA",
            "B": "AFBFBFBFA"
        }
        self.angle = 45
        
        # Color schemes from the original files
        self.color_schemes = {
            "traditional": ["black"],
            "three_color": ["red", "green", "blue"],
            "multicolor": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98FB98"]
        }
    
    def expand_lsystem_string(self, axiom: str, rules: Dict[str, str], iterations: int) -> str:
        """Expand L-System string exactly as in original SIH code"""
        result = axiom
        for _ in range(iterations):
            result = "".join([rules.get(ch, ch) for ch in result])
        return result
    
    def generate_single_knot_kolam_svg(self, dot_size: int = 20, iterations: int = 4,
                                     width: int = 800, height: int = 600) -> str:
        """
        Generate Single Knot Kolam exactly like kollamsingleknot.py from SIH folder
        """
        # Use exact L-System from original code
        axiom = "FBFBFBFB"
        rules = {"A": "AFBFA", "B": "AFBFBFBFA"}
        
        # Expand the L-System
        lsystem_string = self.expand_lsystem_string(axiom, rules, iterations)
        
        # Create SVG
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        # Starting position (center, rotated 45 degrees like original)
        x, y = width // 2, height // 2
        direction = 45  # Start at 45 degrees like original
        
        # Colors from original code
        colors = {"F": "green", "A": "blue", "B": "red"}
        
        # Process each symbol in the L-System string
        for symbol in lsystem_string:
            color = colors.get(symbol, "black")
            
            if symbol == "F":
                # Forward movement (from original: fd(20))
                new_x = x + dot_size * math.cos(math.radians(direction))
                new_y = y + dot_size * math.sin(math.radians(direction))
                
                # Draw line
                dwg.add(dwg.line(start=(x, y), end=(new_x, new_y), 
                               stroke=color, stroke_width=4))
                x, y = new_x, new_y
                
            elif symbol == "A":
                # Arc 90 degrees (from original: circle(20, 90))
                radius = dot_size
                start_angle = math.radians(direction)
                end_angle = math.radians(direction + 90)
                
                # Calculate arc path
                sweep_flag = 1 if 90 > 0 else 0
                large_arc_flag = 1 if abs(90) > 180 else 0
                
                end_x = x + radius * math.cos(end_angle)
                end_y = y + radius * math.sin(end_angle)
                
                path_data = f"M {x} {y} A {radius} {radius} 0 {large_arc_flag} {sweep_flag} {end_x} {end_y}"
                dwg.add(dwg.path(d=path_data, stroke=color, stroke_width=4, fill='none'))
                
                x, y = end_x, end_y
                direction += 90
                direction %= 360
                
            elif symbol == "B":
                # Complex B movement (from original code)
                I = 10 / math.sqrt(2)  # Forward units calculation from original
                
                # First forward movement
                new_x = x + I * math.cos(math.radians(direction))
                new_y = y + I * math.sin(math.radians(direction))
                dwg.add(dwg.line(start=(x, y), end=(new_x, new_y), 
                               stroke=color, stroke_width=4))
                x, y = new_x, new_y
                
                # Arc 270 degrees
                radius = I
                start_angle = math.radians(direction)
                end_angle = math.radians(direction + 270)
                
                sweep_flag = 1 if 270 > 0 else 0
                large_arc_flag = 1 if abs(270) > 180 else 0
                
                end_x = x + radius * math.cos(end_angle)
                end_y = y + radius * math.sin(end_angle)
                
                path_data = f"M {x} {y} A {radius} {radius} 0 {large_arc_flag} {sweep_flag} {end_x} {end_y}"
                dwg.add(dwg.path(d=path_data, stroke=color, stroke_width=4, fill='none'))
                
                x, y = end_x, end_y
                direction += 270
                direction %= 360
                
                # Second forward movement (fd(I) from original)
                new_x = x + I * math.cos(math.radians(direction))
                new_y = y + I * math.sin(math.radians(direction))
                dwg.add(dwg.line(start=(x, y), end=(new_x, new_y), 
                               stroke=color, stroke_width=4))
                x, y = new_x, new_y
        
        return dwg.tostring()
    
    def generate_rhombus_kolam_svg(self, dot_size: int = 20, rhombus_size: int = 5,
                                 width: int = 800, height: int = 600) -> str:
        """
        Generate Rhombus Kolam exactly like rombaturtlekolam.py from SIH folder
        """
        axiom = "FBFBFBFB"
        rules = {"A": "AFBFA", "B": "AFBFBFBFA"}
        iterations = rhombus_size  # Use rhombus_size as iterations like original
        
        lsystem_string = self.expand_lsystem_string(axiom, rules, iterations)
        
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        # Calculate rhombus parameters (from original code)
        rhombus_side = rhombus_size * dot_size
        
        # Starting position (from original: -rhombus_side / 2, rhombus_side / 2)
        x = width // 2 - rhombus_side // 2
        y = height // 2 + rhombus_side // 2
        direction = 0
        
        # Draw the rhombus outline first
        rhombus_points = [
            (width // 2, height // 2 - rhombus_side // 2),  # Top
            (width // 2 + rhombus_side // 2, height // 2),   # Right
            (width // 2, height // 2 + rhombus_side // 2),   # Bottom
            (width // 2 - rhombus_side // 2, height // 2)    # Left
        ]
        dwg.add(dwg.polygon(points=rhombus_points, fill='none', stroke='gray', 
                          stroke_width=2, opacity=0.5))
        
        # Process L-System within rhombus
        for symbol in lsystem_string:
            if symbol == "F":
                new_x = x + dot_size * math.cos(math.radians(direction))
                new_y = y + dot_size * math.sin(math.radians(direction))
                dwg.add(dwg.line(start=(x, y), end=(new_x, new_y), 
                               stroke='black', stroke_width=3))
                x, y = new_x, new_y
                
            elif symbol == "A":
                radius = dot_size
                end_x = x + radius * math.cos(math.radians(direction + 90))
                end_y = y + radius * math.sin(math.radians(direction + 90))
                
                path_data = f"M {x} {y} A {radius} {radius} 0 0 1 {end_x} {end_y}"
                dwg.add(dwg.path(d=path_data, stroke='blue', stroke_width=3, fill='none'))
                
                x, y = end_x, end_y
                direction += 90
                direction %= 360
                
            elif symbol == "B":
                I = 5 / math.sqrt(2)
                # Forward
                new_x = x + I * math.cos(math.radians(direction))
                new_y = y + I * math.sin(math.radians(direction))
                dwg.add(dwg.line(start=(x, y), end=(new_x, new_y), 
                               stroke='red', stroke_width=3))
                x, y = new_x, new_y
                
                # Arc 270
                end_x = x + I * math.cos(math.radians(direction + 270))
                end_y = y + I * math.sin(math.radians(direction + 270))
                path_data = f"M {x} {y} A {I} {I} 0 1 1 {end_x} {end_y}"
                dwg.add(dwg.path(d=path_data, stroke='red', stroke_width=3, fill='none'))
                
                x, y = end_x, end_y
                direction += 270
                direction %= 360
        
        return dwg.tostring()
    
    def generate_polygon_inscribed_kolam_svg(self, dot_size: int = 20, polygon_vertices: int = 6,
                                           polygon_size: int = 100, iterations: int = 4,
                                           width: int = 800, height: int = 600) -> str:
        """
        Generate Polygon Inscribed Kolam like rombaturtlekolamgghpoly.py from SIH folder
        """
        axiom = "FBFBFBFB"
        rules = {"A": "AFBFA", "B": "AFBFBFBFA"}
        
        lsystem_string = self.expand_lsystem_string(axiom, rules, iterations)
        
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        center_x, center_y = width // 2, height // 2
        
        # Generate polygon points
        polygon_points = []
        for i in range(polygon_vertices):
            angle = 2 * math.pi * i / polygon_vertices
            px = center_x + polygon_size * math.cos(angle)
            py = center_y + polygon_size * math.sin(angle)
            polygon_points.append((px, py))
        
        # Draw the polygon outline
        dwg.add(dwg.polygon(points=polygon_points, fill='none', stroke='purple', 
                          stroke_width=3))
        
        # Calculate inscribed kolam size (from original: polygon_side_length / (polygon_vertices + 1))
        kolam_side_length = polygon_size / (polygon_vertices + 1)
        
        # Draw multiple inscribed kolams (from original logic)
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        for i in range(min(polygon_vertices, 5)):  # Limit to avoid overcrowding
            # Position each kolam
            angle = 2 * math.pi * i / polygon_vertices
            kolam_x = center_x + (polygon_size * 0.6) * math.cos(angle)
            kolam_y = center_y + (polygon_size * 0.6) * math.sin(angle)
            
            # Draw small kolam at this position
            self._draw_mini_kolam(dwg, lsystem_string, kolam_x, kolam_y, 
                                dot_size // 2, colors[i % len(colors)])
        
        return dwg.tostring()
    
    def _draw_mini_kolam(self, dwg, lsystem_string: str, start_x: float, start_y: float, 
                        size: int, color: str):
        """Helper method to draw a small kolam at specified position"""
        x, y = start_x, start_y
        direction = 45
        
        for symbol in lsystem_string[:min(len(lsystem_string), 50)]:  # Limit complexity
            if symbol == "F":
                new_x = x + size * math.cos(math.radians(direction))
                new_y = y + size * math.sin(math.radians(direction))
                dwg.add(dwg.line(start=(x, y), end=(new_x, new_y), 
                               stroke=color, stroke_width=2))
                x, y = new_x, new_y
            elif symbol == "A":
                radius = size
                end_x = x + radius * math.cos(math.radians(direction + 90))
                end_y = y + radius * math.sin(math.radians(direction + 90))
                path_data = f"M {x} {y} A {radius} {radius} 0 0 1 {end_x} {end_y}"
                dwg.add(dwg.path(d=path_data, stroke=color, stroke_width=2, fill='none'))
                x, y = end_x, end_y
                direction += 90
                direction %= 360
    
    def generate_circle_inscribed_kolam_svg(self, dot_size: int = 20, circle_radius: int = 100,
                                          iterations: int = 4, width: int = 800, height: int = 600) -> str:
        """
        Generate Circle Inscribed Kolam like rombaturtlekolamgghpolycircle.py from SIH folder
        """
        axiom = "FBFBFBFB"
        rules = {"A": "AFBFA", "B": "AFBFBFBFA"}
        
        lsystem_string = self.expand_lsystem_string(axiom, rules, iterations)
        
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        center_x, center_y = width // 2, height // 2
        
        # Draw the outer circle
        dwg.add(dwg.circle(center=(center_x, center_y), r=circle_radius, 
                         fill='none', stroke='blue', stroke_width=3))
        
        # Draw multiple concentric circles with kolams
        num_circles = 3
        for i in range(num_circles):
            current_radius = circle_radius - (i + 1) * (circle_radius // (num_circles + 1))
            if current_radius > 20:
                # Draw circle
                dwg.add(dwg.circle(center=(center_x, center_y), r=current_radius, 
                                 fill='none', stroke='lightblue', stroke_width=1, opacity=0.7))
                
                # Draw kolam around circle
                num_points = 8
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points
                    kolam_x = center_x + current_radius * math.cos(angle)
                    kolam_y = center_y + current_radius * math.sin(angle)
                    
                    # Draw mini kolam
                    self._draw_mini_kolam(dwg, lsystem_string, kolam_x, kolam_y, 
                                        max(5, dot_size // (i + 2)), f'hsl({j * 45}, 70%, 50%)')
        
        return dwg.tostring()
    
    def generate_suzhi_sikku_kambi_combined_svg(self, dot_size: int = 20, iterations: int = 4,
                                              width: int = 800, height: int = 600) -> str:
        """
        Generate combined Suzhi, Sikku, and Kambi Kolam like suzhisikkukambikolam.py
        """
        axiom = "FBFBFBFB"
        rules = {"A": "AFBFA", "B": "AFBFBFBFA"}
        
        lsystem_string = self.expand_lsystem_string(axiom, rules, iterations)
        
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        # Draw three different sections
        sections = [
            {"center": (width // 4, height // 2), "name": "Suzhi", "color": "red"},
            {"center": (width // 2, height // 2), "name": "Sikku", "color": "green"},
            {"center": (3 * width // 4, height // 2), "name": "Kambi", "color": "blue"}
        ]
        
        for section in sections:
            center_x, center_y = section["center"]
            color = section["color"]
            
            # Add section label
            dwg.add(dwg.text(section["name"], insert=(center_x - 30, center_y - 100), 
                           font_size=16, font_family="Arial", fill=color))
            
            x, y = center_x, center_y
            direction = 45
            
            # Draw the kolam for this section
            for i, symbol in enumerate(lsystem_string):
                if i > 100:  # Limit complexity for combined view
                    break
                    
                if symbol == "F":
                    new_x = x + dot_size * math.cos(math.radians(direction))
                    new_y = y + dot_size * math.sin(math.radians(direction))
                    dwg.add(dwg.line(start=(x, y), end=(new_x, new_y), 
                                   stroke=color, stroke_width=3))
                    x, y = new_x, new_y
                    
                elif symbol == "A":
                    radius = dot_size
                    end_x = x + radius * math.cos(math.radians(direction + 90))
                    end_y = y + radius * math.sin(math.radians(direction + 90))
                    path_data = f"M {x} {y} A {radius} {radius} 0 0 1 {end_x} {end_y}"
                    dwg.add(dwg.path(d=path_data, stroke=color, stroke_width=3, fill='none'))
                    x, y = end_x, end_y
                    direction += 90
                    direction %= 360
                    
                elif symbol == "B":
                    I = 5 / math.sqrt(2)
                    new_x = x + I * math.cos(math.radians(direction))
                    new_y = y + I * math.sin(math.radians(direction))
                    dwg.add(dwg.line(start=(x, y), end=(new_x, new_y), 
                                   stroke=color, stroke_width=3))
                    x, y = new_x, new_y
                    
                    end_x = x + I * math.cos(math.radians(direction + 270))
                    end_y = y + I * math.sin(math.radians(direction + 270))
                    path_data = f"M {x} {y} A {I} {I} 0 1 1 {end_x} {end_y}"
                    dwg.add(dwg.path(d=path_data, stroke=color, stroke_width=3, fill='none'))
                    x, y = end_x, end_y
                    direction += 270
                    direction %= 360
        
        return dwg.tostring()
    
    def generate_coordinate_based_kolam_svg(self, coordinates: List[Tuple[int, int]], 
                                          width: int = 800, height: int = 600,
                                          connect_type: str = "sequential") -> str:
        """
        Generate Kolam from coordinates (like the CSV extraction scripts in SIH folder)
        """
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        if not coordinates:
            return dwg.tostring()
        
        if connect_type == "sequential":
            # Connect points in sequence
            for i in range(len(coordinates) - 1):
                dwg.add(dwg.line(start=coordinates[i], end=coordinates[i + 1], 
                               stroke='black', stroke_width=2))
        elif connect_type == "dots":
            # Just show as dots
            for x, y in coordinates:
                dwg.add(dwg.circle(center=(x, y), r=1, fill='black'))
        elif connect_type == "curves":
            # Connect with smooth curves
            if len(coordinates) > 2:
                path_data = f"M {coordinates[0][0]} {coordinates[0][1]}"
                for i in range(1, len(coordinates) - 1):
                    x1, y1 = coordinates[i]
                    x2, y2 = coordinates[i + 1]
                    # Use quadratic curve
                    path_data += f" Q {x1} {y1} {x2} {y2}"
                
                dwg.add(dwg.path(d=path_data, stroke='black', stroke_width=2, fill='none'))
        
        return dwg.tostring()
