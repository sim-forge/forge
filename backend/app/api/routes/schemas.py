import os
import json
from fastapi import APIRouter, HTTPException
from ...core.schema.base import ResponseModel
from ...core.schema.cognition import SchemaResponse
from ...core.utils.logger import app_logger
from ...core.utils.config import settings

router = APIRouter()

@router.get("", response_model=ResponseModel)
async def get_schemas():
    """
    Get all available schemas.
    
    Returns:
        ResponseModel containing the schemas
    """
    try:
        app_logger.info("Schema request received")
        
        schemas_dir = settings.SCHEMAS_DIR
        schemas = []
        
        # Check if the schemas directory exists
        if not os.path.exists(schemas_dir):
            app_logger.warning(f"Schemas directory not found: {schemas_dir}")
            return ResponseModel(
                success=True,
                message="No schemas found",
                data=SchemaResponse(schemas=[])
            )
        
        # Load all JSON files in the schemas directory
        for filename in os.listdir(schemas_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(schemas_dir, filename), 'r') as f:
                        schema = json.load(f)
                        schemas.append(schema)
                except Exception as e:
                    app_logger.error(f"Error loading schema {filename}: {str(e)}")
        
        response = SchemaResponse(schemas=schemas)
        
        return ResponseModel(
            success=True,
            message=f"Found {len(schemas)} schemas",
            data=response
        )
    except Exception as e:
        app_logger.error(f"Error getting schemas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{schema_name}", response_model=ResponseModel)
async def get_schema(schema_name: str):
    """
    Get a specific schema by name.
    
    Args:
        schema_name: The name of the schema to get
        
    Returns:
        ResponseModel containing the schema
    """
    try:
        app_logger.info(f"Schema request received for {schema_name}")
        
        schemas_dir = settings.SCHEMAS_DIR
        schema_path = os.path.join(schemas_dir, f"{schema_name}.json")
        
        # Check if the schema file exists
        if not os.path.exists(schema_path):
            app_logger.warning(f"Schema not found: {schema_name}")
            raise HTTPException(status_code=404, detail=f"Schema not found: {schema_name}")
        
        # Load the schema
        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
        except Exception as e:
            app_logger.error(f"Error loading schema {schema_name}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error loading schema: {str(e)}")
        
        return ResponseModel(
            success=True,
            message=f"Schema {schema_name} found",
            data=schema
        )
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error getting schema {schema_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))