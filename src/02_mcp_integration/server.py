# 2. FastMCP / MCP Client (segundo passo)

    # 2.1 Entender o que é o protocolo MCP, é um servidor que expõe "tools" para LLMs chamarem via JSON

        # --- o protocolo MCP serve como uma ponte entre o agente e a execução das tools. Ele expõe as tools, entao agora ao 
        # inves do agente ter a tool, o mcp (mcp client) faz uma chamada via json para invocar a tool no mcp server que 
        # executa a tool e devolve o resultado ao agente 

    # 2.2 Criar seu próprio servidor MCP e listar as tools disponíveis

    # 2.3 Chamar uma tool do MCP server manualmente, sem LLM ainda

    # 2.4 Integrar seu mcp no agente criado

import sys
from fastmcp import FastMCP

# 2.2 Criar seu próprio servidor MCP e listar as tools disponíveis
# Initialize FastMCP Server
mcp = FastMCP("test_server")

@mcp.tool()
async def simple_calculator(num1: float, num2: float, operator: str) -> str:
    """Perform a basic arithmetic operation between two numbers.

    Supported operators:
    - '+' for addition
    - '-' for subtraction
    - '*' for multiplication
    - '/' for division

    Returns the result as a string.

    Args: 
        num1: The first number in the calculation
        num2: The second number in the calculation
        operator: The operator to use in the calculation
    """

    # Perform the calculation based on the operator
    if operator == "+":
        return f"{num1 + num2}"
    elif operator == "-":
        return f"{num1 - num2}"
    elif operator == "*":
        return f"{num1 * num2}"
    elif operator == "/":
        if num2 == 0:
            return "Cannot divide by zero."
        return f"{num1 / num2}"
    
    return "Unsupported operator."

# Running the server 
def main():
    print("MCP Server is running...", file=sys.stderr) # envia a mensagem para stderr, ou seja, não interfere no MCP
    mcp.run() # Inicia o servidor MCP 

if __name__ == "__main__":
    main()
