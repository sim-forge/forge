"""
Validator module for SimForge.
Handles validation of cognition sequences against schemas.
"""
import json
from typing import Dict, Any, List, Optional, Union, Tuple
from pydantic import ValidationError
from ...core.utils.logger import app_logger
from ...core.schema.cognition import CognitionSequence, CognitionRow

class Validator:
    """Validator class for validating cognition sequences against schemas."""
    
    def validate_sequence(self, sequence: CognitionSequence) -> bool:
        """
        Validate a cognition sequence against its schema.
        
        Args:
            sequence: The sequence to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Validate using Pydantic
            CognitionSequence.model_validate(sequence.model_dump())
            return True
        except ValidationError as e:
            app_logger.error(f"Validation error: {str(e)}")
            return False
    
    def validate_row(self, row: CognitionRow) -> bool:
        """
        Validate a cognition row against its schema.
        
        Args:
            row: The row to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Validate using Pydantic
            CognitionRow.model_validate(row.model_dump())
            return True
        except ValidationError as e:
            app_logger.error(f"Validation error: {str(e)}")
            return False
    
    def validate_json_against_schema(
        self, 
        data: Dict[str, Any], 
        schema: Dict[str, Any]
    ) -> Tuple[bool, Optional[List[str]]]:
        """
        Validate JSON data against a JSON schema.
        
        Args:
            data: The data to validate
            schema: The schema to validate against
            
        Returns:
            tuple: (is_valid, errors)
        """
        try:
            # For more complex schema validation, we could use jsonschema library
            # For now, we'll do a simple validation based on required fields
            required_fields = schema.get("required", [])
            errors = []
            
            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {field}")
            
            # Validate properties
            properties = schema.get("properties", {})
            for field, field_schema in properties.items():
                if field in data:
                    field_type = field_schema.get("type")
                    if field_type == "string" and not isinstance(data[field], str):
                        errors.append(f"Field {field} should be a string")
                    elif field_type == "number" and not isinstance(data[field], (int, float)):
                        errors.append(f"Field {field} should be a number")
                    elif field_type == "integer" and not isinstance(data[field], int):
                        errors.append(f"Field {field} should be an integer")
                    elif field_type == "array" and not isinstance(data[field], list):
                        errors.append(f"Field {field} should be an array")
                    elif field_type == "object" and not isinstance(data[field], dict):
                        errors.append(f"Field {field} should be an object")
            
            return len(errors) == 0, errors
        except Exception as e:
            app_logger.error(f"Schema validation error: {str(e)}")
            return False, [str(e)]
    
    def load_schema_from_file(self, schema_path: str) -> Optional[Dict[str, Any]]:
        """
        Load a JSON schema from a file.
        
        Args:
            schema_path: Path to the schema file
            
        Returns:
            Optional[Dict[str, Any]]: The schema, or None if loading failed
        """
        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            return schema
        except Exception as e:
            app_logger.error(f"Error loading schema from {schema_path}: {str(e)}")
            return None

# Create a singleton instance
validator = Validator()