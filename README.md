# Clibato: CLI Backup Tool

Clibato is a simple backup/restore tool. I created it to help me backup
and restore my `.dot` files, and to have fun with Python 🐍.

>The name Clibato stands for (CLI) (ba)ckup (to)ol.

## Quick start

    pip install clibato # Installation
    clibato init --config-file=~/.clibato.yml
    vim ~/.clibato.yml # Configuration (required)
    clibato backup # Perform backup
    clibato restore # Restore last backup

## Installation

Clibato can easily be installed using [pip](https://pip.pypa.io/).

   pip install clibato

Once installed, you can run it as `clibato` or `python -m clibato`.

## Configuration

To use the tool, start by creating a configuration file. The `~/.clibato.yml`
will automatically be detected so, it is the recommended location. However,
you can place your configuration anywhere.

    clibato init --config-file=~/.clibato.yml

The generated file contains comments to help you with the configuration.

### Auto-detection

If `--config-file` is not specified, the following locations will be searched:

  - The directory from which the command was issued, i.e. `./.clibato.yml`.
  - The user's home directory, i.e. `~/.clibato.yml`.

If your configuration is not in one of those locations, you can use the
`--config-file` flag with other `clibato` commands.

### Suggestions

  * Place your config in `~/.clibato.yml`.
    * This way, you don't have to specify `--config-file` all the time.
  * Include your `.clibato.yml` in your backup.

## Usage

After you've installed and configured the tool, here's how you use it.

### Backup

To perform a backup, run the following command:

    clibato backup

### Restore

To restore the last backup, run the following command:

    clibato restore

## Examples

For detailed documentation, and more examples, see
[.clibato.example.yml](https://github.com/jigarius/clibato/blob/main/.clibato.example.yml).

### Backup to a directory

```yaml
contents:
  .bashrc:
  .clibato.yml:
destination:
  type: "directory"
  path: "~/backup/clibato"
```

### Backup to a Git repository

```yaml
contents:
  .bashrc:
  .clibato.yml:
destination:
  type: "repository"
  path: "~/backup/clibato"
  remote: "git@gitlab.com:jigarius/dotfiles.git"
  branch: 'main'
```
