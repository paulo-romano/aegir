import click

from aegir.core.commands import shell


class TestShellCommand:
    def test_must_have_shell_command(self):
        shell_command = getattr(shell, 'shell')
        assert isinstance(shell_command, click.Command)
        assert shell_command.name == 'shell'
        assert shell_command.help == \
            'Execute a python interactive shell with Aegir context.'

    def test_load_command_must_rise_error(self, mocker):
        shell_command = getattr(shell, 'shell')
        mocked_embed = mocker.patch.object(shell, 'embed')

        shell_command.callback()

        assert mocked_embed.called
