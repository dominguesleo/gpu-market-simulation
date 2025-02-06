import random
from typing import Dict

from src.agents.agent_base_model import AgentBaseModel
from src.strategies.strategy_base_model import StrategyBaseModel

class TrendFollowerStrategy(StrategyBaseModel):
    def decide(self, agent: AgentBaseModel, gpu_price: float, turn: int) -> Dict[str, bool]:
        """
        Executes a buy, sell, or do nothing operation based on market trends.

        If the price has increased by 1% or more since the previous iteration, the agent has a 75% probability
        of buying and a 25% probability of doing nothing. Otherwise, the agent has a 20% probability of selling
        and an 80% probability of doing nothing.

        Parameters:
            agent (AgentBaseModel): The agent making the decision.
            gpu_price (float): The current price of the GPU.
            turn (int): The current turn of the agent in the iteration

        Returns:
            Dict[str, bool]: A dictionary with the action taken and whether it was successful.
                            The dictionary has the following structure:
                            {
                                "action": str,  # The action taken: "buy", "sell", or "do_nothing".
                                "success": bool  # Whether the action was successful.
                            }
        """
        if hasattr(agent, "previous_price") and agent.previous_price is not None:
            price_change = (gpu_price - agent.previous_price) / agent.previous_price
        else:
            price_change = None

        if price_change is None or price_change >= 0.01:
            action = random.choices(["buy", "do_nothing"], [0.75, 0.25])[0]
        else:
            action = random.choices(["sell", "do_nothing"], [0.20, 0.80])[0]

        result = {"action": action, "success": True}

        if action == "buy":
            result["success"] = agent._buy(gpu_price)
        elif action == "sell":
            result["success"] = agent._sell(gpu_price)

        agent.previous_price = gpu_price
        return result