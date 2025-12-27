from os.path import exists, join
import logging as log
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_dir, copy_file, ensure_dir_owned_by_user


def get_alfred_backup_dir():
    return_val = join(get_macprefs_dir(), 'alfred/')
    ensure_exists(return_val)
    return return_val


def get_alfred_support_dir():
    return join(get_home_dir(), 'Library/Application Support/Alfred/')


def get_alfred_preferences_dir():
    return join(get_home_dir(), 'Library/Preferences/')


def backup():
    log.info('Backing up Alfred settings...')

    # Backup Alfred Application Support directory
    alfred_support = get_alfred_support_dir()
    if exists(alfred_support):
        dest = get_alfred_backup_dir()
        alfred_dest = join(dest, 'ApplicationSupport/')
        ensure_exists(alfred_dest)
        copy_dir(alfred_support, alfred_dest)
        log.debug('Backed up Alfred Application Support')
    else:
        log.info('Alfred Application Support directory not found... skipping.')
        return

    # Backup Alfred preferences plist
    prefs_dir = get_alfred_preferences_dir()
    alfred_plist = join(prefs_dir, 'com.runningwithcrayons.Alfred.plist')
    if exists(alfred_plist):
        dest = get_alfred_backup_dir()
        copy_file(alfred_plist, dest)
        log.debug('Backed up Alfred preferences')


def restore():
    log.info('Restoring Alfred settings...')
    source = get_alfred_backup_dir()

    if not exists(source):
        log.info('No Alfred backup found... skipping.')
        return

    # Restore Alfred Application Support
    alfred_source = join(source, 'ApplicationSupport/')
    if exists(alfred_source):
        alfred_dest = get_alfred_support_dir()
        copy_dir(alfred_source, alfred_dest, with_sudo=True)
        ensure_dir_owned_by_user(alfred_dest, get_user())
        log.debug('Restored Alfred Application Support')

    # Restore Alfred preferences plist
    alfred_plist_source = join(source, 'com.runningwithcrayons.Alfred.plist')
    if exists(alfred_plist_source):
        prefs_dir = get_alfred_preferences_dir()
        copy_file(alfred_plist_source, prefs_dir)
        log.debug('Restored Alfred preferences')
        log.info('Alfred settings restored. You may need to restart Alfred.')
