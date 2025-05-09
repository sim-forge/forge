import os
from fastapi import APIRouter, HTTPException
from ...core.schema.base import ResponseModel
from ...core.schema.cognition import PromptResponse
from ...core.utils.logger import app_logger
from ...core.utils.config import settings

router = APIRouter()

@router.get("", response_model=ResponseModel)
async def get_prompts():
    """
    Get all available prompts.
    
    Returns:
        ResponseModel containing the prompts
    """
    try:
        app_logger.info("Prompt request received")
        
        prompts_dir = settings.PROMPTS_DIR
        prompts = []
        
        # Check if the prompts directory exists
        if not os.path.exists(prompts_dir):
            app_logger.warning(f"Prompts directory not found: {prompts_dir}")
            return ResponseModel(
                success=True,
                message="No prompts found",
                data=PromptResponse(prompts=[])
            )
        
        # Load all text files in the prompts directory
        for filename in os.listdir(prompts_dir):
            if filename.endswith(".txt"):
                try:
                    with open(os.path.join(prompts_dir, filename), 'r') as f:
                        content = f.read()
                        name = os.path.splitext(filename)[0]
                        prompts.append({
                            "name": name,
                            "content": content
                        })
                except Exception as e:
                    app_logger.error(f"Error loading prompt {filename}: {str(e)}")
        
        response = PromptResponse(prompts=prompts)
        
        return ResponseModel(
            success=True,
            message=f"Found {len(prompts)} prompts",
            data=response
        )
    except Exception as e:
        app_logger.error(f"Error getting prompts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{prompt_name}", response_model=ResponseModel)
async def get_prompt(prompt_name: str):
    """
    Get a specific prompt by name.
    
    Args:
        prompt_name: The name of the prompt to get
        
    Returns:
        ResponseModel containing the prompt
    """
    try:
        app_logger.info(f"Prompt request received for {prompt_name}")
        
        prompts_dir = settings.PROMPTS_DIR
        prompt_path = os.path.join(prompts_dir, f"{prompt_name}.txt")
        
        # Check if the prompt file exists
        if not os.path.exists(prompt_path):
            app_logger.warning(f"Prompt not found: {prompt_name}")
            raise HTTPException(status_code=404, detail=f"Prompt not found: {prompt_name}")
        
        # Load the prompt
        try:
            with open(prompt_path, 'r') as f:
                content = f.read()
        except Exception as e:
            app_logger.error(f"Error loading prompt {prompt_name}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error loading prompt: {str(e)}")
        
        prompt = {
            "name": prompt_name,
            "content": content
        }
        
        return ResponseModel(
            success=True,
            message=f"Prompt {prompt_name} found",
            data=prompt
        )
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error getting prompt {prompt_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))