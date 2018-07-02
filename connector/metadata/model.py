import datetime


class Metadata:
    def __init__(self, connector_id, client_id, account_id, data_source, user_id, report_id, profile_id, creation_date=None):
        self.connector_id = connector_id
        self.creation_date = datetime.datetime.utcnow()
        self.profile_id = profile_id
        self.report_id = report_id
        self.user_id = user_id
        self.data_source = data_source
        self.account_id = account_id
        self.client_id = client_id
