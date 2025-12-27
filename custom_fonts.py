from os.path import exists, join
import logging as log
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_dir, ensure_dir_owned_by_user


def get_fonts_backup_dir():
    return_val = join(get_macprefs_dir(), 'fonts/')
    ensure_exists(return_val)
    return return_val


def get_user_fonts_dir():
    return join(get_home_dir(), 'Library/Fonts/')


def backup():
    log.info('Backing up custom fonts...')
    source = get_user_fonts_dir()

    if not exists(source):
        log.info('No user fonts directory found... skipping.')
        return

    dest = get_fonts_backup_dir()
    user_fonts_dest = join(dest, 'UserFonts/')
    ensure_exists(user_fonts_dest)

    copy_dir(source, user_fonts_dest)
    log.debug('Backed up ~/Library/Fonts/')


def restore():
    log.info('Restoring custom fonts...')
    source = get_fonts_backup_dir()
    user_fonts_source = join(source, 'UserFonts/')

    if not exists(user_fonts_source):
        log.info('No fonts backup found... skipping.')
        return

    dest = get_user_fonts_dir()
    copy_dir(user_fonts_source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, get_user())
    log.debug('Restored fonts to ~/Library/Fonts/')
    log.info('Font cache will be rebuilt automatically by the system.')
