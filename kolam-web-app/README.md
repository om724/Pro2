# Kolam Design Generator Web Application

A comprehensive web application for generating traditional Kolam designs using various algorithmic approaches including L-Systems, group theory, and custom coordinate patterns.

## Features

### Design Types Available

1. **Suzhi Kolam** - Traditional Suzhi Kolam pattern using L-Systems
2. **Kambi Kolam** - Kambi Kolam pattern within a rhombus shape  
3. **Four-Color Kolam** - Colorful Kolam with randomly changing colors
4. **Island Kolam** - Island-style Kolam with modified L-system rules
5. **Sikku Kolam** - Step-style Kolam with interlaced patterns
6. **Special Variety Kolam** - Advanced L-system with angle-based transformations
7. **Group Theory Kolam** - Polygon-based Kolam using group theory principles
8. **Custom Kolam** - Custom Kolam from user-defined coordinate points

### Parameters

- **Dot Size**: Controls the size of drawing elements (1-30)
- **Iterations**: Number of L-system iterations (1-10) 
- **Canvas Size**: Adjustable width and height (400-1200 x 300-900 pixels)
- **Rhombus Size**: For Kambi Kolam (1-15)
- **Polygon Sides**: For Group Theory Kolam (3-12)
- **Custom Coordinates**: Interactive coordinate input for custom designs

### Key Features

- **Real-time Generation**: Generate designs instantly with parameter changes
- **SVG Output**: High-quality scalable vector graphics
- **Download Support**: Save generated designs as SVG files
- **Interactive UI**: Intuitive controls with live parameter feedback
- **Responsive Design**: Works on desktop and mobile devices
- **Parameter Validation**: Input validation with helpful error messages

## Technology Stack

- **Backend**: Python Flask with SVG generation
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Graphics**: SVGwrite for vector graphics generation
- **Algorithms**: L-Systems, Group Theory, Coordinate-based drawing

## Installation

1. **Setup Virtual Environment**:
   ```bash
   cd kolam-web-app
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Linux/Mac
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open your browser and navigate to `http://localhost:5000`

## API Endpoints

- `GET /` - Main application page
- `POST /api/generate-kolam` - Generate Kolam design
- `GET /api/design-types` - Get available design types
- `POST /api/validate-parameters` - Validate input parameters

## Usage Instructions

1. **Select Design Type**: Choose from the dropdown menu
2. **Adjust Parameters**: Use sliders and inputs to customize your design
3. **Generate**: Click "Generate Kolam" to create your design
4. **Download**: Save your creation as an SVG file
5. **Experiment**: Try different combinations for unique patterns

## Mathematical Background

### L-Systems
The application uses Lindenmayer Systems (L-Systems) for algorithmic pattern generation:
- **Axiom**: Starting string (e.g., "FBFBFBFB")
- **Rules**: Transformation rules for each symbol
- **Iterations**: Number of rule applications

### Group Theory
Polygon-based designs use mathematical group theory principles:
- Symmetric transformations
- Rotational and reflection symmetries
- Regular polygon constructions

## File Structure

```
kolam-web-app/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── backend/
│   ├── __init__.py
│   └── kolam_generator.py # Core Kolam generation logic
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── styles.css    # Application styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── README.md
```

## Contributing

This application integrates various traditional Kolam generation techniques from the SIH project folder. To add new design types:

1. Add the L-System rules to `kolam_generator.py`
2. Update the Flask API endpoints in `app.py`
3. Add UI controls in `index.html`
4. Update JavaScript logic in `app.js`

## Traditional Kolam Patterns

The application preserves and digitizes traditional South Indian Kolam art forms:
- Maintains authentic geometric patterns
- Respects cultural significance
- Enables preservation through technology
- Supports educational use

## License

This project is part of the Smart India Hackathon (SIH) initiative for preserving traditional Indian art forms through modern technology.
