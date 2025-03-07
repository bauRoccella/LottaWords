import os
import sys
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
import pytz

# Set up Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.lottawords.scraper import LetterBoxedScraper
from src.lottawords.solver import LetterBoxedSolver

app = Flask(__name__)
CORS(app)

# Cache to store puzzle data
cache = {
    'puzzle_data': None,
    'last_updated': None
}

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'puzzle_cache.json')

def load_cache_from_file():
    """Load cached puzzle data from file if it exists and is from today"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                saved_cache = json.load(f)
            
            # Check if cache is from today
            last_updated = datetime.fromisoformat(saved_cache['last_updated'])
            today = datetime.now().date()
            if last_updated.date() == today:
                cache['puzzle_data'] = saved_cache['puzzle_data']
                cache['last_updated'] = saved_cache['last_updated']
                print(f"Loaded cache from {last_updated}")
            else:
                print(f"Cache from {last_updated.date()} is outdated (today is {today})")
        except Exception as e:
            print(f"Error loading cache: {e}")

def save_cache_to_file():
    """Save current puzzle data to cache file"""
    if cache['puzzle_data'] and cache['last_updated']:
        try:
            with open(CACHE_FILE, 'w') as f:
                json.dump(cache, f)
            print(f"Cache saved to {CACHE_FILE}")
        except Exception as e:
            print(f"Error saving cache: {e}")

def fetch_puzzle_data():
    """Fetch fresh puzzle data from NYT and solve it"""
    try:
        print("Fetching new puzzle data...")
        scraper = LetterBoxedScraper()
        sides, nyt_solution = scraper.get_puzzle_data()
        
        # Format sides into a square dictionary as expected by find_shortest_solution
        square = {
            "top": set(sides[0]),
            "right": set(sides[1]),
            "bottom": set(sides[2]),
            "left": set(sides[3])
        }
        
        solver = LetterBoxedSolver()
        lotta_solution = solver.find_shortest_solution(square)
        
        # Format for consistent response
        formatted_data = {
            'square': {
                'top': sides[0],
                'right': sides[1],
                'bottom': sides[2],
                'left': sides[3]
            },
            'nyt_solution': nyt_solution,
            'lotta_solution': lotta_solution,
            'error': None
        }
        
        # Update cache
        cache['puzzle_data'] = formatted_data
        cache['last_updated'] = datetime.now().isoformat()
        
        # Save to file
        save_cache_to_file()
        
        print("Puzzle data updated successfully")
        return formatted_data
    except Exception as e:
        import traceback
        print(f"Error fetching puzzle data: {e}")
        print(traceback.format_exc())
        return {'error': str(e)}

@app.route('/api/puzzle')
def get_puzzle_data():
    """API endpoint to get puzzle data (from cache if available)"""
    # Check if we have valid cached data from today
    if cache['puzzle_data'] and cache['last_updated']:
        last_updated = datetime.fromisoformat(cache['last_updated'])
        # If cache is from today, use it
        if last_updated.date() == datetime.now().date():
            return jsonify(cache['puzzle_data'])
    
    # Otherwise fetch fresh data
    result = fetch_puzzle_data()
    if 'error' in result and result['error']:
        return jsonify(result), 500
    return jsonify(result)

def init_scheduler():
    """Initialize the scheduler to update puzzle data at 3:05 AM EST (when NYT updates)"""
    scheduler = BackgroundScheduler()
    
    # Schedule job to run at 3:05 AM EST every day
    scheduler.add_job(
        fetch_puzzle_data,
        CronTrigger(
            hour=3, 
            minute=5, 
            timezone=pytz.timezone('US/Eastern')
        ),
        id='fetch_daily_puzzle'
    )
    
    scheduler.start()
    print("Scheduler started - puzzle will update daily at 3:05 AM EST")
    
    # Shutdown scheduler when app exits
    atexit.register(lambda: scheduler.shutdown())

# On startup: load cache and initialize scheduler
load_cache_from_file()
init_scheduler()

# Fetch puzzle data on startup if needed
if not cache['puzzle_data'] or not cache['last_updated']:
    fetch_puzzle_data()

@app.route('/')
def index():
    """Fallback route for the old template"""
    square, nyt_solution, lotta_solution = get_puzzle_data()
    return render_template('index.html', 
                         square=square,
                         nyt_solution=nyt_solution,
                         lotta_solution=lotta_solution)

if __name__ == '__main__':
    app.run(debug=True) 