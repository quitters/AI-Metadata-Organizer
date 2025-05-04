"""
Metadata handling for AI-generated images
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union
from PIL import Image
import re

@dataclass
class AIImageMetadata:
    """Metadata for an AI-generated image"""
    prompt: str = ""
    width: int = 0
    height: int = 0
    version: str = ""
    profile: str = ""
    job_id: str = ""
    created_date: datetime = datetime.now()
    author: str = ""
    # Added to track the source AI model
    source_model: str = "unknown"

def extract_metadata(image: Image.Image) -> Optional[AIImageMetadata]:
    """
    Extract metadata from an AI-generated image
    
    Args:
        image: PIL Image object
    
    Returns:
        Optional[AIImageMetadata]: Extracted metadata or None if not supported
    """
    # Import here to avoid circular imports
    from src.app.api.core.models import MetadataExtractorFactory
    
    # Extract text metadata
    image_metadata = {}
    
    # Try both tEXt and iTXt chunks
    print("Extracting image metadata chunks:")
    for key, value in image.info.items():
        if isinstance(value, bytes):
            try:
                value = value.decode('utf-8')
                print(f"  Decoded {key}: {value[:100]}...")  # First 100 chars
            except UnicodeDecodeError:
                print(f"  Failed to decode {key}")
                continue
        else:
            print(f"  Found {key}: {str(value)[:100]}...")  # First 100 chars
        image_metadata[key] = str(value)
    
    # Create appropriate extractor
    extractor = MetadataExtractorFactory.create_extractor(image_metadata)
    if extractor:
        print(f"Using extractor for {extractor.model_type.name}")
        metadata = extractor.extract_metadata(image)
        if metadata:
            # Set source model
            metadata.source_model = extractor.model_type.name
            return metadata
    
    print("No compatible metadata extractor found")
    return None

def parse_description(description: str) -> Dict[str, str]:
    """
    Parse Midjourney description text into components
    
    Args:
        description: Raw description text from image metadata
    
    Returns:
        Dict[str, str]: Parsed metadata components
    """
    metadata = {}
    
    # Extract prompt (everything before the first --)
    prompt_match = re.match(r'(.*?)(?=\s+--)', description)
    if prompt_match:
        metadata['prompt'] = prompt_match.group(1).strip()
    
    # Extract aspect ratio
    ar_match = re.search(r'--ar\s+(\d+:\d+)', description)
    if ar_match:
        metadata['aspect_ratio'] = ar_match.group(1)
    
    # Extract profile
    profile_match = re.search(r'--profile\s+(\w+)', description)
    if profile_match:
        metadata['profile'] = profile_match.group(1)
    
    # Extract stylize value
    stylize_match = re.search(r'--stylize\s+(\d+)', description)
    if stylize_match:
        metadata['stylize'] = stylize_match.group(1)
    
    # Extract version
    version_match = re.search(r'--v\s+([\d.]+)', description)
    if version_match:
        metadata['version'] = version_match.group(1)
    
    # Extract Job ID
    job_id_match = re.search(r'Job ID:\s*([a-f0-9-]+)', description)
    if job_id_match:
        metadata['job_id'] = job_id_match.group(1)
    
    return metadata

def extract_clean_prompts(description: str, ai_model: str = "MIDJOURNEY") -> List[str]:
    """
    Extract clean prompts from a prompt string, with model-specific handling
    
    Args:
        description: Raw prompt string
        ai_model: AI model that generated the image (MIDJOURNEY, EMPROPS, etc.)
    
    Returns:
        List[str]: List of clean prompts
    """
    # For EmProps/Stable Diffusion, handle differently
    if ai_model in ("EMPROPS", "STABLE_DIFFUSION"):
        # SD prompts are generally simpler, just split by commas
        parts = description.split(',')
        return [part.strip() for part in parts if part.strip()]
    
    # Default Midjourney handling
    # First get everything before any -- parameters
    full_prompt = re.match(r'(.*?)(?=\s+--)', description)
    if not full_prompt:
        return []
    
    full_prompt = full_prompt.group(1).strip()
    
    # Split the prompt into parts, keeping both prompts and their weights
    parts = re.split(r'(::[\s-]*[\d.]+\s*)', full_prompt)
    
    prompts = []
    for i in range(0, len(parts)-1, 2):
        prompt = parts[i].strip()
        if i+1 < len(parts):
            weight = parts[i+1]
            # Check if this is a negative weight
            if not re.search(r'::\s*-', weight) and prompt:
                prompts.append(prompt)
    
    # Handle the last prompt if it doesn't have a weight
    if len(parts) % 2 == 1 and parts[-1].strip():
        prompts.append(parts[-1].strip())
    
    return prompts
