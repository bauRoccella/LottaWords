"""
Web scraper module for NYT Letter Boxed puzzle.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)

class LetterBoxedScraper:
    """Scraper for NYT Letter Boxed puzzle."""
    
    def __init__(self):
        """Initialize scraper with Chrome options."""
        # Suppress webdriver messages
        os.environ['WDM_LOG_LEVEL'] = '0'
        
        self.options = Options()
        self.options.add_argument('--headless=new')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--log-level=3')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    def get_puzzle_data(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Fetch today's puzzle data from NYT Letter Boxed.
        
        Returns:
            Tuple[List[str], List[str], List[str]]: (sides, nyt_solution, nyt_dictionary)
                - sides: List of strings representing letters on each side
                - nyt_solution: List of words in NYT's solution
                - nyt_dictionary: List of valid words according to NYT
        """
        driver = webdriver.Chrome(options=self.options)
        
        try:
            logger.info("Fetching puzzle data from NYT...")
            driver.get("https://www.nytimes.com/puzzles/letter-boxed")
            time.sleep(3)
            
            # Verify gameData exists
            has_game_data = driver.execute_script("return window.gameData !== undefined")
            if not has_game_data:
                logger.error("window.gameData not found. The NYT page structure may have changed.")
                return [], [], []
            
            # Get sides, solution, and dictionary
            sides = driver.execute_script("return window.gameData.sides;")
            solution = driver.execute_script("return window.gameData.ourSolution;")
            
            # First check if dictionary property exists
            has_dictionary = driver.execute_script("return 'dictionary' in window.gameData;")
            if not has_dictionary:
                # Try to find another property that might contain the dictionary
                # Check if 'validWords' exists
                has_valid_words = driver.execute_script("return 'validWords' in window.gameData;")
                if has_valid_words:
                    dictionary = driver.execute_script("return window.gameData.validWords;")
                else:
                    # Try other potential properties
                    game_data_keys = driver.execute_script("return Object.keys(window.gameData);")
                    for key in game_data_keys:
                        value_type = driver.execute_script(f"return typeof window.gameData.{key};")
                        if value_type == 'object':
                            value_length = driver.execute_script(f"return window.gameData.{key}.length;")
                            if value_length and value_length > 100:  # Likely a dictionary
                                dictionary = driver.execute_script(f"return window.gameData.{key};")
                                break
                    else:
                        dictionary = []
            else:
                dictionary = driver.execute_script("return window.gameData.dictionary;")
            
            # Ensure dictionary is a list of strings
            if isinstance(dictionary, list):
                if len(dictionary) > 0:
                    first_item_type = type(dictionary[0])
                    # If not strings, convert
                    if first_item_type is not str:
                        dictionary = [str(word) for word in dictionary]
            else:
                dictionary = []
            
            logger.info(f"Successfully fetched puzzle data with {len(dictionary)} words")
            return sides, solution, dictionary
            
        except Exception as e:
            logger.error(f"Error fetching puzzle data: {str(e)}")
            raise
            
        finally:
            driver.quit() 