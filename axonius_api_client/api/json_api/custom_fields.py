# -*- coding: utf-8 -*-
"""Models for API requests & responses."""
import dataclasses
import datetime
import typing as t

import dataclasses_json
import dateutil
import marshmallow
import marshmallow_jsonapi

from ...tools import coerce_bool, listify


class UnionField(marshmallow.fields.Field):
    """Field that deserializes multi-type input data to app-level objects."""

    def __init__(self, types: t.List[t.Type] = None, *args, **kwargs) -> None:
        """Pass."""
        super().__init__(*args, **kwargs)
        if types:
            self.types = listify(types)
        else:
            raise AttributeError("No types provided on union field")

    @property
    def types_str(self) -> str:
        """Pass."""
        return ", ".join([str(i) for i in self.types])

    def _deserialize(self, value, attr, data, **kwargs):
        if bool([isinstance(value, i) for i in self.types if isinstance(value, i)]):
            return value
        else:
            raise marshmallow.ValidationError(
                f"Field shoud be any of the following types: {self.types_str}"
            )


def load_date(value: t.Optional[t.Union[str, datetime.datetime]]) -> t.Optional[datetime.datetime]:
    """Pass."""
    if not isinstance(value, datetime.datetime):
        value = dateutil.parser.parse(value)

    if not value.tzinfo:
        value = value.replace(tzinfo=dateutil.tz.tzutc())
    return value


def dump_date(value: t.Optional[t.Union[str, datetime.datetime]]) -> t.Optional[str]:
    """Pass."""
    if isinstance(value, datetime.datetime):
        if not value.tzinfo:
            value = value.replace(tzinfo=dateutil.tz.tzutc())

        value = value.isoformat()

    return value


class SchemaBool(marshmallow_jsonapi.fields.Bool):
    """Support parsing boolean as strings/etc."""

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None and self.allow_none:
            return None

        try:
            return coerce_bool(value)
        except Exception as exc:
            raise marshmallow.ValidationError(str(exc))

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None and self.allow_none:
            return None

        try:
            return coerce_bool(value)
        except Exception as exc:
            raise marshmallow.ValidationError(str(exc))


class SchemaDatetime(marshmallow_jsonapi.fields.DateTime):
    """Field that deserializes multi-type input data to app-level objects."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None and self.allow_none:
            return None

        return dump_date(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None and self.allow_none:
            return None

        try:
            return load_date(value)
        except Exception as exc:
            raise marshmallow.ValidationError(str(exc))


class SchemaPassword(marshmallow_jsonapi.fields.Field):
    """Field that serializes to a string or an array and deserializes to a string or an array."""

    """
    This exists cuz:
        ["unchanged"]
    """

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value


def get_field_str_req(**kwargs):
    """Pass."""
    kwargs.setdefault("required", True)
    kwargs.setdefault("allow_none", False)
    kwargs.setdefault("validate", marshmallow.validate.Length(min=1))
    return marshmallow_jsonapi.fields.Str(**kwargs)


def get_field_dc_mm(mm_field: marshmallow.fields.Field, **kwargs) -> dataclasses.Field:
    """Pass."""
    kwargs["metadata"] = dataclasses_json.config(mm_field=mm_field)
    return dataclasses.field(**kwargs)


def get_schema_dc(schema: marshmallow.Schema, key: str, **kwargs) -> dataclasses.Field:
    """Pass."""
    kwargs["mm_field"] = schema._declared_fields[key]
    return get_field_dc_mm(**kwargs)


def validator_wrapper(fn: callable) -> callable:
    """Pass."""

    def validator(value):
        try:
            return fn(value=value)
        except Exception as exc:
            raise marshmallow.ValidationError(str(exc))

    return validator


# def get_field_oneof(
#     choices: List[str], field: Type[marshmallow.fields.Field] = marshmallow.fields.Str, **kwargs
# ) -> marshmallow.fields.Field:
#     """Pass."""
#     kwargs["validate"] = marshmallow.validate.OneOf(choices=choices)
#     kwargs.setdefault("required", True)
#     return field(**kwargs)
