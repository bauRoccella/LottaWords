"""
Flask API module for LottaWords.
"""
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_caching import Cache
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple

from .solver import LetterBoxedSolver

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 3600  # 1 hour
})

def create_error_response(message: str, status_code: int = 400) -> Tuple[Dict[str, Any], int]:
    """Create standardized error response."""
    return jsonify({
        'error': message,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code

@cache.cached(timeout=3600, key_prefix='puzzle_solutions')
def get_puzzle_solutions():
    """Get puzzle data and solutions with caching."""
    try:
        scraper = LetterBoxedScraper()
        sides, nyt_solution = scraper.get_puzzle_data()
        
        square = {
            "top": set(sides[0]),
            "right": set(sides[1]),
            "bottom": set(sides[2]),
            "left": set(sides[3])
        }
        
        solver = LetterBoxedSolver()
        lotta_solution = solver.find_shortest_solution(square)
        
        return sides, nyt_solution, lotta_solution
        
    except Exception as e:
        logger.error(f"Error getting puzzle solutions: {str(e)}")
        raise

@app.route('/')
def index():
    """Render web interface."""
    try:
        sides, nyt_solution, lotta_solution = get_puzzle_solutions()
        return render_template('index.html',
                            sides=sides,
                            nyt_solution=nyt_solution,
                            lotta_solution=lotta_solution)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/puzzle')
def get_puzzle():
    """API endpoint for puzzle data."""
    try:
        sides, nyt_solution, lotta_solution = get_puzzle_solutions()
        return jsonify({
            'sides': sides,
            'nyt_solution': nyt_solution,
            'lotta_solution': lotta_solution,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return create_error_response(str(e), 500)

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }) 