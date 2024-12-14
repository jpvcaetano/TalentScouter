import base64
from pathlib import Path
import logging
from typing import List, Dict
import openai

logger = logging.getLogger(__name__)

class CVProcessor:
    def __init__(self, config: dict):
        self.config = config
        self.model = config['openai']['model']
        self.max_tokens = config['openai']['max_tokens']

    def pdf_to_base64(self, pdf_path: Path) -> str:
        """Convert PDF file to base64 string"""
        try:
            with open(pdf_path, 'rb') as file:
                return base64.b64encode(file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error converting PDF to base64: {e}")
            raise

    def process_cvs(self, cv_files: List[Path], criteria: str) -> List[Dict]:
        """Process all CVs and compare against criteria"""
        results = []
        for cv_file in cv_files:
            try:
                logger.info(f"Processing CV: {cv_file.name}")
                
                # Convert PDF to base64
                cv_content = self.pdf_to_base64(cv_file)
                
                # Process with GPT
                cv_analysis = self.analyze_cv(cv_content, criteria)
                cv_analysis['filename'] = cv_file.name
                results.append(cv_analysis)
                
            except Exception as e:
                logger.error(f"Error processing CV {cv_file}: {e}")
                continue
        
        return results

    def analyze_cv(self, cv_content: str, criteria: str) -> Dict:
        """Analyze a single CV using GPT-4"""
        try:
            # Create the analysis prompt
            prompt = self._create_analysis_prompt(criteria)
            
            # Call GPT-4 for analysis
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": cv_content}
                ],
                temperature=0.2
            )
            
            # Parse the response
            analysis = self._parse_gpt_response(response.choices[0].message.content)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in GPT analysis: {e}")
            raise

    def _create_analysis_prompt(self, criteria: str) -> str:
        """Create the prompt for GPT analysis"""
        return f"""You are an expert HR analyst. Analyze the provided CV against the following job criteria:

        {criteria}

        Provide your analysis in the following JSON format:
        {{
            "candidate_name": "Full name of the candidate",
            "summary": "A brief summary of the candidate's background",
            "key_skills": ["List of main skills"],
            "experience_years": "Total years of relevant experience",
            "education": "Highest relevant education",
            "criteria_match": {{
                "matching_points": ["List of criteria that the candidate matches"],
                "missing_points": ["List of criteria that the candidate lacks"]
            }},
            "strengths": ["List of candidate's main strengths"],
            "weaknesses": ["List of areas for improvement"]
        }}

        Ensure your response is valid JSON. Be objective and thorough in your analysis."""

    def _parse_gpt_response(self, response: str) -> Dict:
        """Parse and validate GPT response"""
        try:
            # Extract JSON from response (in case GPT added any extra text)
            import json
            import re
            
            # Find JSON pattern in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if not json_match:
                raise ValueError("No valid JSON found in response")
                
            analysis = json.loads(json_match.group())
            
            # Validate required fields
            required_fields = [
                'candidate_name', 'summary', 'key_skills', 
                'experience_years', 'education', 'criteria_match', 
                'strengths', 'weaknesses'
            ]
            
            for field in required_fields:
                if field not in analysis:
                    raise ValueError(f"Missing required field: {field}")
                    
            return analysis
            
        except Exception as e:
            logger.error(f"Error parsing GPT response: {e}")
            raise 