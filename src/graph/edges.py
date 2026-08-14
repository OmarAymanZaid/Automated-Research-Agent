from typing import Literal
from langgraph.graph import END
from graph.state import ReportState


def should_continue(state: ReportState) -> Literal["research_node", "END"]:
    """Conditional router function determining whether to continue revising or finish.
    
    Returns a string key matching either a target node name or the graph's END node.
    """
    # 1. Quality Gate Check
    if state.get("is_approved", False):
        return END

    # 2. Safety Bounds Check (Prevents Infinite Looping)
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)

    if iteration_count >= max_iterations:
        return END

    # 3. Revision Loop
    return "research_node"

