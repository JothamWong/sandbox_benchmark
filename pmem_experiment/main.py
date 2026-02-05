import asyncio
import os
from dotenv import load_dotenv

# LangChain / LangGraph Imports
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage

# Load API keys
load_dotenv()


async def run_supervisor():
    mcp_client = MultiServerMCPClient(
        {
            "sandbox-benchmarks": {
                "transport": "sse",
                "url": "http://localhost:8000/sse",
            }
        }
    )
    tools = await mcp_client.get_tools()
    print(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = create_react_agent(model, tools)
    query = (
        "I need to run a benchmark on the sandbox architecture. "
        "Please execute the following steps in order:\n"
        "1. Download the PDF to the browser sandbox.\n"
        "2. Convert that PDF to PPTX in the code sandbox.\n"
        "3. Retrieve the final presentation in the terminal sandbox.\n"
        "4. Finally, get the total transfer metrics and report them to me."
    )
    async for event in agent.astream(
        {"messages": [("user", query)]}, stream_mode="values"
    ):
        message = event["messages"][-1]
        if isinstance(message, ToolMessage):
            print(f"🛠️  [TOOL CALLED]: {message.name}")
            print(f"{message.content}")
            # Optional: print(f"Result: {message.content[:100]}...")
        elif hasattr(message, "content") and message.content:
            print(f"[{message.type.upper()}]: {message.content}")

        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(run_supervisor())
