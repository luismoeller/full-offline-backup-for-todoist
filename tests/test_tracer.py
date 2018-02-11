import unittest
from unittest.mock import patch
import io
from tracer import NullTracer, ConsoleTracer

class TestTracer(unittest.TestCase):
    def test_console_tracer_traces_to_console(self):
        # Arrange
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            tracer = ConsoleTracer()

            # Act
            tracer.trace("this is a string")

            # Assert
            self.assertEqual(mock_stdout.getvalue().strip(), "this is a string")

    def test_null_tracer_doesnt_trace_to_console(self):
        # Arrange
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            tracer = NullTracer()

            # Act
            tracer.trace("this is a string")

            # Assert
            self.assertEqual(mock_stdout.getvalue().strip(), "")