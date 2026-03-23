from __future__ import annotations
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import main  # noqa: E402


class HeartbeatSessionModeTests(unittest.TestCase):
    def test_normalize_heartbeat_session_mode(self):
        self.assertEqual(main._normalize_heartbeat_session_mode('auto'), 'auto')
        self.assertEqual(main._normalize_heartbeat_session_mode('fresh'), 'fresh')
        self.assertEqual(main._normalize_heartbeat_session_mode('force'), 'force')
        self.assertEqual(main._normalize_heartbeat_session_mode('restore'), 'restore')
        self.assertEqual(main._normalize_heartbeat_session_mode('AUTO'), 'auto')
        self.assertEqual(main._normalize_heartbeat_session_mode('unknown'), 'restore')
        self.assertEqual(main._normalize_heartbeat_session_mode(None), 'restore')

    def test_extract_context_left_percent_prefers_latest_match(self):
        output = (
            '... 43% context left\n'
            '... some more text\n'
            '... 18% context left\n'
        )
        self.assertEqual(main._extract_context_left_percent(output, launcher='codex'), 18)

    def test_extract_context_left_percent_handles_missing_values(self):
        self.assertIsNone(main._extract_context_left_percent('no context marker here', launcher='codex'))
        self.assertIsNone(main._extract_context_left_percent('999% context left', launcher='codex'))

    def test_extract_context_left_percent_respects_provider_patterns(self):
        output = '18% context left'
        self.assertEqual(main._extract_context_left_percent(output, launcher='codex'), 18)
        self.assertEqual(main._extract_context_left_percent(output, launcher='unknown-cli'), 18)

    def test_heartbeat_handoff_saved_detection(self):
        temp_root = Path(tempfile.mkdtemp(prefix='hb-handoff-'))
        try:
            handoff_file = temp_root / 'handoff.md'
            handoff_file.write_text('- Status: pending\n', encoding='utf-8')
            self.assertFalse(main._heartbeat_handoff_saved(handoff_file))

            handoff_file.write_text('- Status: saved\n## Next Action\n- run', encoding='utf-8')
            self.assertTrue(main._heartbeat_handoff_saved(handoff_file))

            handoff_file.write_text('\n'.join(['line'] * 40), encoding='utf-8')
            self.assertTrue(main._heartbeat_handoff_saved(handoff_file))
        finally:
            shutil.rmtree(temp_root, ignore_errors=True)

    def test_should_rollover_heartbeat_session(self):
        self.assertTrue(main._should_rollover_heartbeat_session('fresh', None))
        self.assertTrue(main._should_rollover_heartbeat_session('auto', 24))
        self.assertFalse(main._should_rollover_heartbeat_session('auto', 25))
        self.assertFalse(main._should_rollover_heartbeat_session('auto', None))
        self.assertFalse(main._should_rollover_heartbeat_session('restore', 1))


if __name__ == '__main__':
    unittest.main()
