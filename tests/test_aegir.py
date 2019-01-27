import aegir


class TestInit:
    def test_must_expose_aegir_commands(self):
        __all__ = getattr(aegir, '__all__')
        assert 'aegir_commands' in __all__
