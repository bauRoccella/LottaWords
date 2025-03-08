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
    def __init__(self):
        """Initialize solver without a default dictionary."""
        self.word_list = []  # Empty by default
        logger.info("Initialized solver without default dictionary")

    def _normalize_square(self, square: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
        """Convert all letters in square to lowercase sets."""
        normalized = {}
        for side, letters in square.items():
            if isinstance(letters, str):
                # Convert string to set of lowercase letters
                normalized[side] = {letter.lower() for letter in letters}
            else:
                # Convert each letter to lowercase
                normalized[side] = {letter.lower() for letter in letters}
        return normalized

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
            
        # Convert to lowercase for comparison
        word = word.lower() 
        
        # Convert square to lowercase for case-insensitive matching
        normalized_square = {}
        for side, letters in square.items():
            normalized_square[side] = {letter.lower() for letter in letters}
        
        # Check if all letters are in the square
        all_letters = set()
        for side_letters in normalized_square.values():
            all_letters.update(side_letters)
            
        # Check that all word letters are in the square
        for letter in word:
            if letter not in all_letters:
                return False
        
        # Find which side each letter belongs to
        letter_sides = {}
        for side, letters in normalized_square.items():
            for letter in letters:
                letter_sides[letter] = side
                
        # Check that consecutive letters are from different sides
        for i in range(1, len(word)):
            prev_letter = word[i-1]
            curr_letter = word[i]
            
            if letter_sides[prev_letter] == letter_sides[curr_letter]:
                return False
                
        return True

    def covers_all_letters(self, used_letters: Set[str], square: Dict[str, Set[str]]) -> bool:
        """Check if all letters in the square have been used."""
        # Make sure used_letters is lowercase for comparison
        used_letters = {letter.lower() for letter in used_letters}
        
        # Get all letters from the square (lowercase for comparison)
        all_letters = set()
        for side, letters in square.items():
            # Handle both string and set inputs
            if isinstance(letters, str):
                all_letters.update(letter.lower() for letter in letters)
            else:
                all_letters.update(letter.lower() for letter in letters)
        
        # Check if every letter from the puzzle is in the used_letters
        missing_letters = all_letters - used_letters
        if missing_letters:
            return False
            
        return True

    def word_priority(self, word: str, used_letters: Set[str]) -> int:
        """Calculate priority score for a word based on unused letters it contains."""
        word_letters = set(word)
        used_letters = {letter for letter in used_letters}
        return len(word_letters - used_letters)

    def find_shortest_solution(self, square: Dict[str, Set[str]], dictionary: List[str]) -> List[str]:
        """
        Find shortest solution that uses all letters.
        
        Args:
            square: Dictionary of sides with their letters
            dictionary: List of valid words to use (NYT dictionary)
            
        Returns:
            List of words forming the shortest solution, guaranteed to be a list (may be empty)
        """
        # Ensure all inputs are valid
        if not dictionary or not isinstance(dictionary, list):
            return []  # Return empty list, not None
            
        # Ensure all dictionary items are strings
        try:
            word_source = [str(word) for word in dictionary]
        except Exception as e:
            return []
        
        # Use normalized square without modifying input
        normalized_square = self._normalize_square(square)
        
        # Get valid words and sort by length (prefer shorter words)
        playable_words = []
        original_case = {}  # Map lowercase words to their original case
        
        for word in word_source:
            if not word:  # Skip empty strings
                continue
                
            word_lower = word.lower()
            is_valid = self.is_valid_word(word_lower, normalized_square)
            
            if is_valid:
                playable_words.append(word_lower)
                original_case[word_lower] = word  # Store original case
        
        if not playable_words:
            return []  # Return empty list, not None
            
        # Sort by length and then by number of unique letters
        playable_words.sort(key=lambda w: (len(w), -len(set(w))))
        
        # Create lookup maps for the search
        first_letter_map = {}
        unique_letters_map = {}  # Track unique letters in each word
        
        for word in playable_words:
            if not word:
                continue
                
            # Map for looking up words by first letter
            first_letter = word[0]
            if first_letter not in first_letter_map:
                first_letter_map[first_letter] = []
            first_letter_map[first_letter].append(word)
            
            # Map words to their unique letters (for prioritizing coverage)
            unique_letters_map[word] = set(word)
        
        # Get all unique letters in the puzzle for verification
        all_puzzle_letters = set()
        for side, letters in square.items():
            if isinstance(letters, str):
                all_puzzle_letters.update(letter.lower() for letter in letters)
            else:
                all_puzzle_letters.update(letter.lower() for letter in letters)
        
        queue: deque = deque()
        for word in playable_words:
            queue.append(([word], unique_letters_map[word]))
        
        visited = set()
        min_solution = None
        min_solution_len = float('inf')
        
        # Increase search limit for better solutions
        max_solution_length = 5
        search_iterations = 0
        max_iterations = 100000  # Increased to find better solutions
        
        while queue and search_iterations < max_iterations:
            search_iterations += 1
            
            current_words, used_letters = queue.popleft()
            
            # Skip if we already have a shorter solution
            if min_solution and len(current_words) >= min_solution_len:
                continue
            
            state = (tuple(current_words), ''.join(sorted(used_letters)))
            if state in visited:
                continue
            visited.add(state)
            
            # Check if this solution covers all letters in the puzzle
            if all_puzzle_letters.issubset(used_letters):
                # Double-check with the detailed verification
                if self.covers_all_letters(used_letters, square):
                    min_solution = current_words
                    min_solution_len = len(current_words)
                    # Early exit if we find a 2-word solution
                    if min_solution_len <= 2:
                        break
                continue

            # Only continue search if we haven't reached the maximum solution length
            if len(current_words) >= max_solution_length:
                continue
                
            # Find next words that can be played
            last_letter = current_words[-1][-1]
            
            # Use the first letter map for more efficient lookup
            next_words = first_letter_map.get(last_letter, [])
            
            # First prioritize by how many new, uncovered letters the word adds
            prioritized_words = []
            for word in next_words:
                new_letters = unique_letters_map[word] - used_letters
                # Score words higher if they add more unique letters
                prioritized_words.append((word, len(new_letters)))
            
            # Sort by number of new letters, then by word length (shorter preferred)
            prioritized_words.sort(key=lambda x: (-x[1], len(x[0])))
            
            # Limit the branching factor but consider more words at early depths
            branch_limit = 25 if len(current_words) == 1 else 15
            
            for word_info in prioritized_words[:branch_limit]:
                word = word_info[0]
                new_words = current_words + [word]
                new_letters = used_letters | unique_letters_map[word]
                queue.append((new_words, new_letters))
        
        # Always return a list, never None
        result = []
        if min_solution:
            # Convert solution back to original case
            try:
                result = [original_case[word] for word in min_solution]
            except Exception as e:
                # Fallback to lowercase solution if conversion fails
                result = min_solution
        elif playable_words:
            # If no solution found but we have valid words, return single longest word
            # Sort by unique letter coverage
            best_words = sorted(playable_words, 
                               key=lambda w: (len(set(w).intersection(all_puzzle_letters)), -len(w)))
            if best_words:
                best_word = best_words[-1]  # Word with most puzzle letter coverage
                result = [original_case.get(best_word, best_word)]
                
        # Final validation to ensure we're returning a list of strings
        if not isinstance(result, list):
            return []
            
        # Ensure all items are strings
        for i, item in enumerate(result):
            if not isinstance(item, str):
                result[i] = str(item)
                
        return result