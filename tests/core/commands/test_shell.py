import click
import pytest

from aegir.core.commands import shell
from aegir.core.commands.shell import get_user_ns, get_banners
from aegir.core.db import session
from aegir.core.models import Owner, PDV


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

    @pytest.mark.parametrize('name, expected_value', (
        ('session', session),
        ('Owner', Owner),
        ('PDV', PDV),
    ))
    def test_must_pre_import_some_aegir_objects(self, name, expected_value):
        assert get_user_ns()[name] == expected_value

    @pytest.mark.parametrize('key', (get_user_ns().keys()))
    def test_must_show_available_objects_in_banner2(self, key):
        assert get_banners()['banner2'].find(key) >= 0
