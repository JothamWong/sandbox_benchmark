import asyncio
import os
from dotenv import load_dotenv

from callback import Timer

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage, messages_to_dict
import json

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
    timer = Timer()
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        callbacks=[timer],
    )
    agent = create_react_agent(model, tools)
    query = (
        "I need to run a benchmark on the sandbox architecture. "
        "Please execute the following steps in order:\n"
        "1. Use the download_pdf_task() tool.\n"
        "2. Use the convert_pdf_task() tool.\n"
        "3. Use the verify_pptx_task() tool.\n"
        "4. Finally, get the total transfer metrics and report them to me."
    )
    final_state = None
    async for event in agent.astream(
        {"messages": [("user", query)]}, stream_mode="values"
    ):
        final_state = event
        message = event["messages"][-1]
        if isinstance(message, ToolMessage):
            print(f"[TOOL CALLED]: {message.name}")
            print(f"{message.content}")
        elif hasattr(message, "content") and message.content:
            print(f"[{message.type.upper()}]: {message.content}")

        print("-" * 40)

    if final_state:
        trajectory_data = {
            "query": query,
            "steps": messages_to_dict(final_state["messages"]),
            "inference_times": timer.times,
        }

        with open("nfs_trajectory.json", "w", encoding="utf-8") as f:
            json.dump(trajectory_data, f, indent=4)

        print(f"\n✅ Trajectory successfully dumped to trajectory.json")

    print("\n" + "=" * 50)

    print("LLM inference times")
    for time in timer.times:
        print(time)


if __name__ == "__main__":
    asyncio.run(run_supervisor())
