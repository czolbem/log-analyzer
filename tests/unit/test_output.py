import json
from io import StringIO

from analyzer.output import JSONWriter


class TestJSONWriter:
    def test_write_writes_results_as_json_string_to_output(self) -> None:
        output = StringIO()
        output.name = 'Test'
        results = {'testkey': 'testvalue'}
        expected_output_content = json.dumps(results)
        json_writer = JSONWriter(output=output, results=results)

        json_writer.write()

        output.seek(0)  # returning to start of stream
        actual_output_content = output.read()
        assert actual_output_content == expected_output_content
