import os
import logging
from pathlib import Path
import yaml
from dotenv import load_dotenv

from file_handler import FileHandler
from cv_processor import CVProcessor
from gpt_analyzer import GPTAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TalentScouter:
    def __init__(self, config_path: str = "../config/config.yaml"):
        self.load_config(config_path)
        self.file_handler = FileHandler(self.config)
        self.cv_processor = CVProcessor(self.config)
        self.gpt_analyzer = GPTAnalyzer(self.config)

    def load_config(self, config_path: str):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            # Override API key from environment variable
            self.config['openai']['api_key'] = os.getenv('OPENAI_API_KEY')
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise

    def run(self):
        """Main execution flow"""
        try:
            # Step 1: Validate and read CV files
            cv_files = self.file_handler.get_pdf_files()
            criteria = self.file_handler.read_criteria_file()

            # Step 2: Process CVs
            cv_analysis = self.cv_processor.process_cvs(cv_files, criteria)

            # Step 3: Save initial analysis
            initial_csv = self.file_handler.save_initial_analysis(cv_analysis)

            # Step 4: Rank candidates
            ranked_candidates = self.gpt_analyzer.rank_candidates(
                initial_csv, 
                self.config['processing']['top_candidates']
            )

            # Step 5: Save final analysis
            self.file_handler.save_final_analysis(ranked_candidates)

        except Exception as e:
            logger.error(f"Error in TalentScouter execution: {e}")
            raise

def main():
    load_dotenv()  # Load environment variables
    scout = TalentScouter()
    scout.run()

if __name__ == "__main__":
    main() 