"""
python -m main
"""

import sys
from langchain_core.messages import HumanMessage

from helpers.settings import get_settings
from stores.llm.LLMFactory import LLMProviderFactory
from graph.builder import build_report_graph


def main():
    print("=" * 60)
    print("🤖 Automated Research & Quality-Gated Report Generator")
    print("Type '/exit' or 'q' to quit.")
    print("=" * 60)

    # 1. Initialize Runtime Resources
    settings = get_settings()
    llm_factory = LLMProviderFactory(settings)
    llm = llm_factory.create_llm()

    # 2. Assemble and Compile Graph
    graph = build_report_graph(llm=llm, enable_checkpointing=True)

    # Unique thread configuration for state persistence
    thread_config = {"configurable": {"thread_id": "cli_session_1"}}

    # 3. Interactive CLI Loop
    while True:
        try:
            user_input = input("\n📝 Enter a topic for research & report generation: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["/exit", "exit", "q", "quit"]:
                print("\nGoodbye! 👋")
                sys.exit(0)

            # 4. Prepare Initial State Payload
            initial_state = {
                "topic": user_input,
                "messages": [HumanMessage(content=f"Generate report on: {user_input}")],
                "search_queries": [],
                "raw_researches": [],
                "draft_report": "",
                "critique": "",
                "iteration_count": 0,
                "max_iterations": 3,
                "is_approved": False,
            }

            print(f"\n🚀 Running Agent Pipeline for topic: '{user_input}'...")
            print("-" * 60)

            # 5. Stream Graph Updates Event-by-Event
            for event in graph.stream(initial_state, config=thread_config, stream_mode="updates"):
                for node_name, node_update in event.items():
                    print(f"\n🔄 [Node: {node_name}] Executed.")
                    
                    if "critique" in node_update:
                        status = "✅ Approved" if node_update.get("is_approved") else "❌ Needs Revision"
                        print(f"   Evaluation: {status}")
                        print(f"   Feedback: {node_update['critique']}")
                    
                    if "draft_report" in node_update and node_name == "writer_node":
                        print("   Draft updated.")

            # 6. Fetch Final Compiled State
            final_state = graph.get_state(thread_config).values
            
            print("\n" + "=" * 60)
            print("📋 FINAL REPORT OUTPUT")
            print("=" * 60)
            print(final_state.get("draft_report", "No report generated."))
            print("=" * 60)

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Exiting... 👋")
            sys.exit(0)


if __name__ == "__main__":
    main()