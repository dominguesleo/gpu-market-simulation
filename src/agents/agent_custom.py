from typing import Dict

from src.agents.agent_base_model import AgentBaseModel
from src.strategies.strategy_custom import CustomStrategy

class AgentCustom(AgentBaseModel):
    """
    Custom agent that follows a strategy to maximize profit by buying low and selling high.

    The agent follows these rules:
    - Buy if the current price is at least 10% lower than the historical average price.
    - Sell if the current price is at least 5% higher than the historical average price.
    - If there are few iterations left, sell all remaining GPUs.

    The agent aims to end the simulation with zero GPUs and maximize its balance.
    """

    def __init__(self, available_capital: float, owned_gpus: int, total_agents: int, distribution: Dict[str, int], total_iterations: int):
        """
        Initializes a custom agent with financial resources and market data.

        Args:
            available_capital (float): The initial capital available to the agent.
            owned_gpus (int): The number of GPUs owned by the agent.
            total_agents (int): The total number of agents in the market.
            distribution (Dict[str, int]): A mapping representing the distribution of policies among agents.
            total_iterations (int): The total number of iterations in the simulation.
        """
        super().__init__(available_capital, owned_gpus, total_agents, distribution)
        self.previous_price = None
        self.strategy = CustomStrategy(total_iterations)