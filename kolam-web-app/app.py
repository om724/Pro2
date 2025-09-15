from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from backend.kolam_generator import KolamGenerator
from backend.authentic_kolam_generator import AuthenticKolamGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the Kolam generators
kolam_gen = KolamGenerator()
auth_kolam_gen = AuthenticKolamGenerator()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/generate-kolam', methods=['POST'])
def generate_kolam():
    """Generate Kolam design based on user inputs"""
    try:
        data = request.get_json()
        
        # Extract parameters
        design_type = data.get('design_type', 'suzhi')
        dot_size = int(data.get('dot_size', 10))
        iterations = int(data.get('iterations', 6))
        width = int(data.get('width', 800))
        height = int(data.get('height', 600))
        
        # Generate SVG based on design type
        if design_type == 'suzhi':
            svg_content = kolam_gen.generate_suzhi_kolam_svg(
                dot_size=dot_size, 
                iterations=iterations, 
                width=width, 
                height=height
            )
        elif design_type == 'kambi':
            rhombus_size = int(data.get('rhombus_size', 5))
            svg_content = kolam_gen.generate_kambi_kolam_svg(
                dot_size=dot_size, 
                rhombus_size=rhombus_size, 
                width=width, 
                height=height
            )
        elif design_type == 'fourcolor':
            svg_content = kolam_gen.generate_fourcolor_kolam_svg(
                dot_size=dot_size, 
                iterations=iterations, 
                width=width, 
                height=height
            )
        elif design_type == 'island':
            svg_content = kolam_gen.generate_island_kolam_svg(
                dot_size=dot_size, 
                iterations=iterations, 
                width=width, 
                height=height
            )
        elif design_type == 'sikku':
            svg_content = kolam_gen.generate_sikku_kolam_svg(
                dot_size=dot_size, 
                iterations=iterations, 
                width=width, 
                height=height
            )
        elif design_type == 'special':
            svg_content = kolam_gen.generate_special_kolam_svg(
                dot_size=dot_size, 
                iterations=iterations, 
                width=width, 
                height=height
            )
        elif design_type == 'group':
            polygon_sides = int(data.get('polygon_sides', 6))
            svg_content = kolam_gen.generate_group_kolam_svg(
                dot_size=dot_size, 
                iterations=iterations, 
                polygon_sides=polygon_sides,
                width=width, 
                height=height
            )
        elif design_type == 'traditional':
            grid_size = int(data.get('grid_size', 7))
            pattern_type = data.get('pattern_type', 'lotus')
            svg_content = kolam_gen.generate_traditional_rangoli_svg(
                dot_size=dot_size, 
                iterations=iterations, 
                grid_size=grid_size,
                pattern_type=pattern_type,
                width=width, 
                height=height
            )
        elif design_type == 'single_knot':
            svg_content = auth_kolam_gen.generate_single_knot_kolam_svg(
                dot_size=dot_size,
                iterations=iterations,
                width=width,
                height=height
            )
        elif design_type == 'rhombus':
            rhombus_size = int(data.get('rhombus_size', 5))
            svg_content = auth_kolam_gen.generate_rhombus_kolam_svg(
                dot_size=dot_size,
                rhombus_size=rhombus_size,
                width=width,
                height=height
            )
        elif design_type == 'polygon_inscribed':
            polygon_vertices = int(data.get('polygon_vertices', 6))
            polygon_size = int(data.get('polygon_size', 100))
            svg_content = auth_kolam_gen.generate_polygon_inscribed_kolam_svg(
                dot_size=dot_size,
                polygon_vertices=polygon_vertices,
                polygon_size=polygon_size,
                iterations=iterations,
                width=width,
                height=height
            )
        elif design_type == 'circle_inscribed':
            circle_radius = int(data.get('circle_radius', 100))
            svg_content = auth_kolam_gen.generate_circle_inscribed_kolam_svg(
                dot_size=dot_size,
                circle_radius=circle_radius,
                iterations=iterations,
                width=width,
                height=height
            )
        elif design_type == 'combined':
            svg_content = auth_kolam_gen.generate_suzhi_sikku_kambi_combined_svg(
                dot_size=dot_size,
                iterations=iterations,
                width=width,
                height=height
            )
        elif design_type == 'custom':
            coordinates = data.get('coordinates', [])
            # Convert coordinates to list of tuples
            coord_list = [(coord['x'], coord['y']) for coord in coordinates]
            svg_content = kolam_gen.generate_custom_kolam_svg(
                coordinates=coord_list, 
                width=width, 
                height=height
            )
        else:
            return jsonify({'error': 'Invalid design type'}), 400
        
        return jsonify({
            'success': True,
            'svg': svg_content,
            'parameters': {
                'design_type': design_type,
                'dot_size': dot_size,
                'iterations': iterations,
                'width': width,
                'height': height
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/design-types', methods=['GET'])
def get_design_types():
    """Get available design types"""
    return jsonify({
        'design_types': [
            {
                'id': 'suzhi',
                'name': 'Suzhi Kolam',
                'description': 'Traditional Suzhi Kolam pattern using L-Systems',
                'parameters': ['dot_size', 'iterations']
            },
            {
                'id': 'kambi',
                'name': 'Kambi Kolam',
                'description': 'Kambi Kolam pattern within a rhombus shape',
                'parameters': ['dot_size', 'rhombus_size']
            },
            {
                'id': 'fourcolor',
                'name': 'Four-Color Kolam',
                'description': 'Colorful Kolam with randomly changing colors',
                'parameters': ['dot_size', 'iterations']
            },
            {
                'id': 'island',
                'name': 'Island Kolam',
                'description': 'Island-style Kolam with modified L-system rules',
                'parameters': ['dot_size', 'iterations']
            },
            {
                'id': 'sikku',
                'name': 'Sikku Kolam',
                'description': 'Step-style Kolam with interlaced patterns',
                'parameters': ['dot_size', 'iterations']
            },
            {
                'id': 'special',
                'name': 'Special Variety Kolam',
                'description': 'Advanced L-system with angle-based transformations',
                'parameters': ['dot_size', 'iterations']
            },
            {
                'id': 'group',
                'name': 'Group Theory Kolam',
                'description': 'Polygon-based Kolam using group theory principles',
                'parameters': ['dot_size', 'iterations', 'polygon_sides']
            },
            {
                'id': 'traditional',
                'name': 'Traditional Rangoli',
                'description': 'Authentic Indian Rangoli designs with intricate patterns',
                'parameters': ['dot_size', 'iterations', 'grid_size', 'pattern_type']
            },
            {
                'id': 'single_knot',
                'name': 'Single Knot Kolam (SIH)',
                'description': 'Exact implementation from kollamsingleknot.py - authentic colored L-System',
                'parameters': ['dot_size', 'iterations']
            },
            {
                'id': 'rhombus',
                'name': 'Rhombus Kolam (SIH)',
                'description': 'From rombaturtlekolam.py - L-System within rhombus boundary',
                'parameters': ['dot_size', 'rhombus_size']
            },
            {
                'id': 'polygon_inscribed',
                'name': 'Polygon Inscribed Kolam (SIH)',
                'description': 'From rombaturtlekolamgghpoly.py - multiple kolams inscribed in polygons',
                'parameters': ['dot_size', 'iterations', 'polygon_vertices', 'polygon_size']
            },
            {
                'id': 'circle_inscribed',
                'name': 'Circle Inscribed Kolam (SIH)',
                'description': 'From rombaturtlekolamgghpolycircle.py - concentric circular patterns',
                'parameters': ['dot_size', 'iterations', 'circle_radius']
            },
            {
                'id': 'combined',
                'name': 'Suzhi-Sikku-Kambi Combined (SIH)',
                'description': 'From suzhisikkukambikolam.py - three traditional patterns combined',
                'parameters': ['dot_size', 'iterations']
            },
            {
                'id': 'custom',
                'name': 'Custom Kolam',
                'description': 'Custom Kolam from coordinate points',
                'parameters': ['coordinates']
            }
        ]
    })

@app.route('/api/validate-parameters', methods=['POST'])
def validate_parameters():
    """Validate input parameters"""
    try:
        data = request.get_json()
        design_type = data.get('design_type')
        
        errors = []
        
        # Common validations
        dot_size = data.get('dot_size', 10)
        if not isinstance(dot_size, int) or dot_size < 1 or dot_size > 50:
            errors.append('Dot size must be between 1 and 50')
        
        width = data.get('width', 800)
        height = data.get('height', 600)
        if not isinstance(width, int) or width < 100 or width > 2000:
            errors.append('Width must be between 100 and 2000')
        if not isinstance(height, int) or height < 100 or height > 2000:
            errors.append('Height must be between 100 and 2000')
        
        # Design-specific validations
        if design_type in ['suzhi', 'fourcolor', 'island', 'sikku', 'special']:
            iterations = data.get('iterations', 6)
            if not isinstance(iterations, int) or iterations < 1 or iterations > 10:
                errors.append('Iterations must be between 1 and 10')
        
        elif design_type == 'kambi':
            rhombus_size = data.get('rhombus_size', 5)
            if not isinstance(rhombus_size, int) or rhombus_size < 1 or rhombus_size > 15:
                errors.append('Rhombus size must be between 1 and 15')
                
        elif design_type == 'group':
            iterations = data.get('iterations', 4)
            if not isinstance(iterations, int) or iterations < 1 or iterations > 8:
                errors.append('Iterations must be between 1 and 8')
            polygon_sides = data.get('polygon_sides', 6)
            if not isinstance(polygon_sides, int) or polygon_sides < 3 or polygon_sides > 12:
                errors.append('Polygon sides must be between 3 and 12')
                
        elif design_type == 'traditional':
            iterations = data.get('iterations', 4)
            if not isinstance(iterations, int) or iterations < 1 or iterations > 6:
                errors.append('Iterations must be between 1 and 6')
            grid_size = data.get('grid_size', 7)
            if not isinstance(grid_size, int) or grid_size < 3 or grid_size > 15:
                errors.append('Grid size must be between 3 and 15')
            pattern_type = data.get('pattern_type', 'lotus')
            if pattern_type not in ['lotus', 'peacock', 'flower', 'geometric']:
                errors.append('Pattern type must be one of: lotus, peacock, flower, geometric')
        
        elif design_type == 'custom':
            coordinates = data.get('coordinates', [])
            if not isinstance(coordinates, list) or len(coordinates) < 2:
                errors.append('At least 2 coordinate points are required for custom design')
            
            for i, coord in enumerate(coordinates):
                if not isinstance(coord, dict) or 'x' not in coord or 'y' not in coord:
                    errors.append(f'Invalid coordinate at position {i+1}')
                    break
                try:
                    x, y = int(coord['x']), int(coord['y'])
                    if x < 0 or x > width or y < 0 or y > height:
                        errors.append(f'Coordinate {i+1} is outside canvas bounds')
                except (ValueError, TypeError):
                    errors.append(f'Coordinate {i+1} must have numeric x and y values')
        
        return jsonify({
            'valid': len(errors) == 0,
            'errors': errors
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
