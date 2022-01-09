import logging

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)

logger = logging.getLogger("shipping-service")

logger.setLevel(level=logging.DEBUG)
