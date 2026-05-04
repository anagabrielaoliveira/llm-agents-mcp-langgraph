from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import mlflow
from client import MCPClient
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o")

# 1.6 Logar uma run no MLflow usando o autolog do mlflow 
# Enabling tracing for LangGraph (LangChain)
mlflow.langchain.autolog()

# Optional: Set a tracking URI and an experiment
#mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("LangGraph")

# uv run mlflow server \
#   --host 0.0.0.0 \
#   --port 5000 \
#   --dev \
#   --cors-allowed-origins "*"
# http://172.25.117.120:5000 linux -> windows

async def build_mcp_client():
    client = MCPClient()
    await client.connect_to_server("server.py")
    return client

# 2.4 Integrar seu mcp no agente criado, ver logs e etc
async def main():
    with mlflow.start_run(run_name="MCP Agent Run"):
        mcp_client = await build_mcp_client()

        try:
            tools = await load_mcp_tools(mcp_client.session)

            # 1.5 Conectar a tool ao agente e deixar ele decidir quando chamá-la
            agent = create_agent(
                model=llm,
                tools=tools, # tools do MCP client
                system_prompt=(
                    "You are a math assistant. "
                    "You MUST use the available tools to solve any mathematical problem between two numbers."
                    "If you do not use a tool, the answer is considered wrong."
                )
            )

            input_data = {
                "messages": [
                    {"role": "user", "content": "I would like to know the result of 100*3.14"}
                ]
            }

            result = await agent.ainvoke(input_data)
            print("Agent response:", result)
            
        finally:
            await mcp_client.close()

asyncio.run(main())