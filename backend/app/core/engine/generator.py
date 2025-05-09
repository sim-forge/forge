"""
Generator module for SimForge.
Handles the generation of cognition sequences using LLMs.
"""
import os
import json
import asyncio
from typing import List, Dict, Any, Optional
import httpx
from ...core.utils.config import settings
from ...core.utils.logger import app_logger
from ...core.schema.cognition import CognitionSequence, CognitionRow, Belief

class Generator:
    """Generator class for creating cognition sequences using LLMs."""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
        self.client = httpx.AsyncClient(timeout=60.0)
        
    async def generate_sequence(
        self, 
        context: str, 
        schema: Optional[Dict[str, Any]] = None,
        n: int = 1, 
        temperature: float = 0.7
    ) -> List[CognitionSequence]:
        """
        Generate cognition sequences based on the provided context and schema.
        
        Args:
            context: The context for generation
            schema: Optional schema to guide generation
            n: Number of sequences to generate
            temperature: Temperature for generation
            
        Returns:
            List of generated CognitionSequence objects
        """
        app_logger.info(f"Generating {n} sequences with temperature {temperature}")
        
        if self.provider == "openai":
            return await self._generate_with_openai(context, schema, n, temperature)
        elif self.provider == "local":
            return await self._generate_with_local(context, schema, n, temperature)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def _generate_with_openai(
        self, 
        context: str, 
        schema: Optional[Dict[str, Any]],
        n: int, 
        temperature: float
    ) -> List[CognitionSequence]:
        """Generate sequences using OpenAI API."""
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        system_prompt = self._build_system_prompt(schema)
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Create batch requests
            tasks = []
            for _ in range(n):
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context}
                    ],
                    "temperature": temperature,
                    "response_format": {"type": "json_object"}
                }
                
                tasks.append(
                    self.client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload
                    )
                )
            
            # Execute batch requests concurrently
            responses = await asyncio.gather(*tasks)
            
            sequences = []
            for response in responses:
                response_data = response.json()
                content = response_data["choices"][0]["message"]["content"]
                
                # Parse the JSON response
                try:
                    sequence_data = json.loads(content)
                    sequence = self._parse_sequence(sequence_data)
                    sequences.append(sequence)
                except json.JSONDecodeError as e:
                    app_logger.error(f"Failed to parse JSON response: {e}")
                    app_logger.debug(f"Raw response: {content}")
                    continue
            
            return sequences
            
        except Exception as e:
            app_logger.error(f"Error generating with OpenAI: {str(e)}")
            raise
    
    async def _generate_with_local(
        self, 
        context: str, 
        schema: Optional[Dict[str, Any]],
        n: int, 
        temperature: float
    ) -> List[CognitionSequence]:
        """Generate sequences using a local LLM provider (e.g., Ollama, LM Studio)."""
        system_prompt = self._build_system_prompt(schema)
        
        try:
            # Assuming local LLM API is running at the configured URL
            local_api_url = settings.LOCAL_LLM_URL
            
            # Create batch requests
            tasks = []
            for _ in range(n):
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context}
                    ],
                    "temperature": temperature,
                    "response_format": {"type": "json_object"}
                }
                
                tasks.append(
                    self.client.post(
                        f"{local_api_url}/v1/chat/completions",
                        json=payload
                    )
                )
            
            # Execute batch requests concurrently
            responses = await asyncio.gather(*tasks)
            
            sequences = []
            for response in responses:
                response_data = response.json()
                content = response_data["choices"][0]["message"]["content"]
                
                # Parse the JSON response
                try:
                    sequence_data = json.loads(content)
                    sequence = self._parse_sequence(sequence_data)
                    sequences.append(sequence)
                except json.JSONDecodeError as e:
                    app_logger.error(f"Failed to parse JSON response: {e}")
                    app_logger.debug(f"Raw response: {content}")
                    continue
            
            return sequences
            
        except Exception as e:
            app_logger.error(f"Error generating with local LLM: {str(e)}")
            raise
    
    def _build_system_prompt(self, schema: Optional[Dict[str, Any]] = None) -> str:
        """Build the system prompt for generation."""
        base_prompt = """
You are SimForge, a synthetic cognition system. Your task is to generate a sequence of cognitive steps that represent how an agent would approach a problem.

For each step in the sequence, provide:
1. A clear goal or objective
2. The beliefs held at that point (with confidence levels from 0-1)
3. The operation or action taken (one of: "Reflect", "Act", "Plan", "Fork")
4. The output or result of that operation

The sequence should be coherent, logical, and demonstrate a progression of thought that leads to a solution or conclusion.

CONSTRAINTS:
- Each step should build on previous steps
- Beliefs should evolve as new information is discovered
- Operations should be specific and actionable
- Outputs should be concrete and informative

FORMAT YOUR RESPONSE AS A JSON OBJECT WITH THE FOLLOWING STRUCTURE:
{
  "title": "Title of the sequence",
  "description": "Brief description of the sequence",
  "rows": [
    {
      "goal": "Goal for step 1",
      "beliefs": [
        {"content": "Belief 1", "confidence": 0.8},
        {"content": "Belief 2", "confidence": 0.6}
      ],
      "operation": "Reflect",
      "output": "Output of step 1"
    },
    {
      "goal": "Goal for step 2",
      "beliefs": [
        {"content": "Updated belief 1", "confidence": 0.9},
        {"content": "New belief based on step 1", "confidence": 0.7}
      ],
      "operation": "Plan",
      "output": "Output of step 2"
    }
  ]
}
"""
        
        # If a schema is provided, include it in the system prompt
        if schema:
            schema_str = json.dumps(schema, indent=2)
            base_prompt += f"\n\nUSE THIS SCHEMA FOR YOUR RESPONSE:\n{schema_str}"
        
        return base_prompt
    
    def _parse_sequence(self, data: Dict[str, Any]) -> CognitionSequence:
        """Parse the sequence data into a CognitionSequence object."""
        rows = []
        
        for row_data in data.get("rows", []):
            beliefs = [
                Belief(
                    content=belief.get("content", ""),
                    confidence=belief.get("confidence", 1.0),
                    source=belief.get("source")
                )
                for belief in row_data.get("beliefs", [])
            ]
            
            # Ensure operation is one of the allowed values
            operation = row_data.get("operation", "Reflect")
            if operation not in ["Reflect", "Act", "Plan", "Fork"]:
                operation = "Reflect"
            
            row = CognitionRow(
                goal=row_data.get("goal", ""),
                beliefs=beliefs,
                operation=operation,
                output=row_data.get("output", "")
            )
            rows.append(row)
        
        return CognitionSequence(
            title=data.get("title", "Untitled Sequence"),
            description=data.get("description", ""),
            rows=rows,
            metadata=data.get("metadata", {})
        )

# Create a singleton instance
generator = Generator()