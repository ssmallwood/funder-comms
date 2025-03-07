"""Command-line interface for the Funder Communications Tool."""

import os
import json
import argparse
from app.models.funder import Funder
from app.models.impact_story import ImpactStory
from app.services.prompt_service import PromptService
from app.services.ai_service import AIService

def load_messaging():
    """Load organizational messaging from JSON file."""
    messaging_path = os.path.join("data", "messaging", "messaging.json")
    if os.path.exists(messaging_path):
        with open(messaging_path, 'r') as f:
            return json.load(f)
    return {}

def load_funder(funder_id):
    """Load a funder profile by ID."""
    funder_path = os.path.join("data", "funders", f"{funder_id}.json")
    if os.path.exists(funder_path):
        return Funder.from_json_file(funder_path)
    return None

def load_impact_stories():
    """Load all impact stories."""
    stories = []
    impacts_dir = os.path.join("data", "impacts")
    
    if not os.path.exists(impacts_dir):
        return stories
        
    for filename in os.listdir(impacts_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(impacts_dir, filename)
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Split content into individual stories if needed
            story_blocks = content.split("\n\n")
            for block in story_blocks:
                if block.strip():
                    story = ImpactStory.from_text_block(block)
                    stories.append(story)
    
    return stories

def main():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(description='Generate funder communications')
    parser.add_argument('funder_id', help='ID of the funder (filename without .json)')
    parser.add_argument(
        '--type', '-t', 
        choices=['update', 'report', 'proposal'], 
        default='update',
        help='Type of communication to generate'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (if not specified, prints to console)'
    )
    
    args = parser.parse_args()
    
    # Load data
    messaging = load_messaging()
    funder = load_funder(args.funder_id)
    
    if not funder:
        print(f"Error: Funder with ID '{args.funder_id}' not found")
        return
    
    all_stories = load_impact_stories()
    
    # Filter stories by relevance
    stories = sorted(
        all_stories, 
        key=lambda story: story.relevance_to_funder(funder),
        reverse=True
    )[:5]  # Get top 5 most relevant stories
    
    # Create prompt and generate content
    prompt_service = PromptService(messaging)
    prompt = prompt_service.create_funder_communication_prompt(
        funder, stories, args.type
    )
    
    ai_service = AIService()
    content = ai_service.generate_content(prompt, max_tokens=1500)
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(content)
        print(f"Content written to {args.output}")
    else:
        print("\n" + "=" * 40 + "\n")
        print(content)
        print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    main()
