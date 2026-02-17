import sys
import os

# Ensure the parent directory is in the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph.build_graph import build_graph
from state.agent_state import AgentState

def print_report(result):
    print("\n\n" + "="*60)
    print("🤖 AUTOMATED RESEARCH REPORT")
    print("="*60)

    # Context might be a dict or a string (if hygiene failed)
    context = result.get("compressed_context", {})
    
    if isinstance(context, dict):
        print(f"\n🎯 MAIN GOAL: {result.get('user_goal')}")
        
        print(f"\n📝 SUMMARY:\n{context.get('summary', 'N/A')}")
        
        print("\n🔑 KEY FINDINGS:")
        for finding in context.get("key_findings", []):
            print(f"- {finding}")
            
        print("\n✅ BENEFITS:")
        for benefit in context.get("benefits", []):
            print(f"- {benefit}")
            
        print("\n⚠️ RISKS:")
        for risk in context.get('risks', []):
            print(f"- {risk}")

        if context.get('regulatory_notes'):
            print("\n⚖️ REGULATORY NOTES:")
            for note in context.get('regulatory_notes', []):
                print(f"- {note}")
            
    else:
        print("\nRaw Context (Structured parsing failed):")
        print(context)

    print("\n" + "-"*30)
    print(f"📊 STATISTICS")
    print(f"Confidence Score: {result.get('confidence_score')}")
    print(f"Iterations: {result.get('iteration_count')}")
    print("="*60 + "\n")

def main():
    print("🚀 Antigravity Interactive Demo Loop")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 40)

    graph = build_graph()

    while True:
        try:
            user_input = input("\n🔎 Enter research goal: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting demo...")
                break
            
            if not user_input:
                continue

            print(f"\n⏳ Starting research on: {user_input}...\n")
            
            initial_state = AgentState(
                user_goal=user_input
            )

            # Invoke the graph
            result = graph.invoke(initial_state)

            # Print the report
            print_report(result)
            
        except KeyboardInterrupt:
            print("\n\nExiting demo...")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
