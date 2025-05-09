import time
from fastapi import APIRouter, HTTPException
from ...core.schema.base import ResponseModel
from ...core.schema.cognition import ForkRequest, ForkResponse, CognitionRow
from ...core.utils.logger import app_logger
from ...core.engine.forker import forker
from ...core.engine.validator import validator

router = APIRouter()

@router.post("/fork", response_model=ResponseModel)
async def create_fork(request: ForkRequest):
    """
    Create forks from an existing cognition row.
    
    Args:
        request: The fork request containing row_id, sequence_id, and parameters
        
    Returns:
        ResponseModel containing the forked rows
    """
    try:
        app_logger.info(f"Fork request received for row {request.row_id}")
        
        start_time = time.time()
        
        # In a real implementation, we would fetch the row from a database
        # For now, we'll create a mock row
        original_row = CognitionRow(
            id=request.row_id,
            goal="Sample goal for forking",
            beliefs=[],
            operation="Reflect",
            output="Sample output for forking"
        )
        
        # Create forks
        forks = await forker.create_forks(
            row=original_row,
            num_forks=request.num_forks,
            fork_type=request.fork_type,
            context=request.context
        )
        
        # Validate forks
        valid_forks = []
        for fork in forks:
            if validator.validate_row(fork):
                valid_forks.append(fork)
            else:
                app_logger.warning(f"Invalid fork generated for row {request.row_id}")
        
        processing_time = time.time() - start_time
        
        response = ForkResponse(
            forks=valid_forks,
            metadata={
                "model": forker.model,
                "provider": forker.provider,
                "processing_time": processing_time,
                "fork_type": request.fork_type,
                "total_generated": len(forks),
                "valid_forks": len(valid_forks)
            }
        )
        
        return ResponseModel(
            success=True,
            message=f"Created {len(valid_forks)} forks successfully",
            data=response
        )
    except Exception as e:
        app_logger.error(f"Error creating forks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))