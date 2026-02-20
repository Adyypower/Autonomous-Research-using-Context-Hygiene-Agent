from langgraph.graph import StateGraph, END
from state.agent_state import AgentState
from graph.build_graph import build_graph

print("Building graph...")
app = build_graph()

print("Generating image...")
png_data = app.get_graph().draw_mermaid_png()

with open("graph_architecture.png", "wb") as f:
    f.write(png_data)

print("Saved graph architecture to graph_architecture.png")
