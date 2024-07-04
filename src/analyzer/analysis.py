import logging
from io import TextIOWrapper
from typing import Sequence

from analyzer.output import JSONWriter
from analyzer.parsing import CSVParser
from analyzer.statistics import LogStatistics

logger = logging.getLogger(__name__)


class LogAnalyzer:
    """
    Parse a range of log files and write requested log statistics to the specified output.

    Parameters:
        input_files: Collection of input files of type io.TextIOWrapper as provided by ArgumentParser.
        output: Output of type io.TextIOWrapper as provided by ArgumentParser.
        mfip: If true, calculate most frequent IP.
        lfip: If true, calculate least frequent IP.
        eps: If true, calculate events per second.
        bytes: If true, calculate total amount of bytes exchanged.
    """

    def __init__(self,
                 input_files: Sequence[TextIOWrapper],
                 output: TextIOWrapper,
                 mfip: bool,
                 lfip: bool,
                 eps: bool,
                 bytes: bool,
                 ):
        self.input_files = input_files
        self.mfip = mfip
        self.lfip = lfip
        self.eps = eps
        self.bytes = bytes
        self.output = output

    def analyze_log_files(self) -> None:
        """
        Parse log files into a dataframe and generate statistics over this dataframe based on the boolean flags
        on the object. Write result to output. Currently, parses logs as CSV and writes results as JSON.
        """
        # Configuration values for the Parser could be added as options to the CLI. For different input types, different
        # Parsers could be implemented.
        log_dataframe = CSVParser(timestamp_unit='s', separator=r'\s+', on_bad_lines='warn').parse_files_to_dataframe(
            self.input_files)

        if len(log_dataframe) == 0:
            logger.warning('No log entries to analyze. Exiting')
            return

        log_statistics = LogStatistics(log_dataframe)
        results = {}

        if self.mfip:
            results['mfip'] = log_statistics.most_frequent_ip()
            logger.info('Adding most frequent IP (--mfip) to result')
        if self.lfip:
            results['lfip'] = log_statistics.least_frequent_ip()
            logger.info('Adding least frequent IP (--lfip) to result')
        if self.eps:
            results['eps'] = log_statistics.events_per_second()
            logger.info('Adding events per second (--eps) to result')
        if self.bytes:
            results['bytes'] = log_statistics.total_amount_of_bytes_exchanged()
            logger.info('Adding total amount of bytes exchanged (--bytes) to result')

        # For different output types, different Writers could be implemented.
        JSONWriter(output=self.output, results=results).write()
