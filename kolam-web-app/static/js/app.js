class KolamApp {
    constructor() {
        this.currentSVG = null;
        this.coordinates = [];
        this.initializeEventListeners();
        this.updateParameterVisibility();
    }

    initializeEventListeners() {
        // Design type change
        document.getElementById('designType').addEventListener('change', () => {
            this.updateParameterVisibility();
            this.updateDesignTypeHelp();
        });

        // Range input updates
        const rangeInputs = ['dotSize', 'iterations', 'rhombusSize', 'polygonSides', 'gridSize', 
                           'polygonVertices', 'polygonSize', 'circleRadius'];
        rangeInputs.forEach(id => {
            const input = document.getElementById(id);
            if (input) {
                input.addEventListener('input', () => {
                    document.getElementById(id + 'Value').textContent = input.value;
                });
            }
        });

        // Canvas size updates
        ['canvasWidth', 'canvasHeight'].forEach(id => {
            document.getElementById(id).addEventListener('change', () => {
                this.updateCanvasSize();
            });
        });

        // Generate Kolam button
        document.getElementById('generateKolam').addEventListener('click', () => {
            this.generateKolam();
        });

        // Clear Canvas button
        document.getElementById('clearCanvas').addEventListener('click', () => {
            this.clearCanvas();
        });

        // Download SVG button
        document.getElementById('downloadSVG').addEventListener('click', () => {
            this.downloadSVG();
        });

        // Custom coordinates management
        document.getElementById('addCoordinate').addEventListener('click', () => {
            this.addCoordinateInput();
        });

        // Canvas click for custom coordinates
        document.getElementById('kolamCanvas').addEventListener('click', (e) => {
            if (document.getElementById('designType').value === 'custom') {
                this.addCoordinateFromClick(e);
            }
        });

        // Remove coordinate buttons (delegation)
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-remove-coord')) {
                this.removeCoordinateInput(e.target.parentElement);
            }
        });
    }

    updateParameterVisibility() {
        const designType = document.getElementById('designType').value;
        
        // Hide all parameter groups
        document.querySelectorAll('.suzhi-params, .kambi-params, .group-params, .traditional-params, .polygon-params, .circle-params, .custom-params').forEach(el => {
            el.style.display = 'none';
        });

        // Show relevant parameter group
        if (['suzhi', 'fourcolor', 'island', 'sikku', 'special', 'single_knot', 'combined'].includes(designType)) {
            document.querySelector('.suzhi-params').style.display = 'block';
        } else if (['kambi', 'rhombus'].includes(designType)) {
            document.querySelector('.kambi-params').style.display = 'block';
        } else if (designType === 'group') {
            document.querySelector('.suzhi-params').style.display = 'block';
            document.querySelector('.group-params').style.display = 'block';
        } else if (designType === 'traditional') {
            document.querySelector('.suzhi-params').style.display = 'block';
            document.querySelector('.traditional-params').style.display = 'block';
        } else if (designType === 'polygon_inscribed') {
            document.querySelector('.suzhi-params').style.display = 'block';
            document.querySelector('.polygon-params').style.display = 'block';
        } else if (designType === 'circle_inscribed') {
            document.querySelector('.suzhi-params').style.display = 'block';
            document.querySelector('.circle-params').style.display = 'block';
        } else if (designType === 'custom') {
            document.querySelector('.custom-params').style.display = 'block';
        }
    }

    updateDesignTypeHelp() {
        const designType = document.getElementById('designType').value;
        const helpElement = document.getElementById('designTypeHelp');
        
        const helpTexts = {
            'suzhi': 'Traditional Suzhi Kolam pattern using L-Systems',
            'kambi': 'Kambi Kolam pattern within a rhombus shape',
            'fourcolor': 'Colorful Kolam with randomly changing colors',
            'island': 'Island-style Kolam with modified L-system rules',
            'sikku': 'Step-style Kolam with interlaced patterns',
            'special': 'Advanced L-system with angle-based transformations',
            'group': 'Polygon-based Kolam using group theory principles',
            'traditional': 'Authentic Indian Rangoli designs with intricate patterns',
            'single_knot': 'Exact implementation from SIH kollamsingleknot.py - authentic colored L-System',
            'rhombus': 'From SIH rombaturtlekolam.py - L-System within rhombus boundary',
            'polygon_inscribed': 'From SIH rombaturtlekolamgghpoly.py - multiple kolams in polygons',
            'circle_inscribed': 'From SIH rombaturtlekolamgghpolycircle.py - concentric circular patterns',
            'combined': 'From SIH suzhisikkukambikolam.py - three traditional patterns combined',
            'custom': 'Custom Kolam from coordinate points'
        };
        
        helpElement.textContent = helpTexts[designType] || '';
    }

    updateCanvasSize() {
        const width = document.getElementById('canvasWidth').value;
        const height = document.getElementById('canvasHeight').value;
        
        const canvas = document.getElementById('kolamCanvas');
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
    }

    addCoordinateInput() {
        const container = document.querySelector('.coordinates-container');
        const coordinateDiv = document.createElement('div');
        coordinateDiv.className = 'coordinate-input';
        coordinateDiv.innerHTML = `
            <input type="number" placeholder="X" class="coord-input" data-axis="x">
            <input type="number" placeholder="Y" class="coord-input" data-axis="y">
            <button type="button" class="btn-remove-coord">Remove</button>
        `;
        container.appendChild(coordinateDiv);
    }

    removeCoordinateInput(element) {
        const container = document.querySelector('.coordinates-container');
        if (container.children.length > 2) { // Keep at least 2 coordinate inputs
            element.remove();
        } else {
            this.showError('At least 2 coordinate points are required');
        }
    }

    addCoordinateFromClick(event) {
        const canvas = document.getElementById('kolamCanvas');
        const rect = canvas.getBoundingClientRect();
        const x = Math.round(event.clientX - rect.left);
        const y = Math.round(event.clientY - rect.top);

        // Add a new coordinate input with these values
        this.addCoordinateInput();
        const inputs = document.querySelectorAll('.coordinate-input:last-child .coord-input');
        inputs[0].value = x; // X coordinate
        inputs[1].value = y; // Y coordinate

        // Visual feedback
        this.showStatus(`Added coordinate: (${x}, ${y})`);
    }

    collectFormData() {
        const designType = document.getElementById('designType').value;
        const data = {
            design_type: designType,
            dot_size: parseInt(document.getElementById('dotSize').value),
            width: parseInt(document.getElementById('canvasWidth').value),
            height: parseInt(document.getElementById('canvasHeight').value)
        };

        if (['suzhi', 'fourcolor', 'island', 'sikku', 'special', 'single_knot', 'combined'].includes(designType)) {
            data.iterations = parseInt(document.getElementById('iterations').value);
        } else if (['kambi', 'rhombus'].includes(designType)) {
            data.rhombus_size = parseInt(document.getElementById('rhombusSize').value);
        } else if (designType === 'group') {
            data.iterations = parseInt(document.getElementById('iterations').value);
            data.polygon_sides = parseInt(document.getElementById('polygonSides').value);
        } else if (designType === 'traditional') {
            data.iterations = parseInt(document.getElementById('iterations').value);
            data.grid_size = parseInt(document.getElementById('gridSize').value);
            data.pattern_type = document.getElementById('patternType').value;
        } else if (designType === 'polygon_inscribed') {
            data.iterations = parseInt(document.getElementById('iterations').value);
            data.polygon_vertices = parseInt(document.getElementById('polygonVertices').value);
            data.polygon_size = parseInt(document.getElementById('polygonSize').value);
        } else if (designType === 'circle_inscribed') {
            data.iterations = parseInt(document.getElementById('iterations').value);
            data.circle_radius = parseInt(document.getElementById('circleRadius').value);
        } else if (designType === 'custom') {
            data.coordinates = this.collectCoordinates();
        }

        return data;
    }

    collectCoordinates() {
        const coordinates = [];
        const coordinateInputs = document.querySelectorAll('.coordinate-input');
        
        coordinateInputs.forEach(input => {
            const xInput = input.querySelector('[data-axis="x"]');
            const yInput = input.querySelector('[data-axis="y"]');
            
            if (xInput.value && yInput.value) {
                coordinates.push({
                    x: parseInt(xInput.value),
                    y: parseInt(yInput.value)
                });
            }
        });
        
        return coordinates;
    }

    async generateKolam() {
        try {
            this.showLoading(true);
            this.clearMessages();

            const formData = this.collectFormData();
            
            // Validate data first
            const validationResponse = await fetch('/api/validate-parameters', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const validationResult = await validationResponse.json();
            
            if (!validationResult.valid) {
                this.showError('Validation errors: ' + validationResult.errors.join(', '));
                return;
            }

            // Generate Kolam
            const response = await fetch('/api/generate-kolam', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                this.displayKolam(result.svg);
                this.showDesignInfo(result.parameters);
                this.showStatus('Kolam generated successfully!');
                document.getElementById('downloadSVG').disabled = false;
            } else {
                this.showError('Failed to generate Kolam: ' + result.error);
            }

        } catch (error) {
            this.showError('Error generating Kolam: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    displayKolam(svgContent) {
        const canvas = document.getElementById('kolamCanvas');
        canvas.innerHTML = svgContent;
        this.currentSVG = svgContent;

        // Make SVG responsive
        const svg = canvas.querySelector('svg');
        if (svg) {
            svg.style.width = '100%';
            svg.style.height = '100%';
            svg.style.display = 'block';
        }
    }

    clearCanvas() {
        const canvas = document.getElementById('kolamCanvas');
        canvas.innerHTML = `
            <div class="placeholder-text">
                <p>🎨 Your beautiful Kolam design will appear here</p>
                <p>Select parameters and click "Generate Kolam" to start</p>
            </div>
        `;
        this.currentSVG = null;
        document.getElementById('downloadSVG').disabled = true;
        this.clearMessages();
        
        // Reset design info
        document.getElementById('designInfo').innerHTML = 
            '<p>Select a design type and generate a Kolam to see detailed information.</p>';
    }

    downloadSVG() {
        if (!this.currentSVG) {
            this.showError('No Kolam design to download');
            return;
        }

        const blob = new Blob([this.currentSVG], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `kolam-${document.getElementById('designType').value}-${Date.now()}.svg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showStatus('Kolam SVG downloaded successfully!');
    }

    showDesignInfo(parameters) {
        const designInfo = document.getElementById('designInfo');
        let infoHTML = `
            <p><strong>Design Type:</strong> ${parameters.design_type.charAt(0).toUpperCase() + parameters.design_type.slice(1)} Kolam</p>
            <p><strong>Canvas Size:</strong> ${parameters.width} × ${parameters.height} pixels</p>
            <p><strong>Dot Size:</strong> ${parameters.dot_size}</p>
        `;
        
        if (parameters.iterations) {
            infoHTML += `<p><strong>Iterations:</strong> ${parameters.iterations}</p>`;
        }
        
        if (parameters.rhombus_size) {
            infoHTML += `<p><strong>Rhombus Size:</strong> ${parameters.rhombus_size}</p>`;
        }
        
        infoHTML += `<p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>`;
        
        designInfo.innerHTML = infoHTML;
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        const generateBtn = document.getElementById('generateKolam');
        
        if (show) {
            spinner.style.display = 'block';
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';
        } else {
            spinner.style.display = 'none';
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Kolam';
        }
    }

    showStatus(message) {
        const statusElement = document.getElementById('statusMessage');
        statusElement.textContent = message;
        statusElement.style.display = 'block';
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 3000);
    }

    showError(message) {
        const errorElement = document.getElementById('errorMessage');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    }

    clearMessages() {
        document.getElementById('statusMessage').style.display = 'none';
        document.getElementById('errorMessage').style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new KolamApp();
});
