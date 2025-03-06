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
    
    def get_puzzle_data(self) -> Tuple[List[str], List[str]]:
        """
        Fetch today's puzzle data from NYT Letter Boxed.
        
        Returns:
            Tuple[List[str], List[str]]: (sides, nyt_solution)
                - sides: List of strings representing letters on each side
                - nyt_solution: List of words in NYT's solution
        """
        driver = webdriver.Chrome(options=self.options)
        
        try:
            logger.info("Fetching puzzle data from NYT...")
            driver.get("https://www.nytimes.com/puzzles/letter-boxed")
            time.sleep(3)
            
            # Get both sides and solution
            sides = driver.execute_script("return window.gameData.sides;")
            solution = driver.execute_script("return window.gameData.ourSolution;")
            
            logger.info("Successfully fetched puzzle data")
            return sides, solution
            
        except Exception as e:
            logger.error(f"Error fetching puzzle data: {str(e)}")
            raise
            
        finally:
            driver.quit() 