import pytest
from geoalchemy2 import WKBElement

from aegir.core import parsers


class TestGeojsonToWKT:
    @pytest.mark.parametrize('value, expected_value', (
        ({
          "type": "MultiPolygon",
          "coordinates": [
            [[[30, 20], [45, 40], [10, 40], [30, 20]]],
            [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
          ]
        },
         'MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), '
         '((15 5, 40 10, 10 20, 5 10, 15 5)))'
        ),
        ({
          "type": "Point",
          "coordinates": [-46.57421, -21.785741]
        },
         'POINT (-46.57421 -21.785741)'
        ),
    ))
    def test_must_parse_value(self, value, expected_value):
        assert parsers.geojson_to_wkt(value) == expected_value


class TestToGeojson:
    @pytest.mark.parametrize('element, expected_value', (
        (
            WKBElement('010600000002000000010300000001000000040000000000000000'
                       '003e40000000000000344000000000008046400000000000004440'
                       '000000000000244000000000000044400000000000003e40000000'
                       '0000003440010300000001000000050000000000000000002e4000'
                       '000000000014400000000000004440000000000000244000000000'
                       '000024400000000000003440000000000000144000000000000024'
                       '400000000000002e400000000000001440'),
            {
                'type': 'MultiPolygon', 'coordinates': [
                 (((30.0, 20.0), (45.0, 40.0), (10.0, 40.0), (30.0, 20.0)),),
                 (((15.0, 5.0), (40.0, 10.0), (10.0, 20.0), (5.0, 10.0),
                   (15.0, 5.0)),)]
            }
        ),
        (
            'MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), '
            '((15 5, 40 10, 10 20, 5 10, 15 5)))',
            {
                'type': 'MultiPolygon', 'coordinates': [
                    (((30.0, 20.0), (45.0, 40.0), (10.0, 40.0),
                      (30.0, 20.0)),),
                    (((15.0, 5.0), (40.0, 10.0), (10.0, 20.0), (5.0, 10.0),
                        (15.0, 5.0)),)]
            }
        ),
        (
            WKBElement('0101000000a18499b67f4947c058207a5226c935c0'),
            {
                "type": "Point",
                "coordinates": (-46.57421, -21.785741)
            }
        ),
        (
            'POINT (-46.57421 -21.785741)',
            {
                "type": "Point",
                "coordinates": (-46.57421, -21.785741)
            }
        ),
    ))
    def test_must_parse_element(self, element, expected_value):
        assert parsers.to_geojson(element) == expected_value
