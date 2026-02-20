import streamlit as st
import sys
import os
import asyncio
from state.agent_state import AgentState
from graph.build_graph import build_graph

# Setup Page
st.set_page_config(page_title="Autonomous Research Agent", layout="wide")
st.title("🤖 Deep Research Agent")

# Sidebar for Config (Optional)
with st.sidebar:
    st.header("Settings")
    st.info("Using Gemini 2.5 Flash + Tavily Search")
    st.markdown("---")
    st.warning("Memory Persistence is Active (ChromaDB)")

# Initialize Trace State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("What would you like to research?"):
    
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Execution
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # UI Updates
        status_box = st.status("Thinking & Researching...", expanded=True)
        
        try:
            # Prepare Input
            initial_state = AgentState(
                user_goal=prompt,
                research_plan=[],
                tool_results=[],
                evaluation_score=0,
                reflection_notes={},
                compressed_context={},
                final_report="",
                iteration_count=0,
                working_memory=[]
            )
            
            # Run Graph
            app = build_graph()
            
            final_report = ""
            
            # Stream events to show progress
            # Note: invoke() blocks, so we use it directly for simplicity. 
            # Ideally stream() would be better for granular updates.
            result = app.invoke(initial_state)
            
            final_report = result.get("final_report", "No report generated.")
            
            status_box.update(label="Research Complete!", state="complete", expanded=False)
            
            st.markdown(final_report)
            
            # Add to history
            st.session_state.messages.append({"role": "assistant", "content": final_report})

        except Exception as e:
            st.error(f"An error occurred: {e}")
            status_box.update(label="Error Failed", state="error")
