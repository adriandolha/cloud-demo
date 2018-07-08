import abc
import datetime
import json


class Encoder(json.JSONEncoder):
    """
    Handles specific encoding issues. E.g. datetime's ISO 8601 formats.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


class BaseSerializer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self, val):
        pass

    @abc.abstractmethod
    def decode(self, val):
        pass


class RestApiSerializer(BaseSerializer):
    """
    Serializes to and from json. The convention is to work with dicts.
    """

    def decode(self, val):
        return json.loads(val)

    def encode(self, val):
        return json.dumps(val, cls=Encoder)


class DynamoSerializer(BaseSerializer):
    """
    Handles dynamo serialization. E.g. datetime, where dynamo requires is0 8601 format.
    It works with dicts.
    """

    def decode(self, val):
        return val

    def encode(self, val):
        """
        Convert model dict to dynamo format. E.g. dynamo doesn't support datetime which should be converted to ISO 8601 format.
        :param val: Model dict
        :return: Formatted dict
        """
        target = {}
        model = val
        if not isinstance(val, dict):
            model = vars(val)
        for key in model:
            if hasattr(model, 'model'):
                target[key] = self.encode(model.model)
            else:
                _val = model[key]
                if isinstance(_val, datetime.datetime):
                    target[key] = _val.isoformat()
                else:
                    target[key] = _val
        return target


rest_api_serializer = RestApiSerializer()
dynamo_serializer = DynamoSerializer()


def to_json(val):
    return rest_api_serializer.encode(val)


def from_json(val):
    return rest_api_serializer.decode(val)


def to_dynamo(val):
    return dynamo_serializer.encode(val)


def from_dynamo(val):
    return dynamo_serializer.decode(val)
