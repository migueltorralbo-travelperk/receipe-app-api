from django.test import TestCase
from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError

class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    @patch('django.db.utils.ConnectionHandler.__getitem__')
    def test_wait_for_db(self, gi, ts):
        """Test waiting for db"""
        gi.side_effect = [OperationalError] * 5 + [True]
        call_command('wait_for_db')
        self.assertEqual(gi.call_count, 6)

