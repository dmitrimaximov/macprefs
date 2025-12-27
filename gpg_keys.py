from os.path import exists, join
import logging as log
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_dir, ensure_dir_owned_by_user


def get_gpg_backup_dir():
    return_val = join(get_macprefs_dir(), 'gnupg/')
    ensure_exists(return_val)
    return return_val


def backup():
    source = join(get_home_dir(), '.gnupg/')
    if not exists(source):
        log.info('No .gnupg dir found... skipping.')
        return
    log.info('Backing up GPG keys...')
    dest = get_gpg_backup_dir()
    copy_dir(source, dest)


def restore():
    source = get_gpg_backup_dir()
    if not exists(source):
        log.info('No .gnupg backup found... skipping.')
        return
    log.info('Restoring GPG keys...')
    dest = join(get_home_dir(), '.gnupg/')
    copy_dir(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, get_user(), mode='700')
