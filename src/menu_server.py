"""Web-based menu server for preset selection"""

from flask import Flask, render_template, jsonify, request
import threading
import json

app = Flask(__name__)

class MenuServer:
    def __init__(self, visualizer, port=5000):
        self.visualizer = visualizer
        self.port = port
        self.server_thread = None

    def start(self):
        """Start the web server in background"""
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        print(f"Menu server started on http://localhost:{self.port}")

    def _run_server(self):
        """Run Flask server"""
        app.config['visualizer'] = self.visualizer
        app.run(host='127.0.0.1', port=self.port, debug=False, use_reloader=False)


@app.route('/')
def index():
    """Serve the menu interface"""
    return render_template('menu.html')


@app.route('/api/presets')
def get_presets():
    """Return all presets organized by category"""
    visualizer = app.config.get('visualizer')
    if not visualizer:
        return jsonify({'error': 'Visualizer not available'}), 500

    # Group presets by theme
    categories = {}
    for i, preset in enumerate(visualizer.presets):
        theme = preset.get('theme', 'Unknown')
        if theme not in categories:
            categories[theme] = []
        categories[theme].append({
            'id': i,
            'name': preset.get('name', f'Preset {i}'),
            'theme': theme,
            'description': preset.get('description', '')
        })

    # Sort categories, keeping 'core' first
    sorted_categories = {}
    if 'core' in categories:
        sorted_categories['Core'] = categories.pop('core')

    for theme in sorted(categories.keys()):
        # Capitalize theme name
        display_name = ' '.join(word.capitalize() for word in theme.split('_'))
        sorted_categories[display_name] = categories[theme]

    return jsonify(sorted_categories)


@app.route('/api/current-preset')
def get_current_preset():
    """Get current preset index"""
    visualizer = app.config.get('visualizer')
    if not visualizer:
        return jsonify({'error': 'Visualizer not available'}), 500

    return jsonify({
        'index': visualizer.current_preset_idx,
        'name': visualizer.presets[visualizer.current_preset_idx].get('name', 'Unknown')
    })


@app.route('/api/select-preset/<int:preset_id>', methods=['POST'])
def select_preset(preset_id):
    """Select a preset"""
    visualizer = app.config.get('visualizer')
    if not visualizer:
        return jsonify({'error': 'Visualizer not available'}), 500

    if 0 <= preset_id < len(visualizer.presets):
        visualizer.current_preset_idx = preset_id
        preset_name = visualizer.presets[preset_id].get('name', 'Unknown')
        print(f"Preset: {preset_name}")
        return jsonify({'success': True, 'preset': preset_name})

    return jsonify({'error': 'Invalid preset ID'}), 400


@app.route('/api/next-preset', methods=['POST'])
def next_preset_route():
    """Cycle to next preset"""
    visualizer = app.config.get('visualizer')
    if not visualizer:
        return jsonify({'error': 'Visualizer not available'}), 500

    visualizer.next_preset()
    return jsonify({'index': visualizer.current_preset_idx})


@app.route('/api/prev-preset', methods=['POST'])
def prev_preset_route():
    """Cycle to previous preset"""
    visualizer = app.config.get('visualizer')
    if not visualizer:
        return jsonify({'error': 'Visualizer not available'}), 500

    visualizer.prev_preset()
    return jsonify({'index': visualizer.current_preset_idx})
