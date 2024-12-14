import os
from pathlib import Path
import pandas as pd
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self, config: dict):
        self.config = config
        self.cv_folder = Path(config['paths']['cv_folder'])
        self.criteria_file = Path(config['paths']['criteria_file'])
        self.output_folder = Path(config['paths']['output_folder'])
        
        # Create output folder if it doesn't exist
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def get_pdf_files(self) -> List[Path]:
        """Get all PDF files from the CV folder"""
        try:
            pdf_files = list(self.cv_folder.glob("*.pdf"))
            if not pdf_files:
                raise ValueError(f"No PDF files found in {self.cv_folder}")
            return pdf_files
        except Exception as e:
            logger.error(f"Error reading PDF files: {e}")
            raise

    def read_criteria_file(self) -> str:
        """Read and return the job criteria"""
        try:
            with open(self.criteria_file, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading criteria file: {e}")
            raise

    def save_initial_analysis(self, analysis: List[Dict]) -> Path:
        """Save initial CV analysis to CSV"""
        try:
            output_path = self.output_folder / "candidates_summary.csv"
            df = pd.DataFrame(analysis)
            df.to_csv(output_path, index=False)
            return output_path
        except Exception as e:
            logger.error(f"Error saving initial analysis: {e}")
            raise

    def save_final_analysis(self, ranked_candidates: List[Dict]) -> Path:
        """Save final ranked analysis to CSV"""
        try:
            output_path = self.output_folder / "ranked_candidates.csv"
            df = pd.DataFrame(ranked_candidates)
            df.to_csv(output_path, index=False)
            return output_path
        except Exception as e:
            logger.error(f"Error saving final analysis: {e}")
            raise 