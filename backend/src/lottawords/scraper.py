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
                print("ERROR: window.gameData not found. The NYT page structure may have changed.")
                print("HTML Source:")
                print(driver.page_source[:500] + "...")  # Print first 500 chars of the page
                return [], [], []
            
            # Check what properties exist in gameData
            game_data_keys = driver.execute_script("""
                return Object.keys(window.gameData);
            """)
            print(f"gameData keys: {game_data_keys}")
            
            # Get sides, solution, and dictionary
            print("Fetching sides...")
            sides = driver.execute_script("return window.gameData.sides;")
            print(f"Sides type: {type(sides)}")
            
            print("Fetching solution...")
            solution = driver.execute_script("return window.gameData.ourSolution;")
            print(f"Solution type: {type(solution)}")
            
            print("Fetching dictionary...")
            # First check if dictionary property exists
            has_dictionary = driver.execute_script("return 'dictionary' in window.gameData;")
            if not has_dictionary:
                print("WARNING: 'dictionary' property not found in window.gameData")
                print("Available properties:", game_data_keys)
                
                # Try to find another property that might contain the dictionary
                # Check if 'validWords' exists
                has_valid_words = driver.execute_script("return 'validWords' in window.gameData;")
                if has_valid_words:
                    print("Using 'validWords' instead of 'dictionary'")
                    dictionary = driver.execute_script("return window.gameData.validWords;")
                else:
                    print("No dictionary-like property found. Checking all properties...")
                    # Try other potential properties
                    for key in game_data_keys:
                        value_type = driver.execute_script(f"return typeof window.gameData.{key};")
                        print(f"Property {key} has type: {value_type}")
                        if value_type == 'object':
                            value_length = driver.execute_script(f"return window.gameData.{key}.length;")
                            if value_length and value_length > 100:  # Likely a dictionary
                                print(f"Using {key} as potential dictionary (has {value_length} items)")
                                dictionary = driver.execute_script(f"return window.gameData.{key};")
                                break
                    else:
                        print("No suitable dictionary found")
                        dictionary = []
            else:
                dictionary = driver.execute_script("return window.gameData.dictionary;")
            
            # Check dictionary type and structure
            print(f"Dictionary type: {type(dictionary)}")
            
            # Ensure dictionary is a list of strings
            if isinstance(dictionary, list):
                if len(dictionary) > 0:
                    first_item_type = type(dictionary[0])
                    print(f"First dictionary item type: {first_item_type}")
                    print(f"First 5 dictionary items: {dictionary[:5]}")
                    
                    # If not strings, convert
                    if first_item_type is not str:
                        print(f"Converting dictionary items from {first_item_type} to str")
                        dictionary = [str(word) for word in dictionary]
            else:
                print(f"WARNING: Dictionary is not a list, it's a {type(dictionary)}")
                dictionary = []
            
            print("Raw sides from NYT:", sides)  # Debug print
            print("Raw solution from NYT:", solution)  # Debug print
            print(f"Dictionary from NYT: {len(dictionary) if dictionary else 0} words")
            
            if dictionary and len(dictionary) > 0:
                print(f"Sample words: {dictionary[:5]}")
            else:
                print("WARNING: Empty dictionary received from NYT")
            
            logger.info("Successfully fetched puzzle data")
            return sides, solution, dictionary
            
        except Exception as e:
            logger.error(f"Error fetching puzzle data: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise
            
        finally:
            driver.quit() 