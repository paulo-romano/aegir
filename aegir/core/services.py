from aegir.core.db import session
from aegir.core.repositories import PDVRepository


async def create_pdvs(pdvs):
    created = []
    for pdv in pdvs:
        with PDVRepository(session) as repository:
            pdv_object = await repository.get_or_create_from_pdv_dict(pdv)
            created.append(str(pdv_object.id))

    return created


async def get_pdv_by_id(pdv_id):
    with PDVRepository(session) as repository:
        pdv = await repository.get_by_id(pdv_id)

    return pdv
