"""
This module contains any specifics for dcm connector. Similar modules should be added per connector case.
"""
from connector.domain import Connector, validate_required_fields


class DcmConnector(Connector):
    """
    This an example of how to add a specific connector. This class should handle specifics per connector case.
    """

    def __init__(self, model):
        super().__init__(model)
        validate_required_fields(model, 'parameters')
        validate_required_fields(model['parameters'], 'profile_id', 'report_id')
