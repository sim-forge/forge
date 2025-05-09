from typing import Dict, List, Optional, Union, Literal, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from .base import BaseSchema

class Belief(BaseModel):
    """A belief in the cognitive model."""
    content: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source: Optional[str] = None

class Action(BaseModel):
    """An action in the cognitive model."""
    description: str
    reasoning: Optional[str] = None
    expected_outcome: Optional[str] = None

class CognitionRow(BaseModel):
    """A row in the cognition table."""
    id: UUID = Field(default_factory=uuid4)
    goal: str
    beliefs: List[Belief]
    operation: Literal["Reflect", "Act", "Plan", "Fork"]
    output: Optional[str] = None
    parent_id: Optional[UUID] = None
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict)

class CognitionSequence(BaseSchema):
    """A sequence of cognition rows."""
    title: str
    description: Optional[str] = None
    rows: List[CognitionRow] = Field(default_factory=list)
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict)

class GenerationRequest(BaseModel):
    """Request model for generating cognition sequences."""
    context: str
    schema_config: Dict[str, Any] = Field(default_factory=dict)
    n: int = Field(default=1, ge=1, le=10)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    
class GenerationResponse(BaseModel):
    """Response model for generation requests."""
    sequences: List[CognitionSequence]
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict)

class ForkRequest(BaseModel):
    """Request model for forking a cognition row."""
    row_id: UUID
    sequence_id: UUID
    num_forks: int = Field(default=1, ge=1, le=5)
    fork_type: Literal["invert_beliefs", "change_goal", "alternative_operation"] = "alternative_operation"
    context: Optional[str] = None
    
class ForkResponse(BaseModel):
    """Response model for fork requests."""
    forks: List[CognitionRow]
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict)

class SchemaResponse(BaseModel):
    """Response model for schema requests."""
    schemas: List[Dict[str, Any]]
    
class PromptResponse(BaseModel):
    """Response model for prompt requests."""
    prompts: List[Dict[str, str]]