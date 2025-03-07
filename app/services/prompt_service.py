"""Service for constructing AI prompts."""

class PromptService:
    """Service for creating prompts for the AI model."""
    
    def __init__(self, messaging_data):
        """Initialize with organizational messaging data."""
        self.messaging = messaging_data
        
    def create_funder_communication_prompt(self, funder, impact_stories, comm_type="update"):
        """Create a prompt for generating funder communication."""
        
        # Organization context
        org_context = f"""
You are assisting Open Campus, a nonprofit newsroom focused on higher education journalism, in drafting communications to funders.

Context about Open Campus:
Mission: {self.messaging.get('mission', '')}
Value Proposition: {self.messaging.get('value_proposition', '')}
Problem We Address: {self.messaging.get('problem', '')}
Our Solution: {self.messaging.get('solution', '')}
Theory of Change: {self.messaging.get('theory_of_change', '')}
        """
        
        # Funder information
        funder_info = f"""
Information about the funder:
Name: {funder.name}
Focus Areas: {', '.join(funder.focus_areas)}
Geographic Interests: {', '.join(funder.geographic_interests)}
Theory of Change: {funder.theory_of_change}
Communication Preferences: 
  Style: {funder.communication_preferences.get('style', '')}
  Format: {funder.communication_preferences.get('format', '')}
  Focus Level: {funder.communication_preferences.get('focus_level', '')}
        """
        
        # Impact stories section
        impact_highlights = "Recent impact highlights:\n"
        for story in impact_stories:
            impact_highlights += f"""
- {story.headline} ({story.date}, {story.location})
  {story.description}
            """
        
        # Current relationship
        relationship = "Current relationship:\n"
        if funder.past_grants:
            for grant in funder.past_grants:
                relationship += f"- {grant.get('date')}: ${grant.get('amount')} for {grant.get('purpose')}\n"
        else:
            relationship += "No previous grants. This would be a new funding relationship.\n"
        
        # Communication type instructions
        comm_instructions = {
            "update": """
Draft an update email to this funder that:
1. Provides a brief, engaging summary of recent impact
2. Connects our work directly to their priorities
3. Sets up potential next steps for engagement
4. Maintains appropriate tone for the relationship

The communication should be approximately 2-3 paragraphs and feel personal, not generic.
            """,
            "report": """
Draft a grant report summary for this funder that:
1. Clearly outlines the key accomplishments during the grant period
2. Quantifies impact where possible
3. Addresses any challenges and how they were overcome
4. Connects outcomes to the funder's strategic goals
5. Sets up the case for continued support

The summary should be approximately 500-750 words and include section headings.
            """,
            "proposal": """
Draft a grant proposal summary for this funder that:
1. Clearly articulates the alignment between our mission and their priorities
2. Presents a compelling case using recent impact stories
3. Outlines specifically what funding would enable
4. Demonstrates our understanding of their approach and theory of change
5. Includes a clear, specific ask with defined outcomes

The summary should be approximately 750-1000 words with a professional but engaging tone.
            """
        }
        
        task = comm_instructions.get(comm_type, comm_instructions["update"])
        
        # Complete prompt
        prompt = f"{org_context}\n\n{funder_info}\n\n{impact_highlights}\n\n{relationship}\n\nTask:\n{task}"
        
        return prompt
