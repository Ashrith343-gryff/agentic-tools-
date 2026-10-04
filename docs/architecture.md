# Architecture

The Agentic Tool Decider is designed with a clear separation of concerns: it **decides** but it **does not execute**.

## High-Level Flow

```
User Query -> Agent Runtime -> Tool Decider -> Decision -> Agent Runtime -> Tool -> Result
```

1. **User Query**: The user asks the agent to do something.
2. **Agent Runtime**: The main agent loop gathers context.
3. **Tool Decider**: The agent asks the Decider, "Given this context and these tools, what should I do?"
4. **Decision**: The Decider evaluates, ranks, and returns a selected tool (or nothing).
5. **Agent Runtime**: The main agent (or an MCP client) takes the decision and actually executes the tool.
6. **Result**: The result is fed back into the agent loop.

**Important Note**: The decider does not execute tools. It merely returns the name of the tool and the suggested arguments.

## Core Components

### Registry
The `Registry` is the catalog. It stores the schemas, descriptions, and metadata for all available tools. It provides a standardized way to query what the agent *can* do.

### Selectors
Selectors are the brains of the decision process.
- **MockSelector**: A deterministic, rule-based selector that runs offline. It's fast, predictable, and requires no network.
- **JevSelector**: An AI-driven selector that calls out to Jev AI to make complex, nuanced decisions based on LLM reasoning.

### JevClient
A lightweight, standard-library-only (`urllib.request`) HTTP client used exclusively by the `JevSelector` to communicate with the Jev API.

### Ranking
When multiple tools could potentially solve a problem, the ranking component evaluates and scores them, ensuring the most appropriate tool is at the top of the list.

### Confidence Gate
A safety mechanism. Even if a selector chooses a tool, the Confidence Gate checks the decision's confidence score against a threshold. If it's too low, the gate blocks the decision, preventing reckless actions.

### Routing
The decider isn't just for low-level tools (like `read_file`). It can treat other sub-agents as tools. This allows the decider to act as a router, directing a complex query to the most appropriate specialized agent.

### Handoff
If the Decider cannot find a suitable tool, or if the Confidence Gate blocks all options, the system issues a Handoff. This signals the runtime that the agent cannot proceed autonomously and must ask the user for clarification or manual intervention.
