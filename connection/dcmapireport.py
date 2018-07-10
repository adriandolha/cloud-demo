"""
This module contains any specifics for dcm connection. Similar modules should be added per connection case.
"""
from connection.domain import Connection, validate_required_fields


class DcmApiReportConnection(Connection):
    """
    This an example of how to add a specific connection. This class should handle specifics per connection case.
    """

    def __init__(self, model):
        super().__init__(model)
        validate_required_fields(model, 'parameters')
        validate_required_fields(model['parameters'], 'profile_id', 'report_id')
