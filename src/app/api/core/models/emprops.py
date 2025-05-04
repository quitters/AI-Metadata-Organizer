"""
EmProps Stable Diffusion metadata extractor
"""

import json
from typing import Dict, Optional, Any
from datetime import datetime
from PIL import Image

from src.app.api.core.models.base import AIImageMetadataExtractor, AIModelType
from src.app.api.core.metadata import AIImageMetadata

class EmPropsMetadataExtractor(AIImageMetadataExtractor):
    """Metadata extractor for StableDiffusion images generated with ComfyUI via EmProps"""
    
    @property
    def model_type(self) -> AIModelType:
        return AIModelType.EMPROPS
    
    def is_compatible(self, image_info: Dict[str, str]) -> bool:
        """
        Check if this extractor is compatible with the image
        
        Args:
            image_info: Dictionary of image metadata
            
        Returns:
            bool: True if image appears to be from EmProps
        """
        if 'prompt' not in image_info:
            return False
            
        # Check for EmProps specific format in the JSON
        try:
            data = json.loads(image_info['prompt'])
            # Look for EmProps_S3_Saver which is specific to EmProps
            return any(
                isinstance(node, dict) and 
                node.get('class_type') == 'EmProps_S3_Saver'
                for node in data.values() if isinstance(node, dict)
            )
        except (json.JSONDecodeError, TypeError):
            return False
    
    def extract_metadata(self, image: Image.Image) -> Optional[AIImageMetadata]:
        """
        Extract metadata from an EmProps SD image
        
        Args:
            image: PIL Image object
            
        Returns:
            Optional[AIImageMetadata]: Extracted metadata
        """
        metadata = AIImageMetadata()
        
        # Basic image properties
        metadata.width = image.width
        metadata.height = image.height
        
        # Extract JSON data
        prompt_data = image.info.get('prompt', '')
        if not prompt_data:
            return None
            
        try:
            json_data = json.loads(prompt_data)
            
            # Extract prompt from CLIPTextEncode nodes
            text_encode_nodes = [
                node for node in json_data.values() 
                if isinstance(node, dict) and 
                node.get('class_type') == 'CLIPTextEncode' and
                'inputs' in node and
                'text' in node.get('inputs', {})
            ]
            
            # Find positive prompt (usually labeled as "CLIP Text Encode (Prompt)")
            positive_nodes = [
                node for node in text_encode_nodes
                if (node.get('_meta', {}).get('title', '').endswith('(Prompt)') or
                   '(negative)' not in node.get('_meta', {}).get('title', '').lower()) and
                node['inputs']['text'].strip() != ''
            ]
            
            if positive_nodes:
                metadata.prompt = positive_nodes[0]['inputs']['text']
            elif text_encode_nodes:
                # Fallback to any non-empty text node
                non_empty_nodes = [
                    node for node in text_encode_nodes
                    if node['inputs']['text'].strip() != ''
                ]
                if non_empty_nodes:
                    metadata.prompt = non_empty_nodes[0]['inputs']['text']
            
            # Extract model information
            checkpoint_nodes = [
                node for node in json_data.values() 
                if isinstance(node, dict) and
                node.get('class_type') in ('CheckpointLoaderSimple', 'UNETLoader') and
                'inputs' in node
            ]
            
            if checkpoint_nodes:
                # Get model name from first checkpoint loader
                model_node = checkpoint_nodes[0]['inputs']
                model_name = model_node.get('ckpt_name', model_node.get('unet_name', ''))
                if model_name:
                    metadata.profile = model_name.replace('.safetensors', '')
            
            # Extract sampler and version information
            sampler_nodes = [
                node for node in json_data.values() 
                if isinstance(node, dict) and
                node.get('class_type') in ('KSampler', 'SamplerCustomAdvanced') and
                'inputs' in node
            ]
            
            if sampler_nodes:
                sampler_node = sampler_nodes[0]['inputs']
                sampler_name = sampler_node.get('sampler_name', '')
                steps = sampler_node.get('steps', '')
                metadata.version = f"SD_{sampler_name}_{steps}steps"
            
            # For SamplerCustomAdvanced, need to follow references
            elif 'sampler' in sampler_node and isinstance(sampler_node['sampler'], list):
                sampler_ref = sampler_node['sampler'][0]
                if sampler_ref in json_data and 'inputs' in json_data[sampler_ref]:
                    sampler_name = json_data[sampler_ref]['inputs'].get('sampler_name', '')
                    metadata.version = f"SD_{sampler_name}"
            
            # Set creation date to now if not already set
            if not metadata.created_date:
                metadata.created_date = datetime.now()
            
            # Set author if available
            metadata.author = "EmProps"
                
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            # Log the error but return partial metadata if available
            print(f"Error parsing EmProps metadata: {str(e)}")
            if not metadata.prompt:
                return None
            
        return metadata
