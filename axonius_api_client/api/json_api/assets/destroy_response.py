# -*- coding: utf-8 -*-
"""Models for API requests & responses."""
import dataclasses
import typing as t

from ..generic import Metadata, MetadataSchema


class DestroySchema(MetadataSchema):
    """Schema for response from destroying assets."""

    class Meta:
        """JSONAPI type."""

        type_ = "metadata_schema"

    @staticmethod
    def get_model_cls() -> t.Any:
        """Get the model for this schema."""
        return Destroy


SCHEMA = DestroySchema()


@dataclasses.dataclass
class Destroy(Metadata):
    """Model for response from destroying assets."""

    SCHEMA: t.ClassVar[t.Any] = SCHEMA

    @staticmethod
    def get_schema_cls() -> t.Any:
        """Get the schema for this model."""
        return DestroySchema
