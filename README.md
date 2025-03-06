# LottaWords - NYT Letter Boxed Solver

A professional implementation of a solver for the NYT Letter Boxed puzzle game, featuring both web interface and REST API.

## Features

- 🎮 Real-time puzzle fetching from NYT Letter Boxed
- 🧮 Advanced word-finding algorithm
- 🌐 Clean web interface
- 🔄 REST API endpoints
- 📊 Performance metrics and caching
- 🔍 Comprehensive test suite

## Tech Stack

- Python 3.8+
- Flask
- Selenium
- pytest
- Docker support

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

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
```

## Usage

### Running locally
```bash
python run.py
```

### Running with Docker
```bash
docker build -t lottawords .
docker run -p 5000:5000 lottawords
```

### API Documentation

#### GET /api/puzzle
Returns today's puzzle data and solutions.

Response:
```json
{
    "sides": [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"], ["J", "K", "L"]],
    "nyt_solution": ["word1", "word2"],
    "lotta_solution": ["word1", "word2", "word3"]
}
```

## Development

### Running tests
```bash
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