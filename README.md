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


