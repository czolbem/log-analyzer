from datetime import timedelta

import pandas as pd


class LogStatistics:
    """
    Statistics for logs that are stored in a Dataframe.

    Parameters:
        log_dataframe: Dataframe with log entries.
    Raises:
        ValueError: If the dataframe provided is empty (length 0).
    """

    def __init__(self, log_dataframe: pd.DataFrame):
        if len(log_dataframe) == 0:
            raise ValueError('LogStatistics cannot be instantiated with an empty dataframe.')
        self.log_dataframe = log_dataframe

    def most_frequent_ip(self) -> str:
        """
        Returns the most frequent (Client) IP.
        Note: There can be more than one IP with that property, in that case one IP is chosen.
        """
        return self.log_dataframe['client_ip'].value_counts().index[0]

    def least_frequent_ip(self) -> str:
        """
        Returns the least frequent (Client) IP.
        Note: There can be more than one IP with that property, in that case one IP is chosen.
        """
        return self.log_dataframe['client_ip'].value_counts().index[-1]

    def events_per_second(self) -> float:
        """
        Returns the average number of events per second.
        """
        number_of_events = len(self.log_dataframe)
        time_span: timedelta = self.log_dataframe['timestamp'].max() - self.log_dataframe['timestamp'].min()
        number_of_seconds = time_span.seconds
        return number_of_events / number_of_seconds

    def total_amount_of_bytes_exchanged(self) -> int:
        """
        Returns total amount of bytes exchanged by adding the sums of the header and response sizes.
        Note: A response size is only used in the sum if the size is positive. This is done because the response size
        can be -1 (e.g., when data is returned 'Chunked'). Adding entries with -1 to the sum would slightly taint the
        overall value.
        """
        total_sum_of_bytes_exchanged = (self.log_dataframe['response_header_size'].where(lambda size: size > 0).sum()
                                        + self.log_dataframe['response_size'].where(lambda size: size > 0).sum())
        return int(total_sum_of_bytes_exchanged)
