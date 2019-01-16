import click

from aegir.core.commands import db


class TestDBGroup:
    def test_must_have_pdvs_group_command(self):
        db_group = getattr(db, 'db')
        assert isinstance(db_group, click.Group)
        assert db_group.name == 'db'
        assert db_group.help == 'Database related commands.'


class TestCreateCommand:
    def test_must_have_create_command(self):
        create_command = getattr(db, 'create')
        assert isinstance(create_command, click.Command)
        assert create_command.name == 'create'

    def test_must_be_listed_on_group(self):
        db_group = getattr(db, 'db')
        create_command = getattr(db, 'create')
        assert db_group.commands['create'] == create_command

    def test_create_command_must_call_function(self, mocker):
        create_command = getattr(db, 'create')

        create_database = \
            mocker.patch.object(db, 'create_database')
        create_database_extensions = \
            mocker.patch.object(db, 'create_database_extensions')
        create_all = mocker.patch('sqlalchemy.sql.schema.MetaData.create_all')
        create_command.callback()
        assert create_database.called is True
        assert create_database_extensions.called is True
        assert create_all.called is True
