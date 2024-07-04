from io import StringIO

import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

from analyzer.parsing import CSVParser


class TestCSVParser:
    file1_content = """
    1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -
    1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html
    """
    file2_content = """
    1157689320.343   1357 10.105.21.199 TCP_REFRESH_HIT/304 214 GET http://www.goonernews.com/styles.css badeyek DIRECT/207.58.145.61 -
    """

    def test_parse_files_to_dataframe_parses_multiple_files_to_one_dataframe(self) -> None:
        csv_parser = CSVParser(timestamp_unit='s', separator=r'\s+', on_bad_lines='warn')
        file1 = StringIO(self.file1_content)
        file2 = StringIO(self.file2_content)

        dataframe = csv_parser.parse_files_to_dataframe([file1, file2])

        assert type(dataframe) is pd.DataFrame
        assert len(dataframe) == 3

    def test_parse_files_to_dataframe_converts_timestamp_string_to_timestamp(self) -> None:
        csv_parser = CSVParser(timestamp_unit='s', separator=r'\s+', on_bad_lines='warn')
        file = StringIO(self.file2_content)

        dataframe = csv_parser.parse_files_to_dataframe([file])

        assert type(dataframe['timestamp'].iloc[0]) is pd.Timestamp

    def test_parse_files_to_dataframe_converts_response_header_size_to_numeric(self) -> None:
        csv_parser = CSVParser(timestamp_unit='s', separator=r'\s+', on_bad_lines='warn')
        file = StringIO(self.file2_content)

        dataframe = csv_parser.parse_files_to_dataframe([file])

        assert is_numeric_dtype(dataframe['response_header_size'])

    def test_parse_files_to_dataframe_converts_response_size_to_numeric(self) -> None:
        csv_parser = CSVParser(timestamp_unit='s', separator=r'\s+', on_bad_lines='warn')
        file = StringIO(self.file2_content)

        dataframe = csv_parser.parse_files_to_dataframe([file])

        assert is_numeric_dtype(dataframe['response_size'])

    def test_parse_files_to_dataframe_drops_nan_values(self) -> None:
        csv_parser = CSVParser(timestamp_unit='s', separator=r'\s+', on_bad_lines='warn')
        file_content = """
        1157689312.049   ABC 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -
        1157689320.327   2864 10.105.21.199 TCP_MISS/200 ABC GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html
        1157689320.ABC   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html
        1157689320.327   1111 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ TheOnlyEntryLeft DIRECT/207.58.145.61 text/html
        """
        file = StringIO(file_content)

        dataframe = csv_parser.parse_files_to_dataframe([file])

        assert len(dataframe) == 1
        assert dataframe.iloc[0]['username'] == 'TheOnlyEntryLeft'
