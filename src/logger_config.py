import logging
import os

def configure_logger(verbose: bool, log_to_file: bool) -> logging.Logger:
    """
    Configures the logger for the market simulation.

    This function sets up a logger that can either print output to the console,
    write output to a file, or both, depending on the provided flags.

    Parameters:
        verbose (bool): If True, the log messages will be printed to the console.
        log_to_file (bool): If True, the log messages will be written to a file.

    Returns:
        logging.Logger: A configured logger that can output messages based on the given settings.
    """
    logger = logging.getLogger('MarketSimulation')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')

    if verbose:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if log_to_file:
        log_file_path = os.path.join(os.path.dirname(__file__), '..', 'market_simulation.txt')
        file_handler = logging.FileHandler(log_file_path, mode='w')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger