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

if __name__ == "__main__":

    graph = build_graph()

    initial_state = AgentState(
        user_goal="Research impact of agentic AI in healthcare"
    )

    result = graph.invoke(initial_state)

    print_report(result)
