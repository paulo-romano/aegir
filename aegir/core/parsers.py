from shapely import geometry, wkt
from geoalchemy2.shape import to_shape


async def geojson_to_wtk(value):
    return geometry.shape(value).wkt


async def wkb_to_geojson(element):
    return geometry.mapping(
        wkt.loads(
            to_shape(element).wkt
        )
    )
