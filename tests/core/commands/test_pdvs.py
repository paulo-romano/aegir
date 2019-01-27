import click

from aegir.core.commands import pdvs


class TestPDVSGroup:
    def test_must_have_pdvs_group_command(self):
        pdvs_group = getattr(pdvs, 'pdvs')
        assert isinstance(pdvs_group, click.Group)
        assert pdvs_group.name == 'pdvs'
        assert pdvs_group.help == 'PDVs related commands.'


class TestLoadCommand:
    def test_must_have_load_command(self):
        load_command = getattr(pdvs, 'load')
        assert isinstance(load_command, click.Command)
        assert load_command.name == 'load'

    def test_must_be_listed_on_group(self):
        pdvs_group = getattr(pdvs, 'pdvs')
        load_command = getattr(pdvs, 'load')
        assert pdvs_group.commands['load'] == load_command
