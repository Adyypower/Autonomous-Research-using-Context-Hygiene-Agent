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

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "run_agent" not in st.session_state:
    st.session_state.run_agent = False
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""
if "research_app" not in st.session_state:
    st.session_state.research_app = build_graph()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("What would you like to research?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.current_prompt = prompt
    st.session_state.run_agent = True
    # Clear previous thread state if any
    config = {"configurable": {"thread_id": "research_thread"}}
    st.session_state.research_app.update_state(config, {"final_report": ""}, as_node="reporter")
    st.rerun()

# Agent Execution Loop
if st.session_state.run_agent:
    with st.chat_message("assistant"):
        status_box = st.status("Thinking & Researching...", expanded=True)
        
        try:
            app = st.session_state.research_app
            config = {"configurable": {"thread_id": "research_thread"}}
            prompt = st.session_state.current_prompt

            # 1. Start or Resume Graph
            state = app.get_state(config)
            
            if not state.values or not state.values.get("user_goal"):
                # Start fresh
                initial_state = AgentState(
                    user_goal=prompt,
                    research_plan=[],
                    tool_results=[],
                    evaluation_score=0,
                    confidence_score=0,
                    reflection_notes={},
                    compressed_context={},
                    final_report="",
                    iteration_count=0,
                    working_memory=[],
                    logs=[],
                    is_plan_approved=False
                )
                app.invoke(initial_state, config)
            
            # 2. Check for HITL Interrupt
            state = app.get_state(config)
            if state.next and state.next[0] == "research":
                status_box.update(label="Planning Complete - Awaiting Approval", state="running", expanded=True)
                
                current_plan = state.values.get("research_plan", [])
                
                st.subheader("📋 Proposed Research Plan")
                st.write("The planner has broken down your request into these sub-tasks. You can edit them below:")
                
                # Editable tasks
                new_plan = []
                for i, task in enumerate(current_plan):
                    edited_task = st.text_input(f"Task {i+1}", value=task, key=f"task_{i}_edit")
                    if edited_task:
                        new_plan.append(edited_task)
                
                # Add new task option
                new_task = st.text_input("➕ Add more to the plan...", key="new_task_input")
                if new_task:
                    new_plan.append(new_task)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🚀 Approve & Start Research", type="primary"):
                        app.update_state(config, {"research_plan": new_plan, "is_plan_approved": True})
                        with st.spinner("Resuming research..."):
                            app.invoke(None, config)
                            st.rerun()
                
                with col2:
                    if st.button("🛑 Cancel"):
                        st.session_state.messages.append({"role": "assistant", "content": "Research cancelled."})
                        st.session_state.run_agent = False
                        st.rerun()

                st.stop()

            # 3. Final Output and Trace
            state = app.get_state(config)
            final_report = state.values.get("final_report", "No report generated.")
            logs = state.values.get("logs", [])

            status_box.update(label="Research Complete!", state="complete", expanded=False)
            st.markdown(final_report)

            with st.expander("🔍 Internal Trace (System Work)", expanded=False):
                if not logs:
                    st.info("No trace data available.")
                else:
                    for entry in logs:
                        node = entry.get("node", "unknown").upper()
                        st.markdown(f"**Step: {node}**")
                        if node == "PLANNER":
                            st.json({"Input Goal": entry.get("input"), "Generated Plan": entry.get("output")})
                        elif node == "RESEARCH":
                            st.write(f"📡 Search Query: `{entry.get('query')}`")
                            st.write(f"📥 Characters Received: {entry.get('result_length')}")
                        elif node == "HYGIENE":
                            st.write(f"🧹 Cleaned `{entry.get('raw_chars')}` raw chars + `{entry.get('rag_chars')}` RAG chars")
                            st.write(f"✅ Extracted `{entry.get('findings_count')}` key findings.")
                        elif node == "EVALUATOR":
                            st.write(f"📊 Confidence: {entry.get('relevance')}")
                            st.write(f"⚠️ Gaps: {', '.join(entry.get('gaps')) if entry.get('gaps') else 'None'}")
                        elif node == "REFLECTION":
                            decision = entry.get('decision', 'unknown')
                            if decision == 'refine':
                                st.warning(f"🤔 Decision: **{decision.upper()}** - Need more data.")
                                st.write(f"🔄 Refinements: {entry.get('refinements')}")
                            else:
                                st.success(f"🎯 Decision: **{decision.upper()}** - Quality is sufficient.")
                        elif node == "RETRIEVAL":
                            st.info(f"🧠 Recovered `{entry.get('docs_retrieved', 0)}` items from long-term memory.")
                        elif node == "REPORTER":
                            st.success(f"📝 {entry.get('status', 'Writing Report')}")
                        st.divider()

            st.session_state.messages.append({"role": "assistant", "content": final_report})
            st.session_state.run_agent = False # Reset for next query

        except Exception as e:
            st.error(f"An error occurred: {e}")
            status_box.update(label="Error Failed", state="error")
            import traceback
            st.code(traceback.format_exc())
            st.session_state.run_agent = False
