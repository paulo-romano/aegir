from aegir.core.models import Owner
from aegir.core.repositories import Repository, OwnerRepository


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
    @staticmethod
    def mock_owner(mocker, owner_data):
        expected_owner = Owner(**owner_data)

        mocked_owner_class = \
            mocker.patch('aegir.core.models.Owner', mocker.MagicMock())
        mocked_owner_class.__new__.return_value = expected_owner

        return mocked_owner_class, expected_owner

    async def test_must_create_owner(
            self, mocker, mocked_sqlalchemy_session):
        owner_data = {
            'name': 'Test',
            'document': 'docteste',
        }

        mocked_owner_class, expected_owner = self.mock_owner(owner_data)

        with OwnerRepository(mocked_sqlalchemy_session) as repo:
            owner = await repo.create(**owner_data)

        assert mocked_sqlalchemy_session.add.called is True
        assert mocker.call(expected_owner) in \
            mocked_sqlalchemy_session.add.call_args_list
        assert mocked_sqlalchemy_session.flush.called is True
        assert owner == expected_owner

    async def test_must_create_from_pdv_dict(
            self, mocker, mocked_sqlalchemy_session):
        pdv_data = {
            'ownerName': 'Test',
            'document': 'docteste',
        }

        expected_owner = 'expected_owner'

        mocked_create = mocker.patch.object(
            OwnerRepository, 'create', return_value=expected_owner
        )

        with OwnerRepository(mocked_sqlalchemy_session) as repo:
            owner = await repo.create_from_pdv_dict(pdv_data)

        assert owner == expected_owner
        assert mocked_create.called is True
        assert mocker.call(pdv_data['ownerName'], pdv_data['document']) in \
            mocked_create.call_args_list
