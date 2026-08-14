from typing import Annotated, TypedDict
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ReportState(TypedDict):
    """Single source of truth passed across all graph nodes."""
    
    # Message stream using the built-in add_messages reducer
    messages: Annotated[list[BaseMessage], add_messages]
    
    # Input domain parameters
    topic: str
    
    # State accumulated across execution
    search_queries: Annotated[list[str], operator.add]
    raw_researches: Annotated[list[str], operator.add]
    draft_report: str
    critique: str
    
    # Execution & Routing Controls
    iteration_count: int
    max_iterations: int
    is_approved: bool
