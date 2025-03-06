"""
Command line interface for LottaWords solver.
"""
import argparse
import logging
from typing import Dict, Set
from .solver import LetterBoxedSolver

def parse_square(square_str: str) -> Dict[str, Set[str]]:
    """Parse square string format 'top:ABC,right:DEF,bottom:GHI,left:JKL'."""
    square = {}
    try:
        for side in square_str.split(','):
            name, letters = side.split(':')
            square[name] = set(letters.upper())
        return square
    except ValueError:
        raise ValueError(
            "Invalid square format. Use: top:ABC,right:DEF,bottom:GHI,left:JKL"
        )

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='Solve NYT Letter Boxed puzzles')
    parser.add_argument(
        '--square', 
        type=str,
        help="Square format: top:ABC,right:DEF,bottom:GHI,left:JKL",
        required=True
    )
    parser.add_argument(
        '--wordlist',
        type=str,
        default='words_alpha.txt',
        help='Path to word list file (default: words_alpha.txt)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )

    try:
        # Parse square
        square = parse_square(args.square)
        
        # Create solver
        solver = LetterBoxedSolver(args.wordlist)
        
        # Find solution
        solution = solver.find_shortest_solution(square)
        
        if solution:
            print("\nFound solution:")
            for i, word in enumerate(solution, 1):
                print(f"{i}. {word}")
            print(f"\nTotal words: {len(solution)}")
        else:
            print("\nNo solution found!")
            
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print(f"Error: Word list file '{args.wordlist}' not found")

if __name__ == '__main__':
    main() 