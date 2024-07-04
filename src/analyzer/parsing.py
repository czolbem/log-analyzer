import abc
import logging
from io import TextIOWrapper
from typing import Sequence, List

import pandas as pd

logger = logging.getLogger(__name__)

COLUMNS = ['timestamp', 'response_header_size', 'client_ip', 'response_code', 'response_size', 'request_method', 'url',
           'username', 'access_destination_ip', 'response_type']


class BaseParser(abc.ABC):
    """
    Base class for the log parser. Provides a shared method to clean a parsed dataframe from malformed data.

    Parameters:
        timestamp_unit: The unit used to parse the provided timestamp. Examples: D,s,ms,us,ns
    """

    def __init__(self, timestamp_unit: str):
        self.timestamp_unit = timestamp_unit

    @abc.abstractmethod
    def parse_files_to_dataframe(self, files: Sequence[TextIOWrapper]) -> pd.DataFrame:
        pass

    def _clean_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Parse timestamp and numeric values and drop entries that contain malformed data after parsing (NaN).
        """
        dataframe['timestamp'] = pd.to_numeric(dataframe['timestamp'], errors='coerce')
        dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit=self.timestamp_unit)
        dataframe['response_header_size'] = pd.to_numeric(dataframe['response_header_size'], errors='coerce')
        dataframe['response_size'] = pd.to_numeric(dataframe['response_size'], errors='coerce')

        row_count_before_drop = len(dataframe)
        dataframe = dataframe.dropna()
        dropped_row_count = row_count_before_drop - len(dataframe)
        if dropped_row_count > 0:
            logger.warning(f'Ignored {dropped_row_count} log entries with unexpected values')

        return dataframe


class CSVParser(BaseParser):
    """
    Implementation of the BaseParser for CSV log files.

    Parameters:
        timestamp_unit: The unit used to parse the provided timestamp. Examples: 'D', 's', 'ms', 'us', 'ns'
        separator: The separator used in parsing the CSV
        on_bad_lines: Sets the behaviour of the parser when it encounters bad lines (e.g., too many columns). Values:
        'error', 'warn', 'skip'
    """

    def __init__(self, timestamp_unit: str, separator: str, on_bad_lines: str):
        self.separator = separator
        self.on_bad_lines = on_bad_lines
        super().__init__(timestamp_unit)

    def parse_files_to_dataframe(self, files: Sequence[TextIOWrapper]) -> pd.DataFrame:
        """
        Parse log files in CSV format to a single dataframe. Calls the parent _clean_dataframe to parse timestamp and
        numeric values and drop NaN values.
        """
        log_dataframes: List[pd.DataFrame] = []
        for file in files:
            # Setting index_col to False because the parser will otherwise get confused if the first line in a file is
            # malformed (i.e., has more columns than expected).
            dataframe = pd.read_csv(file, sep=self.separator, on_bad_lines=self.on_bad_lines, names=COLUMNS,
                                    dtype=pd.StringDtype(), index_col=False, keep_default_na=False)
            log_dataframes.append(dataframe)
        log_dataframe = pd.concat(log_dataframes)

        log_dataframe = self._clean_dataframe(log_dataframe)
        logger.info(f'Parsed {len(log_dataframe)} log lines')

        return log_dataframe
