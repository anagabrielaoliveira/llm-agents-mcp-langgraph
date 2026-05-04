import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 2.3 Chamar uma tool do MCP server manualmente, sem LLM ainda
class MCPClient:
    def __init__(self):
        # Initialize session and client objects 
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        #self.tools = []

    # method to connect to an MCP server
    async def connect_to_server(self, server_script_path: str):
        """ Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py file) to connect to
        """
        # StdioServerParameters é usada para configurar o comando, argumentos e variaveis de ambiente
        # para rodar o Stdio server.
        server_params  = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        #---------------------------------------------
        # List available tools
        response = await self.session.list_tools()
        self.tools = response.tools
        #print(f"Available tools: {self.tools}")
        print("Connected to MCP server successfully.")
        #---------------------------------------------

    async def call_tool(self):
        tool_name = self.tools[0].name
        print(f"Calling tool: {tool_name}")

        tool_args = {
                "num1": 3.14,
                "num2": 1000,
                "operator": "*"
            }
        
        # Initiate call
        result = await self.session.call_tool(tool_name, tool_args)
        print(f"Tool result: {result.content[0].text}")
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    await client.connect_to_server(sys.argv[1]) # server.py"
    await client.call_tool()

if __name__ == "__main__":
    import sys
    asyncio.run(main())
        