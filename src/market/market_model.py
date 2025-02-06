import random
from typing import List, Dict

from src.logger_config import configure_logger
from src.agents.agent_base_model import AgentBaseModel

class Market:
    """
    Represents a market where agents buy, sell, or do nothing with GPUs.

    This class simulates a market environment where a set of agents interact by performing actions on GPUs 
    (buy, sell, or do nothing). The market price changes based on the agents' actions and is updated in each iteration.
    """

    def __init__(self, initial_price: float, iterations: int, stock:int, agents: List[AgentBaseModel], verbose: bool = False, log_to_file: bool = False):
        """
        Initializes the market with the specified parameters.

        Parameters:
            initial_price (float): The initial price of the GPU. Must be non-negative.
            iterations (int): The number of iterations to simulate.
            stock (int): The initial stock of GPUs available in the market. Must be non-negative.
            agents (List[AgentBaseModel]): A list of agents participating in the market.
            verbose (bool, optional): If True, enables verbose output to the console. Default is False.
            log_to_file (bool, optional): If True, logs output to a file. Default is False.
        """
        if initial_price < 0:
            raise ValueError("Initial price cannot be negative.")
        if iterations < 0:
            raise ValueError("Iterations must be non-negative.")
        if stock < 0:
            raise ValueError("Stock must be non-negative.")

        self._price = initial_price
        self._iterations = iterations
        self._stock = stock
        self.agents = agents
        self.history = []
        self.logger = configure_logger(verbose, log_to_file)

    @property
    def price(self) -> float:
        """Returns the current price of the GPU."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Sets the price of the GPU with validation.

        Parameters:
            value (float): The new price to set for the GPU. Must be non-negative.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def iterations(self) -> int:
        """Returns the number of iterations to simulate."""
        return self._iterations

    @iterations.setter
    def iterations(self, value: int) -> None:
        """
        Sets the number of iterations to simulate with validation.

        Parameters:
            value (int): The new number of iterations to simulate. Must be non-negative.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError("Iterations must be non-negative.")
        self._iterations = value

    @property
    def stock(self) -> int:
        """Returns the current stock of the GPU."""
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        """
        Sets the stock of the GPU with validation.

        Parameters:
            value (int): The new stock to set for the GPU. Must be non-negative.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        self._stock = value

    def _update_price_and_stock(self, result: Dict) -> None:
        """
        Updates the price of the GPU and the stock based on the agent's action.

        The price is increased by 0.5% if the agent buys the GPU and the action is successful,
        or decreased by 0.5% if the agent sells the GPU and the action is successful. The stock
        is also updated accordingly.

        Parameters:
            result (Dict): A dictionary containing the result of the agent's action, which includes the action type and success status.
        """
        if result["action"] == "buy" and result["success"]:
            self.price *= 1.005
            self.stock -= 1

        elif result["action"] == "sell" and result["success"]:
            self.price *= 0.995
            self.stock += 1

    def simulate(self) -> None:
        """
        Simulates the market for the specified number of iterations.

        In each iteration, the agents' actions are evaluated, and the market price is updated based on those actions. 
        The results of each agent's actions are recorded for later review.
        """
        for iteration in range(self.iterations):
            random.shuffle(self.agents)
            agent_results = []
            for agent in self.agents:
                result = agent.run(self.price, iteration, self.stock)
                self._update_price_and_stock(result)
                agent_results.append({
                    "type": type(agent).__name__,
                    "available_capital": agent.available_capital,
                    "owned_gpus": agent.owned_gpus,
                    "action": result["action"],
                    "success": result["success"],
                    "current_stock": self.stock,
                    "current_price": self.price
                })
            self._record_iteration(iteration, agent_results)

        self.logger.handlers.clear()

    def _record_iteration(self, iteration: int, agent_results: List[Dict]) -> None:
        """
        Records a summary of the market state at the end of an iteration.

        This method logs a summary of the actions and results of all agents in the current iteration,
        including their available capital, owned GPUs, and the success of their actions.

        Parameters:
            iteration (int): The current iteration number.
            agent_results (List[Dict]): A list of dictionaries containing the results of the agents' actions in the current iteration.
        """
        output = []
        output.append(f"\n--- Iteration {iteration + 1} ---")
        for i, agent_summary in enumerate(agent_results, start=1):
            output.append(f"Interaction {i} | Agent: {agent_summary['type']}, Capital: ${agent_summary['available_capital']:.2f}, "
                        f"GPUs: {agent_summary['owned_gpus']}, Action: {agent_summary['action']}, Success: {agent_summary['success']} | Current Stock: {agent_summary['current_stock']} | Current Price: ${agent_summary['current_price']:.2f}")
        self.logger.info("\n".join(output))