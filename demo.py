"""
Agentic Tool Decider - Full Workflow Demo

This script provides an easy-to-understand tutorial on how to use the 
agentic-tool-decider library to power the decision-making logic of an AI agent.
"""

import time
from decider.registry import ToolRegistry
from decider.models import ToolCandidate
from decider.mock_selector import MockSelector


def main():
    print("="*60)
    print("Agentic Tool Decider - Full Workflow Demo".center(60))
    print("="*60)
    print("\n[Step 1] Setting up the Tool Registry...")
    print("As a developer, you define the tools your agent possesses.")
    
    # Initialize the registry
    registry = ToolRegistry()
    
    # Register our available tools
    registry.register(ToolCandidate(
        name="calculator",
        description="Performs arithmetic calculations (addition, subtraction, multiplication, division).",
        input_schema={"type": "object", "properties": {"expression": {"type": "string"}}}
    ))
    
    registry.register(ToolCandidate(
        name="search_knowledge",
        description="Searches a local knowledge base of workshop documents.",
        input_schema={"type": "object", "properties": {"query": {"type": "string"}}}
    ))
    
    print(f"[OK] Registered {len(registry.list_tools())} tools:")
    for tool in registry.list_tools():
        print(f"   - {tool.name}: {tool.description}")
        
    
    print("\n[Step 2] Initializing the Selector...")
    print("The Selector acts as the 'brain', evaluating requests against registered tools.")
    selector = MockSelector()
    
    
    print("\n[Step 3] Simulating an Agent Processing User Requests...")
    
    # A list of diverse user requests to demonstrate different outcomes
    sample_requests = [
        "Calculate 12 * 5", 
        "Find information about MCP in the workshop documents",
        "What is MCP?",
        "Help me with my project"
    ]
    
    print("-" * 60)
    for request in sample_requests:
        print(f"USER: \"{request}\"")
        time.sleep(0.5)
        
        # Core Library Usage: The Agent asks the decider what to do
        print("   -> Decider evaluating...")
        decision = selector.select(request, registry.list_tools())
        time.sleep(0.5)
        
        # The Agent runtime reacts to the decision
        if decision.decision == "call_tool":
            print(f"   [DECISION] Must call tool -> '{decision.tool}'")
            print(f"   [REASON]   {decision.reason}")
            print(f"   [ACTION]   Agent pauses generation, executes '{decision.tool}', and reads result")
            
        elif decision.decision == "no_tool":
            print(f"   [DECISION] No tool required.")
            print(f"   [REASON]   {decision.reason}")
            print(f"   [ACTION]   Agent answers the user directly from internal knowledge")
            
        elif decision.decision == "cannot_decide":
            print(f"   [DECISION] Cannot decide.")
            print(f"   [REASON]   {decision.reason}")
            print(f"   [ACTION]   Agent asks the user to clarify their request")
            
        print("-" * 60)
        
    print("\nDemo complete! Check out the code in demo.py to see how simple it is.")


if __name__ == "__main__":
    main()
