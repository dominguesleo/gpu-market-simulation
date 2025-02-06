from typing import Dict

from src.agents.agent_base_model import AgentBaseModel
from src.strategies.strategy_trend_follower import TrendFollowerStrategy

class AgentTrendFollower(AgentBaseModel):
    """
    Agent that follows market trends. Buys if the price has increased by 1% or more,
    otherwise sells or does nothing based on probabilities.
    """

    def __init__(self, available_capital: float, owned_gpus: int, total_agents: int, distribution: Dict[str, int]):
        """
        Initializes a trend-following agent with financial resources and market data.

        Args:
            available_capital (float): The initial capital available to the agent.
            owned_gpus (int): The number of GPUs owned by the agent.
            total_agents (int): The total number of agents in the market.
            distribution (Dict[str, int]): A mapping representing the distribution of policies among agents.
        """
        super().__init__(available_capital, owned_gpus, total_agents, distribution)
        self.previous_price = None
        self.strategy = TrendFollowerStrategy()