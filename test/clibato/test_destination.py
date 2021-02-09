import unittest
import clibato


class TestDestination(unittest.TestCase):
    def test_from_dict_with_repository_type(self):
        result = clibato.Destination.from_dict({
            'type': 'repository',
            'remote': 'git@github.com:jigarius/clibato.git'
        })

        expectation = clibato.destination.Repository({
            'type': 'repository',
            'remote': 'git@github.com:jigarius/clibato.git'
        })

        self.assertEqual(result, expectation)

    def test_from_dict_with_illegal_type(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Destination.from_dict({'type': 'foobar'})

        self.assertEqual(
            str(context.exception).strip("'"),
            'Illegal type: foobar'
        )

    def test_equality_operator(self):
        d1 = clibato.destination.Repository({
            'type': 'repository',
            'remote': 'git@github.com:jigarius/clibato.git'
        })

        d2 = clibato.destination.Repository({
            'type': 'repository',
            'remote': 'git@github.com:jigarius/clibato.git'
        })

        d3 = clibato.destination.Repository({
            'type': 'repository',
            'remote': 'git@github.com:jigarius/foobar.git'
        })

        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)
        self.assertNotEqual(d2, d3)
