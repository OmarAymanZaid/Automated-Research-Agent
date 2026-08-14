from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.graph.state import ReportState
from src.graph.nodes import (
    make_research_node,
    make_writer_node,
    make_critic_node,
)
from src.graph.edges import should_continue


def build_report_graph(llm: BaseChatModel, enable_checkpointing: bool = True):
    """Assembles and compiles the LangGraph research & report generator workflow.
    
    Args:
        llm: Runtime LLM instance initialized at application startup.
        enable_checkpointing: Flag to attach in-memory checkpointer for thread history.
        
    Returns:
        Compiled StateGraph instance ready for invocation.
    """
    # 1. Initialize StateGraph with the schema blueprint
    builder = StateGraph(ReportState)

    # 2. Instantiate node subroutines with injected LLM
    research_node = make_research_node(llm)
    writer_node = make_writer_node(llm)
    critic_node = make_critic_node(llm)

    # 3. Register Nodes
    builder.add_node("research_node", research_node)
    builder.add_node("writer_node", writer_node)
    builder.add_node("critic_node", critic_node)

    # 4. Connect Fixed Edges (Linear Control Flow)
    builder.add_edge(START, "research_node")
    builder.add_edge("research_node", "writer_node")
    builder.add_edge("writer_node", "critic_node")

    # 5. Connect Conditional Edges (Dynamic Quality Gate Routing)
    builder.add_conditional_edges(
        "critic_node",
        should_continue,
        {
            "research_node": "research_node",
            END: END,
        },
    )

    # 6. Attach Persistence Checkpointer & Compile
    checkpointer = MemorySaver() if enable_checkpointing else None
    compiled_graph = builder.compile(checkpointer=checkpointer)

    return compiled_graph
