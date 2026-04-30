from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import mlflow

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o")

# 1.4 Criar uma Tool customizada do zero com o decorator @tool
@tool
def simple_calculator(num1: float, num2: float, operator: str) -> str:
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

# 1.6 Logar uma run no MLflow usando o autolog do mlflow 
# Enabling tracing for LangGraph (LangChain)
mlflow.langchain.autolog()

# Optional: Set a tracking URI and an experiment
#mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("LangGraph")

# 1.5 Conectar a tool ao agente e deixar ele decidir quando chamá-la
agent = create_agent(
    model=llm,
    tools=[simple_calculator],
    system_prompt="You are a helpful and precise assistant for solving math problems. You should return" \
    "the answer of the question. Use tools if necessary. "
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "I would like to know the result of 2*254"}
    ]
})

# mlflow server \
#   --host 0.0.0.0 \
#   --port 5000 \
#   --dev \
#   --cors-allowed-origins "*"
# http://172.25.117.120:5000 linux -> windows