"""
Base classes for AI image model abstraction
"""

from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from PIL import Image

from src.app.api.core.metadata import AIImageMetadata

class AIModelType(Enum):
    """Types of AI image generation models"""
    UNKNOWN = 0
    MIDJOURNEY = 1
    STABLE_DIFFUSION = 2
    EMPROPS = 3  # Specific type for EmProps Stable Diffusion

class AIImageMetadataExtractor(ABC):
    """Base class for AI image metadata extractors"""
    
    @property
    def model_type(self) -> AIModelType:
        """Get the model type for this extractor"""
        return AIModelType.UNKNOWN
    
    @abstractmethod
    def is_compatible(self, image_info: Dict[str, str]) -> bool:
        """
        Check if this extractor is compatible with the given image
        
        Args:
            image_info: Dictionary of image metadata
            
        Returns:
            bool: True if this extractor can handle the image
        """
        pass
        
    @abstractmethod
    def extract_metadata(self, image: Image.Image) -> Optional[AIImageMetadata]:
        """
        Extract metadata from an image
        
        Args:
            image: PIL Image object
            
        Returns:
            Optional[AIImageMetadata]: Extracted metadata or None if not compatible
        """
        pass

class MetadataExtractorFactory:
    """Factory for creating appropriate metadata extractors"""
    
    @staticmethod
    def create_extractor(image_info: Dict[str, str]) -> Optional[AIImageMetadataExtractor]:
        """
        Create an appropriate metadata extractor for the given image
        
        Args:
            image_info: Dictionary of image metadata
            
        Returns:
            Optional[AIImageMetadataExtractor]: An extractor instance or None if no compatible extractor
        """
        from .midjourney import MidjourneyMetadataExtractor
        from .emprops import EmPropsMetadataExtractor
        
        extractors = [
            EmPropsMetadataExtractor(),  # Try EmProps first (more specific)
            MidjourneyMetadataExtractor(),  # Then try Midjourney
            # Add more extractors as needed
        ]
        
        for extractor in extractors:
            if extractor.is_compatible(image_info):
                return extractor
                
        return None
