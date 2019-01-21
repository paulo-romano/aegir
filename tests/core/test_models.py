import pytest
from sqlalchemy.orm.attributes import InstrumentedAttribute

from aegir.core.models import Owner, PDV


class TestOwner:
    @pytest.mark.parametrize('key, expected_type', (
        ('id', InstrumentedAttribute),
        ('name', InstrumentedAttribute),
        ('document', InstrumentedAttribute),
    ))
    def test_must_have_attributes(self, key, expected_type):
        assert type(getattr(Owner, key)) == expected_type

    def test_must_convert_as_dict(self):
        owner_name = 'teste 123'
        owner_document = 'doc 3551'
        owner = Owner(name=owner_name, document=owner_document)

        assert owner.as_dict['ownerName'] == owner_name
        assert owner.as_dict['document'] == owner_document


class TestPDV:
    @pytest.mark.parametrize('key, expected_type', (
        ('id', InstrumentedAttribute),
        ('name', InstrumentedAttribute),
        ('owner', InstrumentedAttribute),
        ('address', InstrumentedAttribute),
        ('coverage_area', InstrumentedAttribute),
    ))
    def test_must_have_attributes(self, key, expected_type):
        assert type(getattr(PDV, key)) == expected_type
