from os.path import exists, join
import logging as log
from config import get_macprefs_dir, ensure_exists
from utils import execute_shell


def get_applications_backup_dir():
    return_val = join(get_macprefs_dir(), 'applications/')
    ensure_exists(return_val)
    return return_val


def backup():
    log.info('Backing up applications list...')
    dest = get_applications_backup_dir()

    # List all applications in /Applications
    try:
        log.debug('Listing applications in /Applications...')
        apps = execute_shell(['ls', '-1', '/Applications/'])
        apps_file = join(dest, 'Applications.txt')
        with open(apps_file, 'w') as f:
            f.write(apps)
        log.debug('Backed up /Applications list')
    except Exception as e:
        log.warning('Could not list /Applications: %s', str(e))

    # List user applications in ~/Applications
    try:
        log.debug('Listing applications in ~/Applications...')
        user_apps = execute_shell(['ls', '-1', join(get_home_dir(), 'Applications/')], suppress_errors=True)
        if user_apps:
            user_apps_file = join(dest, 'UserApplications.txt')
            with open(user_apps_file, 'w') as f:
                f.write(user_apps)
            log.debug('Backed up ~/Applications list')
    except Exception as e:
        log.debug('No ~/Applications directory or could not list it: %s', str(e))

    # List Mac App Store applications
    try:
        log.debug('Listing Mac App Store applications...')
        mas_apps = execute_shell(['mas', 'list'], suppress_errors=True)
        mas_file = join(dest, 'MasApplications.txt')
        with open(mas_file, 'w') as f:
            f.write(mas_apps)
        log.debug('Backed up Mac App Store applications')
    except Exception as e:
        log.info('Could not list Mac App Store applications (mas may not be installed): %s', str(e))


def restore():
    log.info('Applications list backup is informational only.')
    source = get_applications_backup_dir()

    apps_file = join(source, 'Applications.txt')
    user_apps_file = join(source, 'UserApplications.txt')
    mas_file = join(source, 'MasApplications.txt')

    if exists(apps_file):
        log.info('Applications list saved at: %s', apps_file)
    if exists(user_apps_file):
        log.info('User applications list saved at: %s', user_apps_file)
    if exists(mas_file):
        log.info('Mac App Store applications list saved at: %s', mas_file)
        log.info('To install Mac App Store apps, review the file and install manually.')
        log.info('Or use: mas install <app-id>')


def get_home_dir():
    from os import getenv
    return getenv('HOME') + '/'
