from os import path
import logging as log
from utils import copy_file, copy_dir, ensure_files_owned_by_user, execute_shell
from config import get_sys_preferences_backup_dir, ensure_exists


def backup():
    log.info('Backing up system preferences...')
    dest = get_sys_preferences_backup_dir()
    backed_up = []

    # Note: System-level preferences may require running with sudo
    # or Full Disk Access permissions for your terminal

    # Backup Power Management
    pm_source = get_pm_path()
    if path.exists(pm_source):
        try:
            execute_shell(['rsync', '-a', pm_source, dest], suppress_errors=True)
            log.debug('Backed up PowerManagement.plist')
            backed_up.append('PowerManagement')
        except Exception as e:
            log.debug('Could not backup PowerManagement.plist (may need sudo): %s', str(e))

    # List of important system-level preferences to backup
    system_prefs = [
        'com.apple.TimeMachine.plist',
        'com.apple.SoftwareUpdate.plist',
        'com.apple.Bluetooth.plist',
        'com.apple.NetworkSharing.plist',
    ]

    for pref_file in system_prefs:
        pref_path = path.join('/Library/Preferences/', pref_file)
        if path.exists(pref_path):
            try:
                execute_shell(['rsync', '-a', pref_path, dest], suppress_errors=True)
                log.debug('Backed up %s', pref_file)
                backed_up.append(pref_file)
            except Exception as e:
                log.debug('Could not backup %s (may need sudo): %s', pref_file, str(e))

    if not backed_up:
        log.info('Could not backup system preferences. Try running with sudo or ensure Full Disk Access is enabled.')


def restore():
    log.info('Restoring system preferences...')
    source = get_sys_preferences_backup_dir()

    if not path.exists(source):
        log.info('No system preferences backup found... skipping.')
        return

    # Restore Power Management
    pm_backup = path.join(source, 'com.apple.PowerManagement.plist')
    if path.exists(pm_backup):
        try:
            pm_dest = get_pm_path()
            execute_shell(['sudo', 'rsync', '-a', pm_backup, path.dirname(pm_dest) + '/'])
            ensure_files_owned_by_user('root:wheel', [pm_dest], '644')
            log.debug('Restored PowerManagement.plist')
        except Exception as e:
            log.warning('Could not restore PowerManagement.plist: %s', str(e))

    # List of important system-level preferences to restore
    system_prefs = [
        'com.apple.TimeMachine.plist',
        'com.apple.SoftwareUpdate.plist',
        'com.apple.Bluetooth.plist',
        'com.apple.NetworkSharing.plist',
    ]

    for pref_file in system_prefs:
        pref_backup = path.join(source, pref_file)
        if path.exists(pref_backup):
            try:
                pref_dest = path.join('/Library/Preferences/', pref_file)
                execute_shell(['sudo', 'rsync', '-a', pref_backup, '/Library/Preferences/'])
                ensure_files_owned_by_user('root:wheel', [pref_dest], '644')
                log.debug('Restored %s', pref_file)
            except Exception as e:
                log.debug('Could not restore %s: %s', pref_file, str(e))


def get_pm_path():
    pm_path = path.join('/Library/Preferences/', 'com.apple.PowerManagement.plist')
    if not path.exists(pm_path):
        pm_path = path.join('/Library/Preferences/SystemConfiguration/', 'com.apple.PowerManagement.plist')
    return pm_path
