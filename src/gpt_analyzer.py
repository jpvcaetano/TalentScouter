from pathlib import Path
import pandas as pd
import logging
from typing import List, Dict
import openai
import json

logger = logging.getLogger(__name__)

class GPTAnalyzer:
    def __init__(self, config: dict):
        self.config = config
        self.model = config['openai']['model']
        self.max_tokens = config['openai']['max_tokens']

    def rank_candidates(self, csv_path: Path, top_n: int) -> List[Dict]:
        """Analyze and rank candidates using GPT-4"""
        try:
            # Read the CSV file
            df = pd.read_csv(csv_path)
            
            # Convert DataFrame to string format for GPT
            candidates_data = df.to_json(orient='records', indent=2)
            
            # Get GPT analysis
            ranked_candidates = self._analyze_candidates(candidates_data, top_n)
            
            return ranked_candidates
            
        except Exception as e:
            logger.error(f"Error ranking candidates: {e}")
            raise

    def _analyze_candidates(self, candidates_data: str, top_n: int) -> List[Dict]:
        """Get GPT analysis for candidate ranking"""
        try:
            prompt = self._create_ranking_prompt(top_n)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": candidates_data}
                ],
                max_tokens=self.max_tokens,
                temperature=0.2
            )
            
            # Parse and validate the response
            ranked_candidates = self._parse_ranking_response(
                response.choices[0].message.content
            )
            
            return ranked_candidates
            
        except Exception as e:
            logger.error(f"Error in GPT ranking analysis: {e}")
            raise

    def _create_ranking_prompt(self, top_n: int) -> str:
        """Create the prompt for ranking analysis"""
        return f"""You are an expert HR analyst. Review the provided candidate data and select the top {top_n} candidates.

                For each candidate, provide a detailed analysis of why they are a good fit for the position.

                Provide your analysis in the following JSON format:
                {{
                    "top_candidates": [
                        {{
                            "rank": "Numerical rank (1 being the best)",
                            "candidate_name": "Name of the candidate",
                            "selection_reasoning": [
                                "List of specific reasons why this candidate was selected"
                            ],
                            "strengths": [
                                "Key strengths that make them suitable"
                            ],
                            "potential_concerns": [
                                "Any potential areas of concern"
                            ],
                            "recommendation": "A brief recommendation for the hiring manager"
                        }}
                    ],
                    "analysis_summary": "Overall summary of the selection process and recommendations"
                }}

                Ensure your response is valid JSON. Be objective and data-driven in your analysis."""

    def _parse_ranking_response(self, response: str) -> List[Dict]:
        """Parse and validate the ranking response"""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if not json_match:
                raise ValueError("No valid JSON found in response")
                
            analysis = json.loads(json_match.group())
            
            # Validate the response structure
            if 'top_candidates' not in analysis:
                raise ValueError("Missing 'top_candidates' in response")
                
            # Sort candidates by rank
            candidates = analysis['top_candidates']
            candidates.sort(key=lambda x: int(x['rank']))
            
            return candidates
            
        except Exception as e:
            logger.error(f"Error parsing ranking response: {e}")
            raise