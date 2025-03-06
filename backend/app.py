from flask import Flask, render_template, jsonify
from flask_cors import CORS
import sys
import os

# Add the src directory to the path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

# Now try the import
from lottawords.scraper import LetterBoxedScraper
from lottawords.solver import LetterBoxedSolver

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_puzzle_solutions():
    scraper = LetterBoxedScraper()
    sides, nyt_solution = scraper.get_puzzle_data()
    square = {
        "top": sides[0],
        "right": sides[1],
        "bottom": sides[2],
        "left": sides[3]
    }
    
    solver = LetterBoxedSolver()
    # The solver needs lowercase for word matching, but we'll preserve the original case
    solver_square = {k: set(v.lower()) for k, v in square.items()}
    lotta_solution = solver.find_shortest_solution(solver_square)
    
    # Convert lotta_solution to match NYT case since we know they're uppercase
    lotta_solution = [word.upper() for word in lotta_solution] if lotta_solution else []
    
    return square, nyt_solution, lotta_solution

@app.route('/api/puzzle')
def get_puzzle():
    """Main API endpoint for puzzle data"""
    try:
        square, nyt_solution, lotta_solution = get_puzzle_solutions()
        return jsonify({
            'square': square,
            'nyt_solution': nyt_solution,
            'lotta_solution': lotta_solution,
            'error': None
        })
    except Exception as e:
        return jsonify({
            'square': None,
            'nyt_solution': None,
            'lotta_solution': None,
            'error': str(e)
        }), 500

@app.route('/')
def index():
    """Fallback route for the old template"""
    square, nyt_solution, lotta_solution = get_puzzle_solutions()
    return render_template('index.html', 
                         square=square,
                         nyt_solution=nyt_solution,
                         lotta_solution=lotta_solution)

if __name__ == '__main__':
    app.run(debug=True) 