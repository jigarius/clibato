import unittest
import clibato


class TestDestination(unittest.TestCase):
    def test_new_not_allowed(self):
        with self.assertRaises(NotImplementedError) as context:
            clibato.Destination({'type': 'directory', 'path': '/tmp'})

        self.assertEqual(
            str(context.exception).strip("'"),
            f'Class not instantiable: {clibato.Destination.__name__}'
        )

    def test_new_without_type(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Directory({'path': '/tmp'})

        self.assertEqual(
            str(context.exception).strip("'"),
            'Key cannot be empty: type'
        )

    def test_from_dict_with_repository_type(self):
        result = clibato.Destination.from_dict({
            'type': 'repository',
            'path': 'git@github.com:jigarius/clibato.git'
        })

        expectation = clibato.destination.Repository({
            'type': 'repository',
            'path': 'git@github.com:jigarius/clibato.git'
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
            'path': 'git@github.com:jigarius/clibato.git'
        })

        d2 = clibato.destination.Repository({
            'type': 'repository',
            'path': 'git@github.com:jigarius/clibato.git'
        })

        d3 = clibato.destination.Repository({
            'type': 'repository',
            'path': 'git@github.com:bunny/wabbit.git'
        })

        d4 = clibato.destination.Directory({
            'type': 'directory',
            'path': '/tmp'
        })

        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)
        self.assertNotEqual(d2, d3)
        self.assertNotEqual(d1, d4)


class TestDirectory(unittest.TestCase):
    def test_path_is_required(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.destination.Directory({
                'type': 'directory',
                'path': ''
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            'Key cannot be empty: path'
        )

    def test_path_is_absolute(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.destination.Directory({
                'type': 'directory',
                'path': 'foo/bar'
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            'Path is not absolute: foo/bar'
        )

    def test_path_is_directory(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.destination.Directory({
                'type': 'directory',
                'path': '/tmp/foo'
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            'Path is not a directory: /tmp/foo'
        )

    @unittest.skip('TODO')
    def test_backup(self):
        pass

    @unittest.skip('TODO')
    def test_backup_file_not_found(self):
        pass

    @unittest.skip('TODO')
    def test_restore(self):
        pass

    @unittest.skip('TODO')
    def test_restore_file_not_found(self):
        pass


class TestRepository(unittest.TestCase):
    def test_path_is_required(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.destination.Repository({
                'type': 'repository',
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            'Key cannot be empty: path'
        )

    def test_default_values_merged(self):
        dest = clibato.destination.Repository({
            'type': 'repository',
            'path': 'git@github.com:jigarius/clibato.git'
        })

        self.assertEqual(
            dest.data(),
            {
                'type': 'repository',
                'path': 'git@github.com:jigarius/clibato.git',
                'branch': 'main',
                'user': {
                    'name': 'Clibato',
                    'mail': 'clibato@jigarius.com'
                }
            }
        )
