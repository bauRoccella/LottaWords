"""
LottaWords solver module for NYT Letter Boxed puzzle.
"""
from collections import deque
from typing import Dict, List, Set, Optional, Tuple
import logging
import copy
import os
import pkg_resources
import sys

logger = logging.getLogger(__name__)

class LetterBoxedSolver:
    def __init__(self, word_file: str = "data/words_alpha.txt"):
        """Initialize solver with word dictionary."""
        self.word_list = self._load_words(word_file)
        logger.info(f"Loaded {len(self.word_list)} words from dictionary")

    def _load_words(self, filename: str) -> List[str]:
        """Load words from dictionary file with fallback strategies."""
        # Get paths to try
        module_dir = os.path.dirname(os.path.abspath(__file__))
        paths_to_try = [
            # Option 1: Direct path from module directory
            os.path.join(module_dir, 'data', os.path.basename(filename)),
            # Option 2: Path relative to current working directory
            os.path.join(os.getcwd(), 'src', 'lottawords', 'data', os.path.basename(filename)),
            # Option 3: If just filename provided
            os.path.join(module_dir, os.path.basename(filename)),
            # Option 4: Original path unchanged
            filename
        ]
        
        # Try pkg_resources as last resort
        try:
            pkg_path = pkg_resources.resource_filename('lottawords', 
                                                      f'data/{os.path.basename(filename)}')
            paths_to_try.append(pkg_path)
        except Exception:
            pass
        
        # Try each path
        for path in paths_to_try:
            try:
                print(f"Trying to load words from: {path}")
                if os.path.exists(path):
                    with open(path, "r") as file:
                        words = [line.strip() for line in file if len(line.strip()) >= 3]
                        print(f"Successfully loaded {len(words)} words from {path}")
                        return words
            except Exception as e:
                print(f"Failed to load from {path}: {e}")
        
        # If all paths fail
        print(f"ERROR: Failed to find word file. Tried: {paths_to_try}")
        return []

    def _normalize_square(self, square: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
        """Convert all letters in square to lowercase."""
        return {side: {letter for letter in letters} for side, letters in square.items()}

    def is_valid_word(self, word: str, square: Dict[str, Set[str]]) -> bool:
        """
        Check if word is valid according to Letter Boxed rules.
        Rules:
        1. All letters must be in the square
        2. Each letter must come from a different side than the previous letter
           (e.g., if letter1 is from top, letter2 must be from right/bottom/left,
            but letter3 could be from top again)
        3. Letters can be used multiple times
        4. Case insensitive
        """
        if not word:
            return False
            
        
        # Use normalized square without modifying input
        normalized_square = self._normalize_square(square)
        logger.debug(f"Checking word '{word}' against square {normalized_square}")
        
        # First, verify all letters exist in the square
        word_letters = set(word)
        all_square_letters = set().union(*normalized_square.values())
        logger.debug(f"Word letters: {word_letters}")
        logger.debug(f"Square letters: {all_square_letters}")
        
        if not word_letters.issubset(all_square_letters):
            logger.debug(f"Word contains letters not in square: {word_letters - all_square_letters}")
            return False
        
        # Find which side each letter belongs to
        letter_sides = {}
        for side, letters in normalized_square.items():
            for letter in letters:
                letter_sides[letter] = side
        
        # Check that each letter is from a different side than the previous letter
        prev_letter = None
        for letter in word:
            if prev_letter:
                if letter_sides[letter] == letter_sides[prev_letter]:
                    logger.debug(f"Invalid: letter '{letter}' is from same side as previous letter '{prev_letter}' ({letter_sides[letter]})")
                    return False
            prev_letter = letter
        
        logger.debug(f"Word '{word}' is valid")
        return True

    def covers_all_letters(self, used_letters: Set[str], square: Dict[str, Set[str]]) -> bool:
        """Check if all letters in the square are used."""
        normalized_square = self._normalize_square(square)
        all_letters = set().union(*normalized_square.values())
        used_letters = {letter for letter in used_letters}
        return all_letters.issubset(used_letters)

    def word_priority(self, word: str, used_letters: Set[str]) -> int:
        """Calculate priority score for a word based on unused letters it contains."""
        word_letters = set(word)
        used_letters = {letter for letter in used_letters}
        return len(word_letters - used_letters)

    def find_shortest_solution(self, square: Dict[str, Set[str]]) -> Optional[List[str]]:
        """Find shortest solution that uses all letters."""
        # Use normalized square without modifying input
        normalized_square = self._normalize_square(square)
        logger.debug(f"Normalized square: {normalized_square}")
        
        # Get valid words and sort by length (prefer shorter words)
        playable_words = []
        for word in self.word_list:
            if self.is_valid_word(word, normalized_square):
                playable_words.append(word)
                logger.debug(f"Valid word found: {word}")
        
        logger.debug(f"Found {len(playable_words)} valid words: {playable_words}")
        
        # Sort by length and then by number of unique letters
        playable_words.sort(key=lambda w: (len(w), -len(set(w))))
        logger.debug(f"Sorted playable words: {playable_words}")
        
        queue: deque = deque()
        for word in playable_words:
            queue.append(([word], set(word)))
            logger.debug(f"Added initial word to queue: {word}")

        visited = set()
        min_solution = None
        min_solution_len = float('inf')

        while queue:
            current_words, used_letters = queue.popleft()
            logger.debug(f"\nChecking path: {current_words}")
            logger.debug(f"Used letters: {sorted(used_letters)}")
            
            # Skip if we already have a shorter solution
            if len(current_words) >= min_solution_len:
                logger.debug("Skipping - longer than current best solution")
                continue
            
            state = (tuple(current_words), ''.join(sorted(used_letters)))
            if state in visited:
                logger.debug("Skipping - state already visited")
                continue
            visited.add(state)

            if self.covers_all_letters(used_letters, normalized_square):
                logger.info(f"Found solution with {len(current_words)} words: {current_words}")
                min_solution = current_words
                min_solution_len = len(current_words)
                continue

            last_letter = current_words[-1][-1]
            next_words = [w for w in playable_words if w[0] == last_letter]
            logger.debug(f"Possible next words starting with '{last_letter}': {next_words}")
            
            # Sort next words by priority (number of new letters) and length
            next_words.sort(key=lambda w: (-self.word_priority(w, used_letters), len(w)))
            logger.debug(f"Sorted next words: {next_words}")

            for word in next_words[:10]:  # Limit branching factor
                if len(current_words) < 4:  # Limit solution length
                    new_words = current_words + [word]
                    new_letters = used_letters | set(word)
                    queue.append((new_words, new_letters))
                    logger.debug(f"Added new path to queue: {new_words}")

        if min_solution:
            return min_solution
        
        logger.warning("No solution found")
        return None 