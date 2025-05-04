"""
Midjourney-specific metadata extractor
"""

import re
from typing import Dict, Optional
from datetime import datetime
from PIL import Image

from src.app.api.core.models.base import AIImageMetadataExtractor, AIModelType
from src.app.api.core.metadata import AIImageMetadata, parse_description

class MidjourneyMetadataExtractor(AIImageMetadataExtractor):
    """Metadata extractor for Midjourney images"""
    
    @property
    def model_type(self) -> AIModelType:
        return AIModelType.MIDJOURNEY
    
    def is_compatible(self, image_info: Dict[str, str]) -> bool:
        """
        Check if this extractor is compatible with the given image
        
        Args:
            image_info: Dictionary of image metadata
            
        Returns:
            bool: True if image appears to be from Midjourney
        """
        description = image_info.get('Description', '').lower()
        
        # Check for model version indicators
        model_indicators = [
            '--v 1', '--v 2', '--v 3', '--v 4', '--v 5', '--v 6',  # Major versions
            '--niji',  # Niji model
            '--test', '--testp',  # Test models
            bool(re.search(r'--v\s*\d+\.\d+', description))  # Decimal versions like 5.2, 6.1
        ]
        
        # Check metadata indicators
        indicators = [
            # Standard indicators
            description.startswith('imagine'),
            'midjourney.com' in image_info.get('Copyright', '').lower(),
            bool(re.search(r'MJ_\w+', image_info.get('filename', ''))),
            'mdjrny' in image_info.get('Software', '').lower(),
            'midjourney' in ' '.join(image_info.values()).lower(),
            
            # Model version indicators
            any(indicator in description for indicator in model_indicators),
            
            # Additional Midjourney-specific indicators
            bool(re.search(r'job id:', description, re.IGNORECASE)),  # Job ID
            '--ar' in description,  # Aspect ratio parameter
            '--stylize' in description,  # Stylize parameter
            '--quality' in description,  # Quality parameter
            '--profile' in description,  # Profile parameter
            bool(re.search(r'--seed \d+', description)),  # Seed parameter
            '--chaos' in description,  # Chaos parameter
            '--stop' in description,  # Stop parameter
            '--style' in description,  # Style parameter
            '--no' in description,  # Negative prompt marker
            '--iw' in description  # Image weight parameter
        ]
        
        # Image is considered Midjourney if any indicators are true
        return any(indicators)
    
    def extract_metadata(self, image: Image.Image) -> Optional[AIImageMetadata]:
        """
        Extract Midjourney metadata from an image
        
        Args:
            image: PIL Image object
            
        Returns:
            Optional[AIImageMetadata]: Extracted metadata
        """
        metadata = AIImageMetadata()
        
        # Basic image properties
        metadata.width = image.width
        metadata.height = image.height
        
        # Extract text metadata
        image_metadata = {}
        
        # Try both tEXt and iTXt chunks
        for key, value in image.info.items():
            if isinstance(value, bytes):
                try:
                    value = value.decode('utf-8')
                except UnicodeDecodeError:
                    continue
            image_metadata[key] = str(value)
        
        # Parse metadata
        description = image_metadata.get('Description', '')
        if description:
            mj_data = parse_description(description)
            metadata.prompt = mj_data.get('prompt', '')
            metadata.version = mj_data.get('version', '')
            metadata.profile = mj_data.get('profile', '')
            metadata.job_id = mj_data.get('job_id', '')
        
        # Creation date
        if 'Creation Time' in image_metadata:
            try:
                metadata.created_date = datetime.strptime(
                    image_metadata['Creation Time'],
                    '%Y-%m-%d %H:%M:%S'
                )
            except ValueError:
                pass
        
        # Author
        metadata.author = image_metadata.get('Author', '')
        
        return metadata
