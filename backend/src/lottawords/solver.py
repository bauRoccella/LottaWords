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
        
        # Debug output
        print(f"Checking word '{word}' against square {normalized_square}")
        
        # Check if all letters are in the square
        all_letters = set()
        for side_letters in normalized_square.values():
            all_letters.update(side_letters)
            
        # Check that all word letters are in the square
        for letter in word:
            if letter not in all_letters:
                print(f"Word '{word}' contains letter '{letter}' not in the square")
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
                print(f"Word '{word}' has consecutive letters from same side: {prev_letter}, {curr_letter}")
                return False
                
        print(f"Word '{word}' is valid")
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
                
        print(f"Checking coverage - All letters in puzzle: {sorted(all_letters)}")
        print(f"Letters used in solution: {sorted(used_letters)}")
        
        # Check if every letter from the puzzle is in the used_letters
        missing_letters = all_letters - used_letters
        if missing_letters:
            print(f"Missing letters: {sorted(missing_letters)}")
            return False
            
        print("Solution covers all letters!")
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
            print("ERROR: Invalid dictionary input, must be a non-empty list")
            return []  # Return empty list, not None
            
        # Ensure all dictionary items are strings
        try:
            word_source = [str(word) for word in dictionary]
        except Exception as e:
            print(f"ERROR converting dictionary items to strings: {e}")
            return []
        
        # Debug the square structure
        print(f"Square before normalization: {square}")
        
        # Use normalized square without modifying input
        normalized_square = self._normalize_square(square)
        print(f"Normalized square: {normalized_square}")
        
        # Debug - check the structure of the first few words
        if word_source:
            print(f"Dictionary sample (first 5): {word_source[:5]}")
        
        # Get valid words and sort by length (prefer shorter words)
        playable_words = []
        original_case = {}  # Map lowercase words to their original case
        
        # Check a sample of words to debug validation
        sample_words = word_source[:20] if len(word_source) > 20 else word_source
        print(f"Testing sample of {len(sample_words)} words for validity")
        
        for word in word_source:
            if not word:  # Skip empty strings
                continue
                
            word_lower = word.lower()
            is_valid = self.is_valid_word(word_lower, normalized_square)
            
            if is_valid:
                playable_words.append(word_lower)
                original_case[word_lower] = word  # Store original case
                
        print(f"Found {len(playable_words)} valid words out of {len(word_source)} total dictionary words")
        
        if playable_words:
            print(f"Valid words sample: {playable_words[:5]}")
        
        if not playable_words:
            print("No valid words found, returning empty solution")
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
                
        print(f"Total puzzle letters to cover: {sorted(all_puzzle_letters)}")
        
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
                print(f"Found solution with {len(current_words)} words: {current_words}")
                print(f"Letter coverage: {len(used_letters)}/{len(all_puzzle_letters)} letters")
                
                # Double-check with the detailed verification
                if self.covers_all_letters(used_letters, square):
                    min_solution = current_words
                    min_solution_len = len(current_words)
                    # Early exit if we find a 2-word solution
                    if min_solution_len <= 2:
                        break
                else:
                    print("Warning: Potential solution fails verification - continuing search")
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
        
        print(f"Search completed after {search_iterations} iterations")
        
        # Always return a list, never None
        result = []
        if min_solution:
            # Convert solution back to original case
            try:
                result = [original_case[word] for word in min_solution]
                print(f"Final solution: {result}")
                
                # Verify once more that result covers all letters
                used_letters = set()
                for word in result:
                    used_letters.update(letter.lower() for letter in word)
                
                missing = all_puzzle_letters - {l.lower() for l in used_letters}
                if missing:
                    print(f"WARNING: Final solution is missing letters: {missing}")
                else:
                    print("Final solution covers all puzzle letters!")
            except Exception as e:
                print(f"ERROR converting solution to original case: {e}")
                # Fallback to lowercase solution if conversion fails
                result = min_solution
        elif playable_words:
            # If no solution found but we have valid words, return single longest word
            print("No complete solution found - finding best partial solution")
            # Sort by unique letter coverage
            best_words = sorted(playable_words, 
                               key=lambda w: (len(set(w).intersection(all_puzzle_letters)), -len(w)))
            if best_words:
                best_word = best_words[-1]  # Word with most puzzle letter coverage
                result = [original_case.get(best_word, best_word)]
                print(f"Using partial solution: {result}")
                
                # Show which letters are still uncovered
                covered = set(best_word.lower())
                missing = all_puzzle_letters - covered
                print(f"Partial solution missing letters: {missing}")
        
        # Final validation to ensure we're returning a list of strings
        if not isinstance(result, list):
            print(f"ERROR: Result is not a list: {result}")
            return []
            
        # Ensure all items are strings
        for i, item in enumerate(result):
            if not isinstance(item, str):
                print(f"WARNING: Solution item {i} is not a string: {item}")
                result[i] = str(item)
                
        return result