"""Impact story model."""

import re
from datetime import datetime

class ImpactStory:
    """Represents an impact story."""

    def __init__(self, data):
        """Initialize an impact story from a dictionary."""
        self.id = data.get("story_id")
        self.headline = data.get("headline", "")
        self.description = data.get("description", "")
        self.date = data.get("date")
        self.location = data.get("location", "")
        self.reporter = data.get("reporter", "")
        self.newsroom_partner = data.get("newsroom_partner", "")
        self.impact_type = data.get("impact_type", "")
        self.tags = data.get("tags", [])
    
    @classmethod
    def from_text_block(cls, text_block):
        """Parse an impact story from a text block."""
        lines = text_block.strip().split('\n')
        data = {}
        
        for line in lines:
            if not line.strip():
                continue
                
            match = re.match(r'^([A-Z_]+):\s*(.+)$', line)
            if match:
                key, value = match.groups()
                key = key.lower()
                
                if key == 'tags':
                    data[key] = [tag.strip() for tag in value.split(',')]
                elif key == 'date':
                    try:
                        # Try to parse the date
                        data[key] = datetime.strptime(value, '%Y-%m-%d').strftime('%Y-%m-%d')
                    except ValueError:
                        data[key] = value
                else:
                    data[key] = value
        
        # Map fields to our expected schema
        if 'title' in data and 'headline' not in data:
            data['headline'] = data['title']
            
        return cls(data)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "story_id": self.id,
            "headline": self.headline,
            "description": self.description,
            "date": self.date,
            "location": self.location,
            "reporter": self.reporter,
            "newsroom_partner": self.newsroom_partner,
            "impact_type": self.impact_type,
            "tags": self.tags
        }
    
    def relevance_to_funder(self, funder):
        """Calculate relevance score to a funder."""
        score = 0
        
        # Check geographic match
        if any(geo.lower() in self.location.lower() for geo in funder.geographic_interests):
            score += 3
            
        # Check tag match with focus areas
        for tag in self.tags:
            if any(focus.lower() in tag.lower() for focus in funder.focus_areas):
                score += 2
                
        # Basic recency score
        try:
            story_date = datetime.strptime(self.date, '%Y-%m-%d')
            days_old = (datetime.now() - story_date).days
            recency_score = max(0, 5 - (days_old // 30))  # 5 points for newest, decreasing by month
            score += recency_score
        except (ValueError, TypeError):
            pass
            
        return score
