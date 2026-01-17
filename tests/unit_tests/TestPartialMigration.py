import unittest
from unittest.mock import MagicMock, patch

from src.ParsedMigrationItem import ParsedMigrationItem
from src.ciki import migrate_them_all
from src.repository.MigrationRepository import MigrationRepository
from tests.FakeUserMigrationFile import FakeUserMigrationFile


class TestPartialMigration(unittest.TestCase):
    @classmethod
    @patch("src.ciki.get_db_instance")
    def setUpClass(cls, get_db_instance_mock):
        get_db_instance_mock.return_value = None
        cls.prepare_mocks()

        try:
            migrate_them_all(cls.mock_repo, [cls.parsed1, cls.parsed2, cls.parsed3])
        except Exception:
            pass

    def test_repo_interaction(self):
        # Create called once
        self.mock_repo.create.assert_called_once()
        # Note: created_mig points to the mutable object which is modified later, so we check final state
        created_mig = self.mock_repo.create.call_args[0][0]
        self.assertEqual(len(created_mig.migration_items), 1)

        # Update should be called ONCE (for parsed2) before failure
        self.assertEqual(self.mock_repo.update_migration.call_count, 1)
        
        last_call_args = self.mock_repo.update_migration.call_args[0][0]
        self.assertEqual(last_call_args["migration_items"], ["02-b.py"])

    def test_parsed2_should_be_migrated(self):
        self.parsed2.migration.success.assert_called()

    def test_parsed3_should_be_attempted(self):
        # It IS called, but raises exception
        self.parsed3.migration.success.assert_called()

    @classmethod
    def prepare_mocks(cls):
        cls.mock_repo = MigrationRepository(cfg=MagicMock(), client=MagicMock())
        cls.mock_repo.create = MagicMock()
        cls.mock_repo.update_migration = MagicMock()
        cls.mock_repo.get_already_done_items = MagicMock(return_value=["01-a.py"])

        cls.parsed1 = ParsedMigrationItem(FakeUserMigrationFile(), "01-a.py", 1)
        cls.parsed1.migration.success = MagicMock()
        
        cls.parsed2 = ParsedMigrationItem(FakeUserMigrationFile(), "02-b.py", 2)
        cls.parsed2.migration.success = MagicMock()
        
        cls.parsed3 = ParsedMigrationItem(FakeUserMigrationFile(), "03-c.py", 3)
        # Simulate failure
        cls.parsed3.migration.success = MagicMock(side_effect=Exception("DB Error"))
