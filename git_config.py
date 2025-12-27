from os.path import exists, join
import logging as log
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_file, ensure_files_owned_by_user


def get_git_config_backup_dir():
    return_val = join(get_macprefs_dir(), 'git_config/')
    ensure_exists(return_val)
    return return_val


def backup():
    log.info('Backing up git configuration...')
    home_dir = get_home_dir()
    dest = get_git_config_backup_dir()

    # Backup .gitconfig
    gitconfig = join(home_dir, '.gitconfig')
    if exists(gitconfig):
        copy_file(gitconfig, dest)
        log.debug('Backed up .gitconfig')
    else:
        log.info('No .gitconfig found... skipping.')

    # Backup .gitconfig.local if exists
    gitconfig_local = join(home_dir, '.gitconfig.local')
    if exists(gitconfig_local):
        copy_file(gitconfig_local, dest)
        log.debug('Backed up .gitconfig.local')

    # Backup .gitignore_global if exists
    gitignore_global = join(home_dir, '.gitignore_global')
    if exists(gitignore_global):
        copy_file(gitignore_global, dest)
        log.debug('Backed up .gitignore_global')


def restore():
    log.info('Restoring git configuration...')
    source = get_git_config_backup_dir()
    dest = get_home_dir()
    files_to_restore = []

    # Restore .gitconfig
    gitconfig = join(source, '.gitconfig')
    if exists(gitconfig):
        copy_file(gitconfig, dest)
        files_to_restore.append(join(dest, '.gitconfig'))
        log.debug('Restored .gitconfig')
    else:
        log.info('No .gitconfig backup found... skipping.')

    # Restore .gitconfig.local if exists
    gitconfig_local = join(source, '.gitconfig.local')
    if exists(gitconfig_local):
        copy_file(gitconfig_local, dest)
        files_to_restore.append(join(dest, '.gitconfig.local'))
        log.debug('Restored .gitconfig.local')

    # Restore .gitignore_global if exists
    gitignore_global = join(source, '.gitignore_global')
    if exists(gitignore_global):
        copy_file(gitignore_global, dest)
        files_to_restore.append(join(dest, '.gitignore_global'))
        log.debug('Restored .gitignore_global')

    # Ensure proper ownership
    if files_to_restore:
        ensure_files_owned_by_user(get_user(), files_to_restore)
