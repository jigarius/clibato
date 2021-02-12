import os
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

    def test_from_dict_with_valid_type(self):
        dest = clibato.Destination.from_dict({
            'type': 'directory',
            'path': '/tmp'
        })

        self.assertEqual(
            dest,
            clibato.destination.Directory({
                'type': 'directory',
                'path': '/tmp'
            })
        )

    def test_from_dict_with_illegal_type(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Destination.from_dict({'type': 'foobar'})

        self.assertEqual(
            str(context.exception).strip("'"),
            'Illegal type: foobar'
        )

    def test_equality_operator(self):
        subject = clibato.destination.Directory({
            'type': 'directory',
            'path': '/tmp',
        })

        self.assertEqual(
            subject,
            clibato.destination.Directory({
                'type': 'directory',
                'path': '/tmp'
            })
        )

        self.assertNotEqual(
            subject,
            clibato.destination.Directory({
                'type': 'directory',
                'path': '/var/www'
            })
        )

        self.assertNotEqual(
            subject,
            clibato.destination.Repository({
                'type': 'repository',
                'path': '/tmp',
                'remote': 'git@github.com:bunny/wabbit.git'
            })
        )


class TestDirectory(unittest.TestCase):
    def test_new(self):
        dest = clibato.destination.Directory({
            'type': 'directory',
            'path': '/tmp'
        })

        self.assertEqual(
            dest.data(),
            {
                'type': 'directory',
                'path': '/tmp'
            }
        )

    def test_inheritance(self):
        self.assertTrue(issubclass(
            clibato.destination.Directory,
            clibato.destination.Destination
        ))

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

    def test_path_is_tilde(self):
        subject = clibato.destination.Directory({
            'type': 'directory',
            'path': '~/backup'
        })

        self.assertEqual(
            subject.data(),
            {
                'type': 'directory',
                'path': os.path.expanduser('~/backup')
            }
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
    def test_new(self):
        subject = clibato.destination.Repository({
            'type': 'repository',
            'path': '/tmp',
            'remote': 'git@github.com:jigarius/clibato.git',
            'branch': 'backup',
            'user': {
                'name': 'Jigarius',
                'mail': 'jigarius@example.com',
            }
        })

        self.assertEqual(
            subject.data(),
            {
                'type': 'repository',
                'path': '/tmp',
                'remote': 'git@github.com:jigarius/clibato.git',
                'branch': 'backup',
                'user': {
                    'name': 'Jigarius',
                    'mail': 'jigarius@example.com',
                }
            }
        )

    def test_inheritance(self):
        self.assertTrue(issubclass(
            clibato.destination.Repository,
            clibato.destination.Directory
        ))

    def test_path_is_required(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.destination.Repository({
                'type': 'repository',
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            'Key cannot be empty: path'
        )

    def test_remote_is_required(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.destination.Repository({
                'type': 'repository',
                'path': '/tmp',
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            'Key cannot be empty: remote'
        )

    def test_default_values_merged(self):
        dest = clibato.destination.Repository({
            'type': 'repository',
            'path': '/tmp',
            'remote': 'git@github.com:jigarius/clibato.git'
        })

        self.assertEqual(
            dest.data(),
            {
                'type': 'repository',
                'path': '/tmp',
                'remote': 'git@github.com:jigarius/clibato.git',
                'branch': 'main',
                'user': {
                    'name': 'Clibato',
                    'mail': 'clibato@jigarius.com'
                }
            }
        )
