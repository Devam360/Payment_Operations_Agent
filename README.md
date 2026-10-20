# Agentic AI for Payment Operations

> **A self-healing payment infrastructure that Observes, Reasons, and Acts in real-time.**

## Overview
Traditional payment operations rely on static dashboards and reactive humans. By the time an alert triggers, revenue is already lost.

This project implements an Agentic AI that acts as an autonomous Reliability Engineer. It ingests streaming payment data, detects complex failure patterns (like issuer outages), and proactively reroutes traffic to healthy gateways—all without human intervention.

## Key Features
* **O.R.D.A Loop:** Implements a full Observe → Reason → Decide → Act cycle.
* **Stateful Memory:** Uses `LangGraph` to maintain context across time steps (remembering past failures).
* **Guardrails:** Includes risk assessment logic to decide when to act autonomously vs. escalating to humans.
* **Gemini-Powered:** Leverages Google's `gemini-1.5-flash` for high-speed, low-latency reasoning.

## Architecture

The system is built on a modular Python architecture:

| Component | File | Description |
| :--- | :--- | :--- |
| **The Brain** | `agent.py` | Uses LangGraph & Gemini to analyze metrics and form hypotheses. |
| **The Environment** | `simulator.py` | Generates realistic payment traffic, success rates, and simulates outages (e.g., Stripe 504s). |
| **The Hands** | `tools.py` | Executable functions that modify the simulator state (e.g., `reroute_traffic`). |
| **The Conductor** | `main.py` | Orchestrates the loop and injects failure scenarios for demonstration. |



## Setup

```bash
git clone https://github.com/Devam360/Payment_Operations_Agent.git
cd Payment_Operations_Agent
pip install -r requirements.txt
cp .env.example .env   # then put your Google API key in .env
python main.py
```

The Google Gemini API key is read from the `GOOGLE_API_KEY` environment variable, loaded from `.env` via `python-dotenv`. `.env` is git-ignored, so keep your real key there and never commit it.
