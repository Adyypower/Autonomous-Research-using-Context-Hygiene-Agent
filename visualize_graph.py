import sys
import os

# Add the project root to sys.path so we can import modules
sys.path.append(os.path.join(os.getcwd(), 'antigravity_agent'))

from antigravity_agent.graph.build_graph import build_graph

def generate_graph_image():
    print("Building graph...")
    graph = build_graph()
    
    print("Generating image...")
    # Get the graph image as PNG binary data
    png_data = graph.get_graph().draw_mermaid_png()
    
    output_file = "agent_graph.png"
    with open(output_file, "wb") as f:
        f.write(png_data)
        
    print(f"Graph image saved to {output_file}")

if __name__ == "__main__":
    generate_graph_image()
