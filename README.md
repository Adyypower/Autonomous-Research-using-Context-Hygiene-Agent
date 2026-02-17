# 🌌 Antigravity Autonomous Research Agent

![Agent Graph](agent_graph.png)

“Probabilistic Intelligence, Deterministic Control.”

This repository contains an Autonomous Agentic Research System — a structured AI agent designed for deep, recursive research tasks.
Unlike standard chatbots that lose context or hallucinate under complex workloads, this system uses a deterministic graph architecture to plan, execute, evaluate, and refine its outputs in a controlled pipeline.

Built by Aditya.

🏗️ System Architecture

This system is built on LangGraph, treating large language models as components in a larger state machine — not as autonomous thinkers.

The Cyclic Execution Graph

The agent progresses through a repeating loop where each step has a clearly defined role:

Planner Node: Breaks the user’s high-level request into specific ordered sub-tasks.

Research Node: Executes targeted web searches (e.g., via DuckDuckGo Search).

Hygiene Node: Cleans and structures raw text into JSON.

Evaluator Node: Applies rule-based scoring to validate the result.

Reflection Node: Uses LLM critique to decide whether to reuse results or retry.

Retrieval Node: Pulls relevant long-term knowledge from vector memory.

Reporter Node: Generates the final verified report.

This structured flow enforces control and accountability at every step.

🚀 Unique Features
🧹 1. Context Hygiene (Signal Amplification)

Most autonomous systems fail because they overload the model with raw HTML and unstructured search data. This system uses a dedicated Hygiene Node that:

Takes large, noisy input (e.g., ~15,000 characters of raw text),

Outputs clean, strict JSON with relevant fields (e.g., key_findings, statistics, risks),

Reduces token noise by ~90%, improving reasoning focus.

This ensures the model works with signal, not clutter.

🧠 2. Deterministic Control on Probabilistic Models

We explicitly separate:

Probabilistic: Content generation done by the LLM

Deterministic: Workflow and logic controlled by code

This means the agent cannot skip steps or proceed on low confidence. If an output scores poorly, the system loops back and refines it — no guesswork allowed.

🧩 3. Model-Agnostic Design

While currently configured to use Gemini 2.5 Flash, the architecture allows swapping any supported model, including:

GPT-4

Claude 3.5 Sonnet

Local models (Llama, Ollama, etc.)

The control flow stays the same regardless of model choice.

🧠 Memory Handling (RAG)

To simulate long-term memory:

Working Memory captures transient context within the current loop.

Long-Term Memory sits in a ChromaDB vector store.

Verified facts are embedded and stored in memory. When a follow-up question arises many steps later, the system performs a semantic retrieval (RAG) from ChromaDB — giving focused, relevant context without context window clutter.

This gives the system effectively infinite recall.

🔮 Future Plans

Multi-Agent Swarm: Separate Critic & Writer agents

Human-In-The-Loop: Manual plan approval via UI

Local Execution: Full offline support with Ollama or local embeddings

Built with ❤️ by Aditya
