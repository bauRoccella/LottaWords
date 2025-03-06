"""
Tests for the LetterBoxed solver module.
"""
import pytest
import logging
from lottawords.solver import LetterBoxedSolver

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def solver():
    """Create a solver instance for testing."""
    return LetterBoxedSolver()

@pytest.fixture
def sample_square():
    """Create a sample puzzle square for testing."""
    return {
        "top": {"A", "B", "C"},
        "right": {"D", "E", "F"},
        "bottom": {"G", "H", "I"},
        "left": {"J", "K", "L"}
    }

def test_is_valid_word(solver, sample_square):
    """Test word validation logic."""
    # Valid words - consecutive letters must be from different sides
    assert solver.is_valid_word("CHJC", sample_square), "CHJC should be valid: C(top)->H(bottom)->J(left)->C(top)"
    assert solver.is_valid_word("CHLD", sample_square), "CHLD should be valid: C(top)->H(bottom)->L(left)->D(right)"
    
    # Invalid words - consecutive letters from same side
    assert not solver.is_valid_word("CHEF", sample_square), "CHEF should be invalid (E->F from same side)"
    assert not solver.is_valid_word("BDE", sample_square), "BDE should be invalid (D->E from same side)"
    assert not solver.is_valid_word("ABC", sample_square), "ABC should be invalid (A->B from same side)"
    assert not solver.is_valid_word("BAD", sample_square), "BAD should be invalid (B->A from same side)"
    
    # Invalid words - non-existent letters
    assert not solver.is_valid_word("XYZ", sample_square), "XYZ should be invalid (letters not in square)"
    
    # Case insensitivity
    assert solver.is_valid_word("ChJc", sample_square), "ChJc should be valid (case insensitive)"

def test_covers_all_letters(solver, sample_square):
    """Test letter coverage checking."""
    # Complete coverage
    all_letters = set("ABCDEFGHIJKL")
    assert solver.covers_all_letters(all_letters, sample_square)
    
    # Partial coverage
    partial_letters = set("ABCDEF")
    assert not solver.covers_all_letters(partial_letters, sample_square)

def test_word_priority(solver):
    """Test word priority scoring."""
    used_letters = set("ABC")
    
    # Word with all new letters
    assert solver.word_priority("DEF", used_letters) == 3
    
    # Word with some new letters
    assert solver.word_priority("ABD", used_letters) == 1
    
    # Word with no new letters
    assert solver.word_priority("CAB", used_letters) == 0

def test_find_shortest_solution(solver, sample_square):
    """Test solution finding."""
    # Mock word list for testing - each word must have consecutive letters from different sides
    solver.word_list = [
        "AGBHCI",   # A(top)->G(bottom)->B(top)->H(bottom)->C(top)->I(bottom)
        "IJDKELF"   # I(bottom)->J(left)->D(right)->K(left)->E(right)->L(left)->F(right)
    ]
    logging.debug(f"Test word list: {solver.word_list}")

    solution = solver.find_shortest_solution(sample_square)
    logging.debug(f"Found solution: {solution}")

    # Check that we got a solution
    assert solution is not None, "Should find a solution with the test word list"
    
    # Check that solution is valid
    for i in range(len(solution) - 1):
        assert solution[i][-1] == solution[i + 1][0], f"Words should chain: {solution[i]} -> {solution[i + 1]}"
        
    # Check that all words are valid
    for word in solution:
        assert solver.is_valid_word(word, sample_square), f"Word {word} should be valid"
        
    # Check letter coverage
    used_letters = set(''.join(solution))
    assert solver.covers_all_letters(used_letters, sample_square), "Solution should use all letters"

def test_no_solution(solver, sample_square):
    """Test behavior when no solution exists."""
    # Empty word list
    solver.word_list = []
    assert solver.find_shortest_solution(sample_square) is None
    
    # Word list with no valid solutions
    solver.word_list = ["XYZ", "ABC"]  # No valid words
    assert solver.find_shortest_solution(sample_square) is None 