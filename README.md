# Clibato: CLI Backup Tool

Clibato is a simple backup/restore tool. I created it to help me backup
my `.dot` files and to have fun with Python 🐍.

## Installation

TODO.

## Usage

After you've installed the tool, here's how you use it.

### Configuration

To use the tool, start by creating a configuration file. The `~/.clibato.yml`
will automatically be detected so, it is the recommended location. However,
you can place your configuration anywhere.

    clibato init --config-file=~/.clibato.yml

The generated file contains comments to help you with the configuration.

#### Auto-detection

If `--config-file` is not specified, the following locations will be searched:

  - The directory from which the command was issued, i.e. `./.clibato.yml`.
  - The user's home directory, i.e. `~/.clibato.yml`.

If your configuration is not in one of those locations, you can use the
`--config-file` flag with other `clibato` commands.

#### Tips

  * Place your config in `~/.clibato.yml`.
    * This way, you don't have to specify `--config-file` all the time.
  * Include your `.clibato.yml` in your backup.

### Backup

To perform a backup, run the following command:

    clibato backup

### Restore

To restore the previous backup, run the following command:

    clibato restore
