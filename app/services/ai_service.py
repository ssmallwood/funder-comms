"""Service for interacting with the Anthropic API."""

import anthropic
from config.settings import ANTHROPIC_API_KEY, DEFAULT_MODEL

class AIService:
    """Service for generating content using the Anthropic API."""
    
    def __init__(self):
        """Initialize the Anthropic client."""
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.default_model = DEFAULT_MODEL
    
    def generate_content(self, prompt, max_tokens=1000, model=None):
        """Generate content using the Anthropic API."""
        if not model:
            model = self.default_model
            
        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error generating content: {str(e)}"
