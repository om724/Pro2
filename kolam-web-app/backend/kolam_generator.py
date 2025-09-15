import svgwrite
import math
import random
import numpy as np
from typing import Dict, List, Tuple

class KolamGenerator:
    def __init__(self):
        # Basic L-System configurations
        self.default_axiom = "FBFBFBFB"  # Default initiator
        self.default_rules = {
            "A": "AFBFA",
            "B": "AFBFBFBFA"
        }
        self.angle = 45  # Angle in degrees
        
        # Store different Kolam rule systems
        self.kolam_systems = {
            "suzhi": {
                "axiom": "FBFBFBFB",
                "rules": {
                    "A": "AFBFA",
                    "B": "AFBFBFBFA"
                },
                "stroke": "black"
            },
            "kambi": {
                "axiom": "FBFBFBFB",
                "rules": {
                    "A": "AFBFA",
                    "B": "AFBFBFBFA"
                },
                "stroke": "blue"
            },
            "fourcolor": {
                "axiom": "FBFBFBFB",
                "rules": {
                    "A": "AFBFA",
                    "B": "AFBFBFBFA"
                },
                "multicolor": True
            },
            "island": {
                "axiom": "FBFBFBFB",
                "rules": {
                    "F": "AB",
                    "A": "AFBFA",
                    "B": "AFBFBFBFA"
                },
                "stroke": "green"
            },
            "sikku": {
                "axiom": "A",
                "rules": {
                    "A": "FBF", 
                    "B": "AFBFA", 
                    "F": "F"
                },
                "stroke": "purple"
            },
            "special": {
                "axiom": "A",
                "rules": {
                    "A": "B+FA-FB-FB-FB-FA+B",
                    "B": "BB"
                },
                "uses_angles": True,
                "stroke": "red"
            },
            "group": {
                "axiom": "FBFBFBFB",
                "rules": {
                    "A": "AFBFA",
                    "B": "AFBFBFBFA"
                },
                "polygon": True,
                "stroke": "navy"
            },
            "traditional": {
                "axiom": "FBFBFBFB",
                "rules": {
                    "A": "AFBFA",
                    "B": "AFBFBFBFA"
                },
                "traditional": True,
                "stroke": "black"
            }
        }
        
    def expand_lsystem_string(self, axiom: str, rules: Dict[str, str], iterations: int) -> str:
        """Expand the L-System string based on rules and iterations"""
        result = axiom
        for _ in range(iterations):
            result = "".join([rules.get(ch, ch) for ch in result])
        return result
    
    def generate_lsystem_svg(self, design_type: str, dot_size: int = 10, iterations: int = 6, 
                             width: int = 800, height: int = 600, **kwargs) -> str:
        """Generate L-system based Kolam pattern as SVG string"""
        # Get the kolam system configuration based on design type
        system = self.kolam_systems.get(design_type, self.kolam_systems["suzhi"])
        axiom = system["axiom"]
        rules = system["rules"]
        stroke_color = system.get("stroke", "black")
        multicolor = system.get("multicolor", False)
        uses_angles = system.get("uses_angles", False)
        is_polygon = system.get("polygon", False)
        
        # Additional parameters
        rhombus_size = kwargs.get("rhombus_size", 5)
        polygon_sides = kwargs.get("polygon_sides", 6)
        
        # Generate the L-system string
        lsystem_string = self.expand_lsystem_string(axiom, rules, iterations)
        
        # Create SVG drawing
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        # Special case for polygon-based designs
        if is_polygon:
            return self._generate_polygon_kolam_svg(width, height, polygon_sides, dot_size, iterations)
        
        # Special case for traditional Rangoli designs
        if system.get("traditional", False):
            return self._generate_traditional_rangoli_svg(width, height, dot_size, iterations, **kwargs)
        
        # Set up initial position and state based on design type
        if design_type == "kambi":
            # Calculate rhombus parameters
            rhombus_side = rhombus_size * dot_size
            x, y = width // 2 - rhombus_side // 2, height // 2 + rhombus_side // 2
        else:
            # Default centered position
            x, y = width // 2, height // 2
        
        direction = 0  # angle in degrees
        path_data = f"M {x} {y}"
        
        # Process L-system string to generate SVG path
        color_paths = {}
        current_color = stroke_color
        current_path = path_data
        
        for symbol in lsystem_string:
            # For multicolor designs, randomly change colors
            if multicolor and random.random() > 0.7:
                # Save the current path if it exists
                if current_path != path_data:
                    if current_color not in color_paths:
                        color_paths[current_color] = []
                    color_paths[current_color].append(current_path)
                
                # Generate a new random color
                r, g, b = random.random(), random.random(), random.random()
                current_color = f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"
                current_path = f"M {x} {y}"
            
            if symbol == "F":
                # Draw line forward
                new_x = x + dot_size * math.cos(math.radians(direction))
                new_y = y + dot_size * math.sin(math.radians(direction))
                current_path += f" L {new_x} {new_y}"
                x, y = new_x, new_y
                
            elif symbol == "+" and uses_angles:
                # Turn right by angle
                direction += self.angle
                direction %= 360
                
            elif symbol == "-" and uses_angles:
                # Turn left by angle
                direction -= self.angle
                direction %= 360
                
            elif symbol == "A":
                # Draw arc (90 degrees)
                radius = dot_size
                start_angle = math.radians(direction)
                end_angle = math.radians(direction + 90)
                
                # Calculate arc endpoint
                center_x = x - radius * math.sin(start_angle)
                center_y = y + radius * math.cos(start_angle)
                end_x = center_x + radius * math.cos(end_angle)
                end_y = center_y + radius * math.sin(end_angle)
                
                current_path += f" A {radius} {radius} 0 0 1 {end_x} {end_y}"
                x, y = end_x, end_y
                direction += 90
                direction %= 360
                
            elif symbol == "B":
                # Move forward and draw arc (270 degrees)
                forward_units = 5 / (2 ** 0.5)
                x += forward_units * math.cos(math.radians(direction))
                y += forward_units * math.sin(math.radians(direction))
                current_path += f" L {x} {y}"
                
                # Draw 270-degree arc
                radius = forward_units
                start_angle = math.radians(direction)
                end_angle = math.radians(direction + 270)
                
                center_x = x - radius * math.sin(start_angle)
                center_y = y + radius * math.cos(start_angle)
                end_x = center_x + radius * math.cos(end_angle)
                end_y = center_y + radius * math.sin(end_angle)
                
                current_path += f" A {radius} {radius} 0 1 1 {end_x} {end_y}"
                x, y = end_x, end_y
                direction += 270
                direction %= 360
        
        # Save the last path
        if current_path != path_data:
            if current_color not in color_paths:
                color_paths[current_color] = []
            color_paths[current_color].append(current_path)
        
        # Add paths to SVG
        if multicolor and color_paths:
            for color, paths in color_paths.items():
                for path_data in paths:
                    path = dwg.path(d=path_data, stroke=color, stroke_width='2', fill='none')
                    dwg.add(path)
        else:
            # Add a single path with the specified color
            path = dwg.path(d=current_path, stroke=stroke_color, stroke_width='2', fill='none')
            dwg.add(path)
        
        return dwg.tostring()
        
    def _generate_polygon_kolam_svg(self, width: int, height: int, sides: int, dot_size: int, iterations: int) -> str:
        """Generate a polygon-based Kolam design as SVG"""
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        # Center of the drawing
        center_x, center_y = width // 2, height // 2
        
        # Calculate radius based on dot size and iterations
        radius = dot_size * (iterations + 2) * 5
        
        # Generate polygon points
        points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
            
        # Draw the main polygon
        polygon_points = [(x, y) for x, y in points]
        dwg.add(dwg.polygon(points=polygon_points, fill='none', stroke='navy', stroke_width=2))
        
        # Draw internal patterns connecting points
        for i in range(sides):
            for j in range(i + 2, sides):
                if (i + j) % 2 == 0:  # Add some variation to connections
                    dwg.add(dwg.line(start=points[i], end=points[j], stroke='purple', stroke_width=1.5))
        
        # Add decorative circles at vertices
        for x, y in points:
            dwg.add(dwg.circle(center=(x, y), r=dot_size/2, fill='blue'))
        
        return dwg.tostring()
        
    def _generate_traditional_rangoli_svg(self, width: int, height: int, dot_size: int, iterations: int, **kwargs) -> str:
        """Generate a traditional Rangoli/Kolam design with intricate patterns"""
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        center_x, center_y = width // 2, height // 2
        
        # Parameters for the design
        grid_size = kwargs.get('grid_size', 7)  # Number of dots in grid
        pattern_type = kwargs.get('pattern_type', 'lotus')  # Pattern style
        
        # Create dot grid (traditional Kolam starts with dots)
        dots = []
        spacing = min(width, height) // (grid_size + 2)
        start_x = center_x - (grid_size - 1) * spacing // 2
        start_y = center_y - (grid_size - 1) * spacing // 2
        
        for i in range(grid_size):
            for j in range(grid_size):
                x = start_x + j * spacing
                y = start_y + i * spacing
                dots.append((x, y))
                # Draw dots
                dwg.add(dwg.circle(center=(x, y), r=2, fill='gray', opacity=0.3))
        
        # Generate traditional patterns based on type
        if pattern_type == 'lotus':
            self._draw_lotus_pattern(dwg, center_x, center_y, dot_size * 2, iterations)
        elif pattern_type == 'peacock':
            self._draw_peacock_pattern(dwg, center_x, center_y, dot_size * 2, iterations)
        elif pattern_type == 'flower':
            self._draw_flower_pattern(dwg, center_x, center_y, dot_size * 2, iterations)
        else:
            self._draw_geometric_pattern(dwg, dots, spacing, dot_size, iterations)
        
        return dwg.tostring()
    
    def _draw_lotus_pattern(self, dwg, center_x: int, center_y: int, radius: int, iterations: int):
        """Draw a lotus-like pattern"""
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        # Draw concentric circles with petals
        for i in range(iterations):
            current_radius = radius + i * 15
            petals = 6 + i * 2
            color = colors[i % len(colors)]
            
            # Draw petals
            for j in range(petals):
                angle = 2 * math.pi * j / petals
                
                # Petal coordinates
                x1 = center_x + current_radius * math.cos(angle)
                y1 = center_y + current_radius * math.sin(angle)
                
                # Control points for curves
                cx1 = center_x + (current_radius * 0.7) * math.cos(angle - 0.3)
                cy1 = center_y + (current_radius * 0.7) * math.sin(angle - 0.3)
                cx2 = center_x + (current_radius * 0.7) * math.cos(angle + 0.3)
                cy2 = center_y + (current_radius * 0.7) * math.sin(angle + 0.3)
                
                # Create petal shape
                path_data = f"M {center_x} {center_y} Q {cx1} {cy1} {x1} {y1} Q {cx2} {cy2} {center_x} {center_y}"
                dwg.add(dwg.path(d=path_data, fill=color, opacity=0.7, stroke='black', stroke_width=1))
    
    def _draw_peacock_pattern(self, dwg, center_x: int, center_y: int, radius: int, iterations: int):
        """Draw a peacock feather-like pattern"""
        colors = ['#8E44AD', '#3498DB', '#E74C3C', '#F39C12', '#27AE60']
        
        # Draw feather-like curves
        for i in range(8):  # 8 feathers around center
            angle = 2 * math.pi * i / 8
            color = colors[i % len(colors)]
            
            # Main feather stem
            stem_length = radius + 20
            end_x = center_x + stem_length * math.cos(angle)
            end_y = center_y + stem_length * math.sin(angle)
            
            # Draw stem
            dwg.add(dwg.line(start=(center_x, center_y), end=(end_x, end_y), 
                           stroke=color, stroke_width=3))
            
            # Draw feather details
            for j in range(iterations):
                detail_radius = 10 + j * 8
                detail_x = center_x + (stem_length * 0.8) * math.cos(angle)
                detail_y = center_y + (stem_length * 0.8) * math.sin(angle)
                
                # Left curve
                left_x = detail_x + detail_radius * math.cos(angle + math.pi/2)
                left_y = detail_y + detail_radius * math.sin(angle + math.pi/2)
                
                # Right curve  
                right_x = detail_x + detail_radius * math.cos(angle - math.pi/2)
                right_y = detail_y + detail_radius * math.sin(angle - math.pi/2)
                
                # Create feather detail curves
                path_data = f"M {detail_x} {detail_y} Q {left_x} {left_y} {end_x} {end_y} Q {right_x} {right_y} {detail_x} {detail_y}"
                dwg.add(dwg.path(d=path_data, fill='none', stroke=color, stroke_width=1.5, opacity=0.8))
    
    def _draw_flower_pattern(self, dwg, center_x: int, center_y: int, radius: int, iterations: int):
        """Draw a flower-like pattern"""
        colors = ['#FF1744', '#FF9800', '#FFEB3B', '#4CAF50', '#2196F3', '#9C27B0']
        
        # Draw flower layers
        for layer in range(iterations):
            current_radius = radius + layer * 25
            petals = 6
            color = colors[layer % len(colors)]
            
            # Draw petals as ellipses
            for i in range(petals):
                angle = 2 * math.pi * i / petals + (layer * 0.5)  # Rotate each layer
                
                petal_x = center_x + current_radius * math.cos(angle)
                petal_y = center_y + current_radius * math.sin(angle)
                
                # Create petal as rotated ellipse
                transform = f"rotate({math.degrees(angle)} {petal_x} {petal_y})"
                dwg.add(dwg.ellipse(center=(petal_x, petal_y), 
                                  r=(15 + layer * 5, 8 + layer * 2),
                                  fill=color, opacity=0.6, 
                                  stroke='black', stroke_width=1,
                                  transform=transform))
        
        # Center circle
        dwg.add(dwg.circle(center=(center_x, center_y), r=radius//3, 
                         fill='yellow', stroke='orange', stroke_width=2))
    
    def _draw_geometric_pattern(self, dwg, dots: list, spacing: int, dot_size: int, iterations: int):
        """Draw geometric connecting patterns between dots"""
        colors = ['black', '#E74C3C', '#3498DB', '#27AE60', '#F39C12']
        
        # Connect dots in various geometric patterns
        grid_size = int(math.sqrt(len(dots)))
        
        # Horizontal and vertical lines
        for i in range(grid_size):
            for j in range(grid_size - 1):
                idx1 = i * grid_size + j
                idx2 = i * grid_size + j + 1
                if idx1 < len(dots) and idx2 < len(dots):
                    dwg.add(dwg.line(start=dots[idx1], end=dots[idx2], 
                                   stroke=colors[0], stroke_width=2))
        
        # Vertical lines
        for i in range(grid_size - 1):
            for j in range(grid_size):
                idx1 = i * grid_size + j
                idx2 = (i + 1) * grid_size + j
                if idx1 < len(dots) and idx2 < len(dots):
                    dwg.add(dwg.line(start=dots[idx1], end=dots[idx2], 
                                   stroke=colors[0], stroke_width=2))
        
        # Diagonal patterns
        for i in range(grid_size - 1):
            for j in range(grid_size - 1):
                idx1 = i * grid_size + j
                idx2 = (i + 1) * grid_size + j + 1
                if idx1 < len(dots) and idx2 < len(dots) and iterations > 3:
                    dwg.add(dwg.line(start=dots[idx1], end=dots[idx2], 
                                   stroke=colors[1], stroke_width=1.5, opacity=0.7))
        
        # Add decorative curves around intersections
        for i, (x, y) in enumerate(dots):
            if i % 2 == 0 and iterations > 2:  # Add curves at alternate dots
                dwg.add(dwg.circle(center=(x, y), r=dot_size//2, 
                                 fill='none', stroke=colors[2], stroke_width=1.5))
        
    def generate_suzhi_kolam_svg(self, dot_size: int = 10, iterations: int = 6, 
                                width: int = 800, height: int = 600) -> str:
        """Generate Suzhi Kolam pattern as SVG string (legacy support)"""
        return self.generate_lsystem_svg("suzhi", dot_size, iterations, width, height)
    
    def generate_kambi_kolam_svg(self, dot_size: int = 10, rhombus_size: int = 5,
                                width: int = 800, height: int = 600) -> str:
        """Generate Kambi Kolam pattern as SVG string (legacy support)"""
        return self.generate_lsystem_svg("kambi", dot_size, iterations=rhombus_size, 
                                       width=width, height=height, rhombus_size=rhombus_size)
    
    def generate_custom_kolam_svg(self, coordinates: List[Tuple[int, int]], 
                                 width: int = 800, height: int = 600) -> str:
        """Generate custom Kolam from coordinate points"""
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
        
        if not coordinates:
            return dwg.tostring()
        
        # Create path from coordinates
        path_data = f"M {coordinates[0][0]} {coordinates[0][1]}"
        for x, y in coordinates[1:]:
            path_data += f" L {x} {y}"
        
        # Close the path if needed
        if len(coordinates) > 2:
            path_data += " Z"
        
        path = dwg.path(d=path_data, stroke='red', stroke_width='2', fill='none')
        dwg.add(path)
        
        return dwg.tostring()
        
    def generate_fourcolor_kolam_svg(self, dot_size: int = 10, iterations: int = 6,
                                    width: int = 800, height: int = 600) -> str:
        """Generate a Four-Color Kolam pattern as SVG string"""
        return self.generate_lsystem_svg("fourcolor", dot_size, iterations, width, height)
    
    def generate_island_kolam_svg(self, dot_size: int = 10, iterations: int = 6,
                                 width: int = 800, height: int = 600) -> str:
        """Generate an Island Kolam pattern as SVG string"""
        return self.generate_lsystem_svg("island", dot_size, iterations, width, height)
    
    def generate_sikku_kolam_svg(self, dot_size: int = 10, iterations: int = 6,
                               width: int = 800, height: int = 600) -> str:
        """Generate a Sikku Kolam pattern as SVG string"""
        return self.generate_lsystem_svg("sikku", dot_size, iterations, width, height)
    
    def generate_special_kolam_svg(self, dot_size: int = 10, iterations: int = 6,
                                  width: int = 800, height: int = 600) -> str:
        """Generate a Special Variety Kolam pattern as SVG string"""
        return self.generate_lsystem_svg("special", dot_size, iterations, width, height)
    
    def generate_group_kolam_svg(self, dot_size: int = 10, iterations: int = 4,
                                polygon_sides: int = 6, width: int = 800, height: int = 600) -> str:
        """Generate a Group Theory based Kolam pattern as SVG string"""
        return self.generate_lsystem_svg("group", dot_size, iterations, width, height, 
                                       polygon_sides=polygon_sides)
                                       
    def generate_traditional_rangoli_svg(self, dot_size: int = 10, iterations: int = 4,
                                        grid_size: int = 7, pattern_type: str = 'lotus',
                                        width: int = 800, height: int = 600) -> str:
        """Generate a Traditional Rangoli pattern as SVG string"""
        return self.generate_lsystem_svg("traditional", dot_size, iterations, width, height,
                                       grid_size=grid_size, pattern_type=pattern_type)
