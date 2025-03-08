# LottaWords - NYT Letter Boxed Solver

A professional implementation of a solver for the NYT Letter Boxed puzzle game, featuring both web interface and REST API.

![screenshot](https://github.com/user-attachments/assets/b7199c48-56c4-43f4-9b59-f43838133519)

## Features

- 🎮 Real-time puzzle fetching from NYT Letter Boxed
- 🧠 Smart solver using NYT's own dictionary for valid solutions
- 🧩 Complete solutions that use all letters in the puzzle
- 🔄 Daily automatic puzzle updates with scheduler
- 🚀 Responsive React frontend with animated solution paths
- 🔍 Intelligent caching system with time-based validation
- 📊 Comprehensive logging system
- 🛡️ Robust error handling and recovery
- 🌐 Clean REST API endpoints
- 🧪 Separation of frontend and backend for easier development

## Tech Stack

### Backend
- Python 3.8+
- Flask
- Selenium for web scraping
- APScheduler for automatic updates
- Caching with timestamp validation
- Proper logging

### Frontend
- React with TypeScript
- Styled Components
- SVG animations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LottaWords.git
cd LottaWords
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
cd backend
pip install -e .
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Usage

### Running the backend
```bash
cd backend
python app.py
```

### Running the frontend
```bash
cd frontend
npm start
```

The application will be available at http://localhost:3000 and will automatically connect to the backend at http://localhost:5000.

### API Documentation

#### GET /api/puzzle
Returns today's puzzle data and solutions.

Response:
```json
{
    "square": {
        "top": "WML",
        "right": "FRO",
        "bottom": "EIP",
        "left": "TUD"
    },
    "nyt_solution": ["FLOWERPOT", "TEDIUM"],
    "lotta_solution": ["MULTIFLOWERED"]
}
```

#### GET /api/status
Check if puzzle data is being scraped.

Response:
```json
{
    "cache_valid": true,
    "scraping_in_progress": false
}
```

## How It Works

1. The backend scrapes the current puzzle from the NYT Letter Boxed game website
2. It uses the NYT's own dictionary to ensure all solutions are valid
3. The solver finds the shortest solution that uses all letters in the puzzle
4. The frontend displays the puzzle and animates the solution paths
5. The app caches puzzle data and automatically updates it daily

## Key Features

### Time-Based Caching
The app maintains a cache that is valid until 3:05 AM EST, which is when NYT publishes a new puzzle.

### Smart Solver
The solver prioritizes shorter solutions that cover all letters in the puzzle, ensuring complete solutions.

### Resilient Loading
The frontend implements a retry mechanism to handle initial data loading, providing a smooth user experience.

## Development

### Running tests
```bash
cd backend
pytest
```

### Code formatting
```bash
black .
flake8
mypy .
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
