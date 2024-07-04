import logging


def init_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d",
        level=logging.INFO,
    )
