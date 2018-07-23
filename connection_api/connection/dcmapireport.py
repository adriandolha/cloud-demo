"""
This module contains any specifics for dcm connection. Similar modules should be added per connection case.
"""
from connection.domain import Connection


class DcmApiReportConnection(Connection):
    """
    This an example of how to add a specific connection. This class should handle specifics per connection case.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._profile_id = self.parameters['profile_id']
        if not self._profile_id:
            raise KeyError('profile_id')
        self._report_id = self.parameters['report_id']
        if not self._report_id:
            raise KeyError('report_id')

