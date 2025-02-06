from abc import ABC
from typing import Dict

class AgentBaseModel(ABC):
    """
    Abstract base class representing an agent managing financial resources and GPU assets.

    This class provides foundational functionalities for agents participating in a market,
    allowing them to manage available capital, GPU ownership, and decision-making strategies.
    """

    def __init__(self, available_capital: float, owned_gpus: int, total_agents: int, distribution: Dict[str, int]):
        """
        Initializes an agent with financial resources, GPU ownership, and market data.

        Args:
            available_capital (float): The initial capital available to the agent. Must be non-negative.
            owned_gpus (int): The number of GPUs owned by the agent. Must be non-negative.
            total_agents (int): The total number of agents in the market.
            distribution (Dict[str, int]): A mapping representing the distribution of policies among agents.

        Raises:
            ValueError: If `available_capital` or `owned_gpus` is negative.
        """
        if available_capital < 0:
            raise ValueError("Available capital cannot be negative.")
        if owned_gpus < 0:
            raise ValueError("Number of owned GPUs cannot be negative.")

        self._available_capital = available_capital
        self._owned_gpus = owned_gpus
        self.total_agents = total_agents
        self.distribution = distribution
        self.current_stock = None # Will be set in the run method
        self.strategy = None  # This will be set in the subclasses

    @property
    def available_capital(self) -> float:
        """Returns the agent's available capital."""
        return self._available_capital

    @available_capital.setter
    def available_capital(self, value: float) -> None:
        """
        Sets the agent's available capital with validation.

        Args:
            value (float): The new value to be set for the available capital.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError("Available capital cannot be negative.")
        self._available_capital = value

    @property
    def owned_gpus(self) -> int:
        """Returns the number of GPUs owned by the agent."""
        return self._owned_gpus

    @owned_gpus.setter
    def owned_gpus(self, value: int) -> None:
        """
        Sets the number of owned GPUs with validation.

        Args:
            value (int): The new value to be set for the owned GPUs.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError("Number of owned GPUs cannot be negative.")
        self._owned_gpus = value

    def _buy(self, gpu_price: float) -> bool:
        """
        Attempts to purchase a GPU if the agent has sufficient capital and ava.

        Args:
            gpu_price (float): The cost of a single GPU. Must be positive.

        Returns:
            bool: True if the purchase was successful, False otherwise.

        Raises:
            ValueError: If `gpu_price` is not positive.
        """
        if gpu_price <= 0:
            raise ValueError("GPU price must be positive.")
        if self._available_capital >= gpu_price and self.current_stock > 0:
            self._available_capital -= gpu_price
            self._owned_gpus += 1
            return True
        return False

    def _sell(self, gpu_price: float) -> bool:
        """
        Attempts to sell a GPU if the agent has any available.

        Args:
            gpu_price (float): The selling price of a single GPU. Must be positive.

        Returns:
            bool: True if the sale was successful, False otherwise.

        Raises:
            ValueError: If `gpu_price` is not positive.
        """
        if gpu_price <= 0:
            raise ValueError("GPU price must be positive.")
        if self._owned_gpus > 0:
            self._available_capital += gpu_price
            self._owned_gpus -= 1
            return True
        return False

    def run(self, gpu_price: float, turn: int, current_stock:int) -> Dict[str, bool]:
        """
        Executes an action (buy, sell, or hold) based on the agent's strategy.

        Args:
            gpu_price (float): The current price of a GPU.
            turn (int): The current market turn or time step.
            current_stock (int): The current stock of GPUs available in the market.

        Returns:
            Dict[str, bool]: A dictionary containing:
                - "action" (str): The action taken ("buy", "sell", or "do_nothing").
                - "success" (bool): Whether the action was successful.

        Raises:
            NotImplementedError: If the strategy has not been set.
        """
        self.current_stock = current_stock
        if self.strategy is None:
            raise NotImplementedError("Strategy not set for the agent.")
        return self.strategy.decide(self, gpu_price, turn)