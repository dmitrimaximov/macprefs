from os.path import exists, join
import logging as log
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_file, ensure_files_owned_by_user, execute_shell


def get_vscode_backup_dir():
    return_val = join(get_macprefs_dir(), 'vscode/')
    ensure_exists(return_val)
    return return_val


def get_vscode_user_dir():
    return join(get_home_dir(), 'Library/Application Support/Code/User/')


def backup():
    log.info('Backing up VS Code settings...')
    source_dir = get_vscode_user_dir()

    if not exists(source_dir):
        log.info('VS Code settings directory not found... skipping.')
        return

    dest = get_vscode_backup_dir()

    # Backup settings.json
    settings_file = join(source_dir, 'settings.json')
    if exists(settings_file):
        copy_file(settings_file, dest)
        log.debug('Backed up settings.json')

    # Backup keybindings.json
    keybindings_file = join(source_dir, 'keybindings.json')
    if exists(keybindings_file):
        copy_file(keybindings_file, dest)
        log.debug('Backed up keybindings.json')

    # Backup snippets directory
    snippets_dir = join(source_dir, 'snippets/')
    if exists(snippets_dir):
        snippets_dest = join(dest, 'snippets/')
        ensure_exists(snippets_dest)
        execute_shell(['rsync', '-a', snippets_dir, snippets_dest])
        log.debug('Backed up snippets/')

    # Backup extensions list
    try:
        extensions = execute_shell(['code', '--list-extensions'], suppress_errors=True)
        extensions_file = join(dest, 'extensions.txt')
        with open(extensions_file, 'w') as f:
            f.write(extensions)
        log.debug('Backed up extensions list')
    except Exception as e:
        log.info('Could not backup VS Code extensions list: %s', str(e))


def restore():
    log.info('Restoring VS Code settings...')
    source = get_vscode_backup_dir()

    if not exists(source):
        log.info('No VS Code backup found... skipping.')
        return

    dest_dir = get_vscode_user_dir()
    ensure_exists(dest_dir)
    files_to_fix = []

    # Restore settings.json
    settings_source = join(source, 'settings.json')
    if exists(settings_source):
        settings_dest = join(dest_dir, 'settings.json')
        copy_file(settings_source, dest_dir)
        files_to_fix.append(settings_dest)
        log.debug('Restored settings.json')

    # Restore keybindings.json
    keybindings_source = join(source, 'keybindings.json')
    if exists(keybindings_source):
        keybindings_dest = join(dest_dir, 'keybindings.json')
        copy_file(keybindings_source, dest_dir)
        files_to_fix.append(keybindings_dest)
        log.debug('Restored keybindings.json')

    # Restore snippets directory
    snippets_source = join(source, 'snippets/')
    if exists(snippets_source):
        snippets_dest = join(dest_dir, 'snippets/')
        execute_shell(['rsync', '-a', snippets_source, dest_dir])
        log.debug('Restored snippets/')

    # Restore extensions (informational)
    extensions_file = join(source, 'extensions.txt')
    if exists(extensions_file):
        log.info('VS Code extensions list found at: %s', extensions_file)
        log.info('To install extensions, run:')
        log.info('  cat %s | xargs -L 1 code --install-extension', extensions_file)

    # Fix ownership
    if files_to_fix:
        ensure_files_owned_by_user(get_user(), files_to_fix)
