"""
Forker module for SimForge.
Handles the creation of forks from existing cognition rows.
"""
import json
import asyncio
from typing import List, Dict, Any, Optional, Literal
from uuid import UUID, uuid4
import httpx
from ...core.utils.config import settings
from ...core.utils.logger import app_logger
from ...core.schema.cognition import CognitionRow, Belief

class Forker:
    """Forker class for creating forks from existing cognition rows."""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def create_forks(
        self,
        row: CognitionRow,
        num_forks: int = 1,
        fork_type: Literal["invert_beliefs", "change_goal", "alternative_operation"] = "alternative_operation",
        context: Optional[str] = None
    ) -> List[CognitionRow]:
        """
        Create forks from an existing cognition row.
        
        Args:
            row: The row to fork
            num_forks: Number of forks to create
            fork_type: Type of fork to create
            context: Optional context for generation
            
        Returns:
            List of forked CognitionRow objects
        """
        app_logger.info(f"Creating {num_forks} forks of type {fork_type}")
        
        if fork_type == "invert_beliefs":
            return await self._create_inverted_belief_forks(row, num_forks, context)
        elif fork_type == "change_goal":
            return await self._create_alternative_goal_forks(row, num_forks, context)
        elif fork_type == "alternative_operation":
            return await self._create_alternative_operation_forks(row, num_forks, context)
        else:
            raise ValueError(f"Unsupported fork type: {fork_type}")
    
    async def _create_inverted_belief_forks(
        self,
        row: CognitionRow,
        num_forks: int,
        context: Optional[str]
    ) -> List[CognitionRow]:
        """Create forks with inverted beliefs."""
        system_prompt = """
You are SimForge, a synthetic cognition system. Your task is to create alternative versions of a cognitive step by inverting or challenging some of the beliefs.

For each alternative version:
1. Identify 1-2 key beliefs to invert or challenge
2. Modify the confidence levels appropriately
3. Adjust the goal slightly if necessary based on the new beliefs
4. Provide a new operation that follows from the modified beliefs
5. Generate a new output that reflects the operation

The alternative versions should be coherent and plausible, representing genuinely different perspectives or approaches.

FORMAT YOUR RESPONSE AS A JSON ARRAY OF OBJECTS WITH THE FOLLOWING STRUCTURE:
[
  {
    "goal": "Modified goal based on inverted beliefs",
    "beliefs": [
      {"content": "Inverted belief 1", "confidence": 0.7},
      {"content": "Original belief 2", "confidence": 0.8}
    ],
    "operation": "New operation based on inverted beliefs",
    "output": "New output based on the operation"
  }
]
"""
        
        user_prompt = f"""
Original cognitive step:
Goal: {row.goal}
Beliefs:
{self._format_beliefs(row.beliefs)}
Operation: {row.operation}
Output: {row.output}

Create {num_forks} alternative versions by inverting or challenging some of the beliefs.
"""
        
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"
        
        return await self._generate_forks(row, system_prompt, user_prompt, num_forks)
    
    async def _create_alternative_goal_forks(
        self,
        row: CognitionRow,
        num_forks: int,
        context: Optional[str]
    ) -> List[CognitionRow]:
        """Create forks with alternative goals."""
        system_prompt = """
You are SimForge, a synthetic cognition system. Your task is to create alternative versions of a cognitive step by changing the goal while keeping most beliefs similar.

For each alternative version:
1. Create a new goal that represents a different approach or priority
2. Keep most beliefs the same, but adjust 1-2 if necessary for coherence
3. Provide a new operation that follows from the new goal
4. Generate a new output that reflects the operation

The alternative versions should be coherent and plausible, representing genuinely different approaches to the situation.

FORMAT YOUR RESPONSE AS A JSON ARRAY OF OBJECTS WITH THE FOLLOWING STRUCTURE:
[
  {
    "goal": "Alternative goal",
    "beliefs": [
      {"content": "Original belief 1", "confidence": 0.8},
      {"content": "Slightly modified belief 2", "confidence": 0.7}
    ],
    "operation": "New operation based on alternative goal",
    "output": "New output based on the operation"
  }
]
"""
        
        user_prompt = f"""
Original cognitive step:
Goal: {row.goal}
Beliefs:
{self._format_beliefs(row.beliefs)}
Operation: {row.operation}
Output: {row.output}

Create {num_forks} alternative versions by changing the goal while keeping most beliefs similar.
"""
        
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"
        
        return await self._generate_forks(row, system_prompt, user_prompt, num_forks)
    
    async def _create_alternative_operation_forks(
        self,
        row: CognitionRow,
        num_forks: int,
        context: Optional[str]
    ) -> List[CognitionRow]:
        """Create forks with alternative operations."""
        system_prompt = """
You are SimForge, a synthetic cognition system. Your task is to create alternative versions of a cognitive step by changing the operation while keeping the goal and beliefs the same.

For each alternative version:
1. Keep the same goal
2. Keep the same beliefs
3. Provide a different operation (Reflect, Act, Plan, or Fork)
4. Generate a new output that reflects the new operation

The alternative versions should be coherent and plausible, representing genuinely different approaches to the same goal and beliefs.

FORMAT YOUR RESPONSE AS A JSON ARRAY OF OBJECTS WITH THE FOLLOWING STRUCTURE:
[
  {
    "goal": "Same goal as original",
    "beliefs": [
      {"content": "Same belief 1", "confidence": 0.8},
      {"content": "Same belief 2", "confidence": 0.7}
    ],
    "operation": "Alternative operation",
    "output": "New output based on the alternative operation"
  }
]
"""
        
        user_prompt = f"""
Original cognitive step:
Goal: {row.goal}
Beliefs:
{self._format_beliefs(row.beliefs)}
Operation: {row.operation}
Output: {row.output}

Create {num_forks} alternative versions by changing the operation while keeping the goal and beliefs the same. Choose from operations: Reflect, Act, Plan, Fork.
"""
        
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"
        
        return await self._generate_forks(row, system_prompt, user_prompt, num_forks)
    
    async def _generate_forks(
        self,
        original_row: CognitionRow,
        system_prompt: str,
        user_prompt: str,
        num_forks: int
    ) -> List[CognitionRow]:
        """Generate forks using the LLM."""
        if self.provider == "openai":
            return await self._generate_forks_with_openai(original_row, system_prompt, user_prompt, num_forks)
        elif self.provider == "local":
            return await self._generate_forks_with_local(original_row, system_prompt, user_prompt, num_forks)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def _generate_forks_with_openai(
        self,
        original_row: CognitionRow,
        system_prompt: str,
        user_prompt: str,
        num_forks: int
    ) -> List[CognitionRow]:
        """Generate forks using OpenAI API."""
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.8,
                "response_format": {"type": "json_object"}
            }
            
            response = await self.client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
            
            # Parse the JSON response
            try:
                fork_data = json.loads(content)
                
                # Ensure we have a list of forks
                if not isinstance(fork_data, list):
                    if isinstance(fork_data, dict) and "forks" in fork_data:
                        fork_data = fork_data["forks"]
                    else:
                        app_logger.error("Invalid fork data format")
                        return []
                
                # Limit to requested number of forks
                fork_data = fork_data[:num_forks]
                
                # Create fork rows
                forks = []
                for fork in fork_data:
                    beliefs = [
                        Belief(
                            content=belief.get("content", ""),
                            confidence=belief.get("confidence", 1.0),
                            source=belief.get("source")
                        )
                        for belief in fork.get("beliefs", [])
                    ]
                    
                    # Ensure operation is one of the allowed values
                    operation = fork.get("operation", "Reflect")
                    if operation not in ["Reflect", "Act", "Plan", "Fork"]:
                        operation = "Reflect"
                    
                    fork_row = CognitionRow(
                        id=uuid4(),
                        goal=fork.get("goal", original_row.goal),
                        beliefs=beliefs,
                        operation=operation,
                        output=fork.get("output", ""),
                        parent_id=original_row.id
                    )
                    forks.append(fork_row)
                
                return forks
                
            except json.JSONDecodeError as e:
                app_logger.error(f"Failed to parse JSON response: {e}")
                app_logger.debug(f"Raw response: {content}")
                return []
                
        except Exception as e:
            app_logger.error(f"Error generating forks with OpenAI: {str(e)}")
            raise
    
    async def _generate_forks_with_local(
        self,
        original_row: CognitionRow,
        system_prompt: str,
        user_prompt: str,
        num_forks: int
    ) -> List[CognitionRow]:
        """Generate forks using a local LLM provider."""
        try:
            # Assuming local LLM API is running at the configured URL
            local_api_url = settings.LOCAL_LLM_URL
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.8,
                "response_format": {"type": "json_object"}
            }
            
            response = await self.client.post(
                f"{local_api_url}/v1/chat/completions",
                json=payload
            )
            
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
            
            # Parse the JSON response
            try:
                fork_data = json.loads(content)
                
                # Ensure we have a list of forks
                if not isinstance(fork_data, list):
                    if isinstance(fork_data, dict) and "forks" in fork_data:
                        fork_data = fork_data["forks"]
                    else:
                        app_logger.error("Invalid fork data format")
                        return []
                
                # Limit to requested number of forks
                fork_data = fork_data[:num_forks]
                
                # Create fork rows
                forks = []
                for fork in fork_data:
                    beliefs = [
                        Belief(
                            content=belief.get("content", ""),
                            confidence=belief.get("confidence", 1.0),
                            source=belief.get("source")
                        )
                        for belief in fork.get("beliefs", [])
                    ]
                    
                    # Ensure operation is one of the allowed values
                    operation = fork.get("operation", "Reflect")
                    if operation not in ["Reflect", "Act", "Plan", "Fork"]:
                        operation = "Reflect"
                    
                    fork_row = CognitionRow(
                        id=uuid4(),
                        goal=fork.get("goal", original_row.goal),
                        beliefs=beliefs,
                        operation=operation,
                        output=fork.get("output", ""),
                        parent_id=original_row.id
                    )
                    forks.append(fork_row)
                
                return forks
                
            except json.JSONDecodeError as e:
                app_logger.error(f"Failed to parse JSON response: {e}")
                app_logger.debug(f"Raw response: {content}")
                return []
                
        except Exception as e:
            app_logger.error(f"Error generating forks with local LLM: {str(e)}")
            raise
    
    def _format_beliefs(self, beliefs: List[Belief]) -> str:
        """Format beliefs for the prompt."""
        return "\n".join([
            f"- {belief.content} (confidence: {belief.confidence})"
            for belief in beliefs
        ])

# Create a singleton instance
forker = Forker()