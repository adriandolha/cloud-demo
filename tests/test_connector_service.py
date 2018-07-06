import json

from connector import aws, make_repo
from connector import domain


class TestConnectorService:
    def test_repo_is_cached(self, model_valid, mock_ddb_table):
        assert make_repo() == make_repo()
