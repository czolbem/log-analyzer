import os
import shutil
import sys

import pytest

from analyzer import main

RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources')
FILE1 = os.path.join(RESOURCE_DIRECTORY, 'access1.log')
FILE2 = os.path.join(RESOURCE_DIRECTORY, 'access2.log')


class TestMain:
    @pytest.fixture(scope="session")
    def tmp_file(self, tmp_path_factory):
        tmp_dir = tmp_path_factory.mktemp('tmp')
        path = os.path.join(tmp_dir, 'output.json')
        yield path
        shutil.rmtree(tmp_dir)

    def test_log_analyzer_outputs_correct_statistics_for_provided_log_files(self, tmp_file) -> None:
        sys.argv = [FILE1, FILE2, '--mfip', '--lfip', '--eps', '--bytes', '--output', tmp_file]
        expected_output_content = '{"mfip": "10.105.21.199", "lfip": "10.105.37.58", "eps": 1.0, "bytes": 307475}'

        main()

        with open(tmp_file) as output_file:
            actual_output_content = output_file.read()
        assert actual_output_content == expected_output_content
