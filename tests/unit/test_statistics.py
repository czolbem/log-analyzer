import math

import pandas as pd
import pytest

from analyzer.statistics import LogStatistics


class TestStatistics:
    test_dataframe: pd.DataFrame

    @pytest.fixture(autouse=True)
    def setup_test(self) -> None:
        columns = ['timestamp', 'response_header_size', 'client_ip', 'response_code', 'response_size', 'request_method',
                   'url', 'username', 'access_destination_ip', 'response_type']
        data = [
            ['1157689312.000', '100', '10.105.21.199', 'TCP_MISS/200', '200', 'CONNECT', 'login.yahoo.com:443',
             'badeyek', 'DIRECT/209.73.177.115', '-'],
            ['1157689312.150', '100', '10.105.21.199', 'TCP_MISS/200', '300', 'CONNECT', 'login.yahoo.com:443',
             'badeyek', 'DIRECT/209.73.177.115', '-'],
            ['1157689313.000', '100', '10.105.21.198', 'TCP_MISS/200', '100', 'CONNECT', 'login.yahoo.com:443',
             'badeyek', 'DIRECT/209.73.177.115', '-'],
        ]
        self.test_dataframe = pd.DataFrame(data=data, columns=columns)
        self.test_dataframe['timestamp'] = pd.to_numeric(self.test_dataframe['timestamp'], errors='coerce')
        self.test_dataframe['timestamp'] = pd.to_datetime(self.test_dataframe['timestamp'], unit='s')
        self.test_dataframe['response_header_size'] = pd.to_numeric(self.test_dataframe['response_header_size'],
                                                                    errors='coerce')
        self.test_dataframe['response_size'] = pd.to_numeric(self.test_dataframe['response_size'], errors='coerce')

    def test_most_frequent_ip_returns_most_frequent_ip(self) -> None:
        log_statistics = LogStatistics(self.test_dataframe)
        expected_most_frequent_ip = '10.105.21.199'

        actual_most_frequent_ip = log_statistics.most_frequent_ip()

        assert actual_most_frequent_ip == expected_most_frequent_ip

    def test_least_frequent_ip_returns_least_frequent_ip(self) -> None:
        log_statistics = LogStatistics(self.test_dataframe)
        expected_least_frequent_ip = '10.105.21.198'

        actual_lest_frequent_ip = log_statistics.least_frequent_ip()

        assert actual_lest_frequent_ip == expected_least_frequent_ip

    def test_events_per_second_returns_events_per_second(self) -> None:
        log_statistics = LogStatistics(self.test_dataframe)
        expected_events_per_second = 3.0

        actual_events_per_second = log_statistics.events_per_second()

        assert math.isclose(actual_events_per_second, expected_events_per_second, rel_tol=1e-09, abs_tol=1e-09)

    def test_total_amount_of_bytes_exchanged_returns_total_amount_of_bytes_exchanged(self) -> None:
        log_statistics = LogStatistics(self.test_dataframe)
        expected_amount_of_bytes = 900

        actual_amount_of_bytes = log_statistics.total_amount_of_bytes_exchanged()

        assert actual_amount_of_bytes == expected_amount_of_bytes

    def test_total_amount_of_bytes_exchanged_returns_total_amount_of_bytes_exchanged_excluding_negative_values(
            self) -> None:
        self.test_dataframe['response_header_size'] = pd.Series([100, 100, -1])
        self.test_dataframe['response_size'] = pd.Series([100, -1, 100])
        log_statistics = LogStatistics(self.test_dataframe)
        expected_amount_of_bytes = 400

        actual_amount_of_bytes = log_statistics.total_amount_of_bytes_exchanged()

        assert actual_amount_of_bytes == expected_amount_of_bytes

    def test_class_cannot_be_instantiated_with_empty_dataframe(self) -> None:
        empty_dataframe = pd.DataFrame()

        with pytest.raises(ValueError):
            LogStatistics(empty_dataframe)
