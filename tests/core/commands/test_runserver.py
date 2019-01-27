import click

from aegir.core.commands import runserver


class TestRunserverCommand:
    def test_must_have_runserver_command(self):
        runserver_command = getattr(runserver, 'runserver')
        assert isinstance(runserver_command, click.Command)
        assert runserver_command.name == 'runserver'
        assert runserver_command.help == \
            'Execute Aegir server.'
