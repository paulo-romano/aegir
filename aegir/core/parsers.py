from shapely import geometry, wkt
from geoalchemy2.shape import to_shape


def geojson_to_wkt(value):
    """Parse geojson element to WKT."""
    return geometry.shape(value).wkt


def to_geojson(element):
    """Parse WKT or WKB to geojson element."""
    try:
        element_wkt = to_shape(element).wkt
    except Exception:
        element_wkt = element

    return geometry.mapping(
        wkt.loads(
            element_wkt
        )
    )
