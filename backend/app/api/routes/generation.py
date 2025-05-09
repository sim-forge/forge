import time
from fastapi import APIRouter, HTTPException
from ...core.schema.base import ResponseModel
from ...core.schema.cognition import GenerationRequest, GenerationResponse
from ...core.utils.logger import app_logger
from ...core.engine.generator import generator
from ...core.engine.validator import validator

router = APIRouter()

@router.post("/generate", response_model=ResponseModel)
async def generate_sequence(request: GenerationRequest):
    """
    Generate cognition sequences based on the provided context and schema.
    
    Args:
        request: The generation request containing context, schema, and parameters
        
    Returns:
        ResponseModel containing the generated sequences
    """
    try:
        app_logger.info(f"Generation request received with context: {request.context[:50]}...")
        
        start_time = time.time()
        
        # Generate sequences
        sequences = await generator.generate_sequence(
            context=request.context,
            schema=request.schema,
            n=request.n,
            temperature=request.temperature
        )
        
        # Validate sequences
        valid_sequences = []
        for sequence in sequences:
            if validator.validate_sequence(sequence):
                valid_sequences.append(sequence)
            else:
                app_logger.warning(f"Invalid sequence generated: {sequence.title}")
        
        processing_time = time.time() - start_time
        
        response = GenerationResponse(
            sequences=valid_sequences,
            metadata={
                "model": generator.model,
                "provider": generator.provider,
                "processing_time": processing_time,
                "temperature": request.temperature,
                "total_generated": len(sequences),
                "valid_sequences": len(valid_sequences)
            }
        )
        
        return ResponseModel(
            success=True,
            message=f"Generated {len(valid_sequences)} sequences successfully",
            data=response
        )
    except Exception as e:
        app_logger.error(f"Error generating sequence: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))