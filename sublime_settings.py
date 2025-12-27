from os import listdir
from os.path import exists, join, isdir
import logging as log
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_dir, ensure_dir_owned_by_user


def get_sublime_backup_dir():
    return_val = join(get_macprefs_dir(), 'sublime/')
    ensure_exists(return_val)
    return return_val


def get_sublime_support_dir():
    return join(get_home_dir(), 'Library/Application Support/')


def backup():
    log.info('Backing up Sublime Text/Merge settings...')
    support_dir = get_sublime_support_dir()
    dest = get_sublime_backup_dir()
    backed_up = False

    # Find all Sublime Text versions
    try:
        all_dirs = listdir(support_dir)
        sublime_dirs = [d for d in all_dirs if d.startswith('Sublime Text') and isdir(join(support_dir, d))]
    except Exception as e:
        log.info('Could not list Application Support directory: %s', str(e))
        sublime_dirs = []

    # Backup Sublime Text settings
    for sublime_dir in sublime_dirs:
        sublime_path = join(support_dir, sublime_dir)
        user_path = join(sublime_path, 'Packages/User/')

        if exists(user_path):
            sublime_dest = join(dest, sublime_dir, 'Packages/User/')
            ensure_exists(sublime_dest)
            copy_dir(user_path, sublime_dest)
            log.debug('Backed up %s settings', sublime_dir)
            backed_up = True

    # Find all Sublime Merge versions
    try:
        all_dirs = listdir(support_dir)
        merge_dirs = [d for d in all_dirs if d.startswith('Sublime Merge') and isdir(join(support_dir, d))]
    except Exception as e:
        log.debug('Could not find Sublime Merge directories: %s', str(e))
        merge_dirs = []

    # Backup Sublime Merge settings
    for merge_dir in merge_dirs:
        merge_path = join(support_dir, merge_dir)
        user_path = join(merge_path, 'Packages/User/')

        if exists(user_path):
            merge_dest = join(dest, merge_dir, 'Packages/User/')
            ensure_exists(merge_dest)
            copy_dir(user_path, merge_dest)
            log.debug('Backed up %s settings', merge_dir)
            backed_up = True

    if not backed_up:
        log.info('No Sublime Text or Sublime Merge settings found... skipping.')


def restore():
    log.info('Restoring Sublime Text/Merge settings...')
    source = get_sublime_backup_dir()

    if not exists(source):
        log.info('No Sublime backup found... skipping.')
        return

    support_dir = get_sublime_support_dir()

    # Find all backed up Sublime directories
    try:
        backed_up_dirs = [d for d in listdir(source) if isdir(join(source, d))]
    except Exception as e:
        log.info('Could not list Sublime backup directories: %s', str(e))
        return

    for sublime_dir in backed_up_dirs:
        user_source = join(source, sublime_dir, 'Packages/User/')
        if exists(user_source):
            user_dest = join(support_dir, sublime_dir, 'Packages/User/')
            ensure_exists(join(support_dir, sublime_dir, 'Packages/'))
            copy_dir(user_source, user_dest, with_sudo=True)
            ensure_dir_owned_by_user(user_dest, get_user())
            log.debug('Restored %s settings', sublime_dir)

    log.info('Sublime settings restored. Restart Sublime Text/Merge to apply changes.')
