import pytest

from aegir.core.models import Owner, PDV
from aegir.core.repositories import Repository, OwnerRepository, PDVRepository


class TestRepository:
    def test_must_set_session_on_init(self):
        fake_session = 'fake_session'
        repository = Repository(fake_session)
        assert repository.session == fake_session

    def test_must_return_self_on_dunder_enter(self, mocker):
        with Repository(mocker.MagicMock()) as repository:
            assert isinstance(repository, Repository) is True

    def test_must_commit_work_on_dunder_exit(
            self, mocker, mocked_sqlalchemy_session):
        mocked_log = mocker.patch('aegir.core.repositories.log')
        with Repository(mocked_sqlalchemy_session) as repository:
            assert isinstance(repository, Repository) is True

        assert mocked_sqlalchemy_session.commit.called is True
        assert mocked_log.debug.called is True
        assert mocker.call('Work commited.') in \
            mocked_log.debug.call_args_list

    def test_must_rollback_on_error(
            self, mocker, mocked_sqlalchemy_session):
        mocked_log = mocker.patch('aegir.core.repositories.log')
        mocked_sqlalchemy_session.commit.side_effect = Exception

        with Repository(mocked_sqlalchemy_session) as repository:
            assert isinstance(repository, Repository) is True

        assert mocked_log.exception.called is True
        assert mocker.call('Error while commit work.') in \
            mocked_log.exception.call_args_list
        assert mocked_sqlalchemy_session.rollback.called is True


class TestOwnerRepository:
    @pytest.mark.asyncio
    async def test_must_create_owner(
            self, mocker, mocked_sqlalchemy_session):
        owner_data = {
            'name': 'Test',
            'document': 'docteste',
        }

        mocker.patch('aegir.core.models.Owner', mocker.MagicMock())

        with OwnerRepository(mocked_sqlalchemy_session) as repo:
            await repo.create(**owner_data)

        assert mocked_sqlalchemy_session.add.called is True
        assert mocked_sqlalchemy_session.flush.called is True

    @pytest.mark.asyncio
    async def test_must_filter_by_document(
            self, mocker, mocked_sqlalchemy_session):
        document = 'doctest112'

        mocked_sqlalchemy_session.query = mocker.MagicMock()

        with OwnerRepository(mocked_sqlalchemy_session) as repo:
            await repo.get_by_document(document)

        assert mocked_sqlalchemy_session.query.called is True
        assert mocker.call(Owner) in \
            mocked_sqlalchemy_session.query.call_args_list
        assert mocked_sqlalchemy_session.query.return_value.filter_by.called \
            is True
        assert mocker.call(document=document) in \
            mocked_sqlalchemy_session.query.return_value.filter_by. \
            call_args_list

    @pytest.mark.asyncio
    async def test_get_or_create_from_pdv_dict_must_create(
            self, mocker, mocked_sqlalchemy_session, mocked_coroutine_factory):
        pdv_data = {
            'ownerName': 'Test',
            'document': 'docteste',
        }

        expected_owner = Owner(
            name=pdv_data['ownerName'], document=pdv_data['document']
        )

        mocker.patch(
            'aegir.core.repositories.OwnerRepository.get_by_document',
            mocked_coroutine_factory(None)
        )

        mocked_create = mocker.patch(
            'aegir.core.repositories.OwnerRepository.create',

            side_effect=mocked_coroutine_factory(expected_owner)
        )

        with OwnerRepository(mocked_sqlalchemy_session) as repo:
            owner = await repo.get_or_create_from_pdv_dict(pdv_data)

        assert owner == expected_owner
        assert mocked_create.called is True
        assert mocker.call(pdv_data['ownerName'], pdv_data['document']) in \
            mocked_create.call_args_list


class TestPDVRepository:
    @pytest.mark.asyncio
    async def test_must_create_pdv(
            self, mocker, mocked_sqlalchemy_session):
        mocked_owner = Owner(name='Test Owner', document='teste124')
        pdv_data = {
            'owner': mocked_owner,
            'name': 'Test',
            'coverage_area': {
                'type': 'MultiPolygon',
                'coordinates': [
                    [[[30, 20], [45, 40], [10, 40], [30, 20]]],
                    [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
                ]
            },
            'address': {
                'type': 'Point',
                'coordinates': [-46.57421, -21.785741]
            }
        }

        expected_pdv = PDV(**pdv_data)

        mocker.patch('aegir.core.models.PDV', mocker.MagicMock())

        mocker.patch.object(PDV, '__new__', return_value=expected_pdv)

        with PDVRepository(mocked_sqlalchemy_session) as repo:
            owner = await repo.create(**pdv_data)

        assert mocked_sqlalchemy_session.add.called is True
        assert mocker.call(expected_pdv) in \
            mocked_sqlalchemy_session.add.call_args_list
        assert mocked_sqlalchemy_session.flush.called is True
        assert owner == expected_pdv

    @pytest.mark.aaynxio
    async def test_must_get_instead_of_create(
            self, mocker, mocked_sqlalchemy_session, mocked_coroutine_factory):
        expected_pdv = PDV()

        mocker.patch(
            'aegir.core.repositories.PDVRepository'
            '.get_by_owner_and_name',
            mocked_coroutine_factory(expected_pdv)
        )

        mocked_create = mocker.patch(
            'aegir.core.repositories.PDVRepository.create',
        )

        with PDVRepository(mocked_sqlalchemy_session) as repo:
            pdv = await repo.get_or_create_from_pdv_dict(mocker.MagicMock())

        assert pdv == expected_pdv
        assert mocked_create.called is False

    @pytest.mark.asyncio
    async def test_must_filter_by_id(
            self, mocker, mocked_sqlalchemy_session):
        pdv_id = 'fakeidt112'

        mocked_sqlalchemy_session.query = mocker.MagicMock()

        with PDVRepository(mocked_sqlalchemy_session) as repo:
            await repo.get_by_id(pdv_id)

        assert mocked_sqlalchemy_session.query.called is True
        assert mocker.call(PDV) in \
            mocked_sqlalchemy_session.query.call_args_list
        assert mocked_sqlalchemy_session.query.return_value.filter_by.called \
            is True
        assert mocker.call(id=pdv_id) in \
            mocked_sqlalchemy_session.query.return_value.filter_by. \
            call_args_list
