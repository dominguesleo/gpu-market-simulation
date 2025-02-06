import random
from typing import Dict

from src.agents.agent_base_model import AgentBaseModel
from src.strategies.strategy_base_model import StrategyBaseModel

class RandomStrategy(StrategyBaseModel):
    def decide(self, agent: AgentBaseModel, gpu_price: float, turn: int) -> Dict[str, bool]:
        """
        Executes a buy, sell, or do nothing operation based on equal probability.

        The strategy randomly selects one of the following actions with equal probability:
        - "buy"
        - "sell"
        - "do_nothing"

        Parameters:
            agent (AgentBaseModel): The agent making the decision.
            gpu_price (float): The current price of the GPU.
            turn (int): The current turn of the agent in the iteration.

        Returns:
            Dict[str, bool]: A dictionary with the action taken and whether it was successful.
                            The dictionary has the following structure:
                            {
                                "action": str,  # The action taken: "buy", "sell", or "do_nothing".
                                "success": bool  # Whether the action was successful.
                            }
        """
        action = random.choice(["buy", "sell", "do_nothing"])
        result = {"action": action, "success": True}

        if action == "buy":
            result["success"] = agent._buy(gpu_price)
        elif action == "sell":
            result["success"] = agent._sell(gpu_price)

        return result