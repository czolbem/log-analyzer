from io import StringIO

import pytest

from analyzer.analysis import LogAnalyzer


class TestLogAnalyzer:
    log_analyzer: LogAnalyzer

    @pytest.fixture(autouse=True)
    def setup_test(self) -> None:
        file1_content = """
        1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -
        1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html
        """
        file2_content = """
        1157689320.343   1357 10.105.21.199 TCP_REFRESH_HIT/304 214 GET http://www.goonernews.com/styles.css badeyek DIRECT/207.58.145.61 -
        """
        file1 = StringIO(file1_content)
        file2 = StringIO(file2_content)
        input_files = [file1, file2]
        output = StringIO()
        output.name = 'TestName'
        self.log_analyzer = LogAnalyzer(input_files=input_files, output=output, mfip=False, lfip=False, eps=False,
                                        bytes=False)

    def test_analyze_log_files_outputs_result_with_mfip_with_mfip_option(self) -> None:
        self.log_analyzer.mfip = True
        expected_output_key = 'mfip'

        self.log_analyzer.analyze_log_files()

        self.log_analyzer.output.seek(0)
        actual_output_content = self.log_analyzer.output.read()
        assert expected_output_key in actual_output_content

    def test_analyze_log_files_outputs_result_with_lfip_with_lfip_option(self) -> None:
        self.log_analyzer.lfip = True
        expected_output_key = 'lfip'

        self.log_analyzer.analyze_log_files()

        self.log_analyzer.output.seek(0)
        actual_output_content = self.log_analyzer.output.read()
        assert expected_output_key in actual_output_content

    def test_analyze_log_files_outputs_result_with_eps_with_eps_option(self) -> None:
        self.log_analyzer.eps = True
        expected_output_key = 'eps'

        self.log_analyzer.analyze_log_files()

        self.log_analyzer.output.seek(0)
        actual_output_content = self.log_analyzer.output.read()
        assert expected_output_key in actual_output_content

    def test_analyze_log_files_outputs_result_with_bytes_with_bytes_option(self) -> None:
        self.log_analyzer.bytes = True
        expected_output_key = 'bytes'

        self.log_analyzer.analyze_log_files()

        self.log_analyzer.output.seek(0)
        actual_output_content = self.log_analyzer.output.read()
        assert expected_output_key in actual_output_content

    def test_analyze_log_files_outputs_all_results_with_all_options(self) -> None:
        self.log_analyzer.mfip = True
        self.log_analyzer.lfip = True
        self.log_analyzer.eps = True
        self.log_analyzer.bytes = True

        self.log_analyzer.analyze_log_files()

        self.log_analyzer.output.seek(0)
        actual_output_content = self.log_analyzer.output.read()
        assert 'mfip' in actual_output_content
        assert 'lfip' in actual_output_content
        assert 'eps' in actual_output_content
        assert 'bytes' in actual_output_content

    def test_analyze_log_files_outputs_nothing_if_no_log_entries_are_available(self) -> None:
        self.log_analyzer.input_files = [StringIO()]
        expected_output_content = ''

        self.log_analyzer.analyze_log_files()

        self.log_analyzer.output.seek(0)
        actual_output_content = self.log_analyzer.output.read()
        assert expected_output_content == actual_output_content
