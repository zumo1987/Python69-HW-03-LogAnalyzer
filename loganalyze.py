import unittest
import tempfile
import os

from loganalyze import analyze_user_activity


class TestAnalyzeUserActivity(unittest.TestCase):

    def create_log_file(self, content):
        file = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False
        )
        file.write(content)
        file.close()
        return file.name

    def test_normal_data(self):
        content = """\
2025-08-01T10:00:00 u001 login 120
2025-08-01T10:02:05 u002 login 200
2025-08-01T10:04:00 u001 view 0
2025-08-01T10:05:00 u002 view 100
2025-08-01T10:06:00 u002 submit 200
2025-08-01T10:07:00 u001 logout 120
2025-08-01T10:08:00 u002 logout 220
"""

        path = self.create_log_file(content)

        try:
            result = analyze_user_activity(path)

            self.assertEqual(result["total_users"], 2)

            self.assertEqual(
                result["action_counts"],
                {
                    "login": 2,
                    "view": 2,
                    "submit": 1,
                    "logout": 2
                }
            )

            self.assertEqual(result["most_active_user"], "u002")
            self.assertAlmostEqual(
                result["average_session_time"],
                137.14,
                places=2
            )

        finally:
            os.remove(path)

    def test_empty_file(self):
        path = self.create_log_file("")

        try:
            result = analyze_user_activity(path)

            self.assertEqual(result["total_users"], 0)
            self.assertEqual(result["action_counts"], {})
            self.assertIsNone(result["most_active_user"])
            self.assertEqual(result["average_session_time"], 0.0)

        finally:
            os.remove(path)

    def test_invalid_lines(self):
        content = """\
2025-08-01T10:00:00 u001 login 120
invalid line
2025-08-01T10:02:00 u002 login abc
2025-08-01T10:03:00 u001 view 50
2025-08-01T10:04:00
"""

        path = self.create_log_file(content)

        try:
            result = analyze_user_activity(path)

            self.assertEqual(result["total_users"], 1)

            self.assertEqual(
                result["action_counts"],
                {
                    "login": 1,
                    "view": 1
                }
            )

            self.assertEqual(result["most_active_user"], "u001")
            self.assertEqual(
                result["average_session_time"],
                85.0
            )

        finally:
            os.remove(path)

    def test_file_not_found(self):
        result = analyze_user_activity("not_found.log")

        self.assertEqual(result["total_users"], 0)
        self.assertEqual(result["action_counts"], {})
        self.assertIsNone(result["most_active_user"])
        self.assertEqual(result["average_session_time"], 0.0)


if __name__ == "__main__":
    unittest.main()
