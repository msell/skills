import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/skills"


class AgentInstallationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "repo"
        self.home = self.root / "home"
        self.script = self.repo / "scripts/skills"
        self.script.parent.mkdir(parents=True)
        shutil.copy2(SCRIPT, self.script)
        self.source = self.repo / "agents/example.md"
        self.source.parent.mkdir()
        self.source.write_text(
            "---\nname: example\ndescription: Example agent.\n---\nOriginal instructions.\n",
            encoding="utf-8",
        )
        self.claude_target = self.home / ".claude/agents/example.md"
        self.codex_target = self.home / ".codex/agents/example.toml"

    def run_command(self, command="link-agents", *options):
        return subprocess.run(
            [sys.executable, str(self.script), command, "--home", str(self.home), *options],
            capture_output=True,
            text=True,
        )

    def assert_rejected(self, result):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_dangling_codex_symlink_does_not_create_its_target(self):
        outside = self.root / "outside.toml"
        self.codex_target.parent.mkdir(parents=True)
        self.codex_target.symlink_to(outside)

        result = self.run_command()

        self.assert_rejected(result)
        self.assertFalse(outside.exists())
        self.assertTrue(self.codex_target.is_symlink())
        self.assertFalse(self.claude_target.parent.exists())

    def test_codex_symlink_does_not_overwrite_a_generated_file(self):
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        outside = self.root / "outside.toml"
        self.codex_target.rename(outside)
        original = outside.read_bytes()
        self.codex_target.symlink_to(outside)
        self.source.write_text(
            self.source.read_text(encoding="utf-8").replace("Original", "Updated"),
            encoding="utf-8",
        )

        result = self.run_command()

        self.assert_rejected(result)
        self.assertEqual(outside.read_bytes(), original)
        self.assertTrue(self.codex_target.is_symlink())

    def test_agent_directory_cannot_redirect_into_checkout(self):
        for provider in (".claude", ".codex"):
            with self.subTest(provider=provider):
                home = self.root / provider
                redirect = self.repo / provider
                redirect.mkdir()
                destination = home / provider / "agents"
                destination.parent.mkdir(parents=True)
                destination.symlink_to(redirect, target_is_directory=True)
                result = subprocess.run(
                    [sys.executable, str(self.script), "link-agents", "--home", str(home)],
                    capture_output=True,
                    text=True,
                )

                self.assert_rejected(result)
                self.assertEqual(list(redirect.iterdir()), [])
                other_provider = ".codex" if provider == ".claude" else ".claude"
                self.assertFalse((home / other_provider).exists())

    def test_symlinked_parent_cannot_redirect_into_checkout(self):
        self.home.mkdir()
        (self.home / ".codex").symlink_to(self.repo, target_is_directory=True)

        result = self.run_command()

        self.assert_rejected(result)
        self.assertFalse((self.repo / "agents/example.toml").exists())
        self.assertFalse(self.claude_target.parent.exists())

    def test_unlink_rejects_checkout_destination_before_removing_any_agents(self):
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        generated = self.codex_target.read_bytes()
        self.codex_target.unlink()
        self.codex_target.parent.rmdir()
        protected = self.repo / "protected"
        protected.mkdir()
        protected_target = protected / "example.toml"
        protected_target.write_bytes(generated)
        self.codex_target.parent.symlink_to(protected, target_is_directory=True)

        result = self.run_command("unlink-agents")

        self.assert_rejected(result)
        self.assertEqual(protected_target.read_bytes(), generated)
        self.assertTrue(self.claude_target.is_symlink())

    def test_install_update_and_uninstall_in_real_directories(self):
        for _ in range(2):
            result = self.run_command()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.claude_target.resolve(), self.source.resolve())
            self.assertFalse(self.codex_target.is_symlink())
            self.assertIn("Original instructions.", self.codex_target.read_text())

        self.source.write_text(
            self.source.read_text(encoding="utf-8").replace("Original", "Updated"),
            encoding="utf-8",
        )
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Updated instructions.", self.codex_target.read_text())

        result = self.run_command("unlink-agents")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.claude_target.is_symlink())
        self.assertFalse(self.codex_target.exists())
        self.assertTrue(self.source.exists())

    def test_dry_run_does_not_create_destinations(self):
        result = self.run_command("link-agents", "--dry-run")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.home.exists())


if __name__ == "__main__":
    unittest.main()
