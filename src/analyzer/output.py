import json
import logging
from io import TextIOWrapper
from typing import Dict

logger = logging.getLogger(__name__)


class JSONWriter:
    """
    Write results as JSON.

    Parameters:
        output: io.TextIOWrapper to the output (e.g., sys.stdout or a file).
        results: Dictionary holding the results to be written.
    """

    def __init__(self, output: TextIOWrapper, results: Dict):
        self.output = output
        self.results = results

    def write(self) -> None:
        """
        Write results as JSON formatted string to the output.
        """
        self.output.write(json.dumps(self.results))
        logger.info(f'Wrote output to {self.output.name}')
