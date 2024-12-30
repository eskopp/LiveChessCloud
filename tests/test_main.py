from colorama import init, Fore, Style
import unittest
from click.testing import CliRunner
from LiveChessCloud.__init__ import main

# Initialize colorama
init(autoreset=True)

class TestLiveChessCloud(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(main, ['help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage:", result.output)

    def test_download_invalid_url(self):
        result = self.runner.invoke(main, ['download', 'invalid_url'])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error: Invalid URL format for download", result.output)

    def test_export_invalid_url(self):
        result = self.runner.invoke(main, ['export', 'invalid_url'])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error: Invalid URL format for export", result.output)

    def test_export_valid_url(self):
        # Replace with a valid URL for actual testing
        valid_url = "https://view.livechesscloud.com/#1eb49a34-ddb6-436a-b1bf-f4fc03c488d1"
        result = self.runner.invoke(main, ['export', valid_url, 'output.pgn'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Exporting game from URL:", result.output)
        self.assertIn("Export successful!", result.output)

if __name__ == "__main__":
    unittest.main()
