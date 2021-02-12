# Clibato: CLI Backup Tool

Clibato helps is a simple backup/restore tool. I created it with the intention
of backing up my `dot` files (and to have fun with Python).

## Installation

TODO.

## Usage

After you've installed the tool, here's how you use it.

### Configuration

Create a `.clibato.yml` file based on [.clibato.example.yml](clibato.example.yml).
When you run `clibato`, you can specify a config file as follows:

    clibato --config-file=/path/to/.clibato.yml ...

If a `--config-file` is not specified, Clibato will look for a config file in
the following directories:

  - The directory from which the command was issued, i.e. `./.clibato.yml`.
  - The user's home directory, i.e. `~/.clibato.yml`.

Since I use clibato to back up my dot-files, I put it in my home directory.
That way, I don't have to specify a `--config-file` all the time.

Additionally, you can include your `.clibato.yml` file in your backup.

### Backup

To perform a backup, run the following command:

    clibato backup

### Restore

To restore files from a backup, run the following command:

    clibato restore
