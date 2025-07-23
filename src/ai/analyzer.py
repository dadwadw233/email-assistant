"""
AI analyzer for the Personal Email Management Assistant
Handles LLM API integrations and email analysis
"""

from typing import Dict, List, Optional
import logging
import openai
import os
import httpx

class EmailAnalyzer:
    """Analyzes emails using LLM APIs to determine importance and generate summaries"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.openai_client = None
        self.model = "qwen-plus"  # Default to Qwen Plus
        
        # Try to load Qwen configuration from environment
        api_key = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('OPENAI_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        
        # If we have API key, initialize the client
        if api_key:
            # Handle proxy configuration
            http_client = None
            proxy_url = os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')
            if proxy_url and proxy_url.startswith('socks'):
                # SOCKS proxy is not directly supported by httpx, so we skip it
                self.logger.warning(f"SOCKS proxy {proxy_url} is not supported, ignoring proxy configuration")
                proxy_url = None
            
            if proxy_url:
                try:
                    http_client = httpx.Client(proxy=proxy_url)
                except Exception as e:
                    self.logger.warning(f"Failed to configure proxy {proxy_url}: {str(e)}")
            
            self.openai_client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url,
                http_client=http_client
            )
            
            # Use the model specified in environment or default to qwen-plus
            self.model = os.getenv('OPENAI_MODEL', 'qwen-plus')
            self.logger.info(f"Initialized Qwen analyzer with model: {self.model}")
    
    def analyze_email(self, email_data: Dict) -> Dict:
        """
        Analyze an email to determine its importance and generate a summary
        
        Args:
            email_data: Dictionary containing email information
            
        Returns:
            Dictionary with analysis results including:
            - importance: float between 0 and 1
            - summary: brief summary of the email
            - category: email category (e.g., work, personal, spam)
            - action: recommended action (e.g., read, archive, delete)
        """
        # If no LLM API key is available, return default analysis
        if not self.openai_client:
            return self._default_analysis(email_data)
        
        # Prepare prompt for LLM
        prompt = self._create_analysis_prompt(email_data)
        
        try:
            # Call Qwen API
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an email analysis assistant. Analyze emails and provide their importance, summary, category, and recommended action."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            # Parse response
            analysis_text = response.choices[0].message.content.strip()
            return self._parse_analysis_response(analysis_text)
            
        except openai.APIError as e:
            self.logger.error(f"OpenAI API error analyzing email: {str(e)}")
            return self._default_analysis(email_data)
        except Exception as e:
            self.logger.error(f"Error analyzing email with Qwen: {str(e)}")
            return self._default_analysis(email_data)
    
    def _create_analysis_prompt(self, email_data: Dict) -> str:
        """Create a prompt for the LLM to analyze an email"""
        prompt = f"""
        Analyze the following email and provide:
        1. Importance (0-1 scale, where 1 is very important)
        2. Brief summary (2-3 sentences)
        3. Category (work, personal, newsletter, spam, other)
        4. Recommended action (read, archive, delete)

        Email details:
        From: {email_data.get('from', 'Unknown')}
        Subject: {email_data.get('subject', 'No subject')}
        Body: {email_data.get('body', 'No body')[:1000]}  # Limit body length

        Format your response as JSON:
        {{
          "importance": 0.8,
          "summary": "Brief summary of the email",
          "category": "work",
          "action": "read"
        }}
        """
        return prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict:
        """Parse the LLM response and extract analysis results"""
        import json
        
        try:
            # Try to parse as JSON
            analysis = json.loads(response_text)
            return analysis
        except json.JSONDecodeError:
            # If JSON parsing fails, extract information manually
            self.logger.warning("Failed to parse LLM response as JSON, using fallback parsing")
            return self._extract_analysis_manually(response_text)
    
    def _extract_analysis_manually(self, response_text: str) -> Dict:
        """Extract analysis information manually from LLM response"""
        # This is a simplified implementation
        # In a real application, you'd want more robust parsing
        
        # Default values
        analysis = {
            "importance": 0.5,
            "summary": "Unable to generate summary",
            "category": "other",
            "action": "read"
        }
        
        # Simple keyword-based extraction
        if "importance" in response_text.lower():
            # Try to extract importance value
            import re
            imp_match = re.search(r"importance.*?([0-9]*\.?[0-9]+)", response_text, re.IGNORECASE)
            if imp_match:
                try:
                    analysis["importance"] = float(imp_match.group(1))
                except ValueError:
                    pass
        
        return analysis
    
    def _default_analysis(self, email_data: Dict) -> Dict:
        """Provide a default analysis when LLM is not available"""
        self.logger.info("Using default email analysis (no LLM API key)")
        
        # Simple heuristic-based analysis
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        sender = email_data.get('from', '').lower()
        
        # Determine category based on keywords
        category = "other"
        if any(word in subject for word in ['meeting', 'urgent', 'asap', 'deadline', 'project', 'task']):
            category = "work"
        elif any(word in subject for word in ['offer', 'deal', 'discount', 'sale', 'newsletter']):
            category = "newsletter"
        elif any(word in body for word in ['unsubscribe', 'opt out']) or 'noreply' in sender:
            category = "spam"
        elif any(word in subject for word in ['personal', 'friend', 'family']):
            category = "personal"
        
        # Determine action based on category
        action = "read"
        if category == "spam":
            action = "delete"
        elif category == "newsletter":
            action = "archive"
        
        # Determine importance based on category and keywords
        importance = 0.5
        if category == "work":
            importance = 0.8
        elif category == "spam":
            importance = 0.1
        elif category == "newsletter":
            importance = 0.3
        elif category == "personal":
            importance = 0.7
            
        # Adjust importance based on sender
        if any(domain in sender for domain in ['boss@', 'manager@', 'supervisor@']):
            importance = min(1.0, importance + 0.2)
            
        # Generate a simple summary
        summary = f"Email from {email_data.get('from', 'Unknown sender')}"
        if subject:
            summary += f" with subject: {subject[:50]}{'...' if len(subject) > 50 else ''}"
        
        return {
            "importance": importance,
            "summary": summary,
            "category": category,
            "action": action
        }