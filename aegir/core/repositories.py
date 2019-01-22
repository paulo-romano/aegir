from aegir.core.models import Owner
from aegir.core.utils import log


class Repository:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.session.commit()
            log.debug('Work commited.')
        except Exception:
            log.exception('Error while commit work.')
            self.session.rollback()


class OwnerRepository(Repository):
    async def create(self, name, document):
        owner = Owner(name=name, document=document)
        self.session.add(owner)
        self.session.flush()
        return owner

    async def get_by_document(self, document):
        return self.session.query(Owner).filter_by(document=document).first()

    async def get_or_create_from_pdv_dict(self, pdv_dict):
        owner = await self.get_by_document(document=pdv_dict['document'])
        if not owner:
            owner = await self.create(
                pdv_dict['ownerName'], pdv_dict['document']
            )

        return owner
