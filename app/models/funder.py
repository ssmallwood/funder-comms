"""Funder profile model."""

class Funder:
    """Represents a funding organization."""

    def __init__(self, data):
        """Initialize a funder from a dictionary."""
        self.id = data.get("funder_id")
        self.name = data.get("name")
        self.description = data.get("description", "")
        self.focus_areas = data.get("focus_areas", [])
        self.geographic_interests = data.get("geographic_interests", [])
        self.theory_of_change = data.get("theory_of_change", "")
        self.communication_preferences = data.get("communication_preferences", {})
        self.past_grants = data.get("past_grants", [])
        self.key_contacts = data.get("key_contacts", [])
    
    @classmethod
    def from_json_file(cls, file_path):
        """Load a funder from a JSON file."""
        import json
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls(data)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "funder_id": self.id,
            "name": self.name,
            "description": self.description,
            "focus_areas": self.focus_areas,
            "geographic_interests": self.geographic_interests,
            "theory_of_change": self.theory_of_change,
            "communication_preferences": self.communication_preferences,
            "past_grants": self.past_grants,
            "key_contacts": self.key_contacts
        }
