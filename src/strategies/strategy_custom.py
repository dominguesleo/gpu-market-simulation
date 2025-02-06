import random
from typing import Dict

from src.agents.agent_base_model import AgentBaseModel
from src.strategies.strategy_base_model import StrategyBaseModel

class CustomStrategy(StrategyBaseModel):
    def __init__(self, total_iterations: int):
        self.total_iterations = total_iterations
        self.iteration_count = 0
        self.lowest_price = None
        self.highest_price = None
        self.price_history = []
        self.target_profit_percentage = 0.1
        self.buy_threshold = 0.10
        self.sell_threshold = 0.05
        self.safety_margin = 1

    def decide(self, agent: AgentBaseModel, gpu_price: float, turn: int) -> Dict[str, bool]:
        """
        Executes a buy, sell, or do nothing operation based on a custom strategy.

        The strategy aims to maximize the agent's balance by buying low and selling high,
        and ensuring the agent ends with zero GPUs. The specific strategy is as follows:
        - Buy if the current price is at least 10% lower than the historical average price.
        - Sell if the current price is at least 5% higher than the historical average price.
        - If there are few iterations left, sell all remaining GPUs.

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

        current_iteration = self.iteration_count
        self.iteration_count += 1
        iterations_left = self.total_iterations - current_iteration

        # Add the current price to the history for analysis
        self.price_history.append(gpu_price)
        if len(self.price_history) > 10:
            self.price_history.pop(0)

        # Set reference prices
        if self.lowest_price is None or gpu_price < self.lowest_price:
            self.lowest_price = gpu_price
        if self.highest_price is None or gpu_price > self.highest_price:
            self.highest_price = gpu_price

        # Calculate the historical average price
        avg_price = sum(self.price_history) / len(self.price_history)

        # If there are few iterations left, sell all remaining GPUs
        if iterations_left <= agent.owned_gpus + self.safety_margin:
            action = "sell" if agent.owned_gpus > 0 else "do_nothing"
        else:
            # Buy only if the price is at least 10% lower than the average price
            if gpu_price <= avg_price * (1 - self.buy_threshold) and agent.available_capital >= gpu_price:
                action = "buy"
            # Sell if the price is at least 5% higher than the average purchase price
            elif gpu_price >= avg_price * (1 + self.sell_threshold) and agent.owned_gpus > 0:
                action = "sell"
            else:
                action = "do_nothing"

        agent.previous_price = gpu_price

        result = {"action": action, "success": True}

        if action == "buy":
            result["success"] = agent._buy(gpu_price)
        elif action == "sell":
            result["success"] = agent._sell(gpu_price)

        return result