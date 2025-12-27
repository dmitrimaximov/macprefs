from os.path import exists, join, isfile
import logging as log
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_file, copy_dir, ensure_files_owned_by_user, ensure_dir_owned_by_user


def get_env_configs_backup_dir():
    return_val = join(get_macprefs_dir(), 'env_configs/')
    ensure_exists(return_val)
    return return_val


def backup():
    log.info('Backing up environment configs...')
    home_dir = get_home_dir()
    dest = get_env_configs_backup_dir()

    # List of individual config files to backup
    config_files = [
        '.aliases',
        '.exports',
        '.env',
        '.functions',
        '.path',
        '.extra',
    ]

    for config_file in config_files:
        file_path = join(home_dir, config_file)
        if exists(file_path) and isfile(file_path):
            copy_file(file_path, dest)
            log.debug('Backed up %s', config_file)

    # Backup .config directory (selective)
    config_dir = join(home_dir, '.config/')
    if exists(config_dir):
        config_backup_dir = join(dest, 'config/')
        ensure_exists(config_backup_dir)

        # Backup important directories from .config
        important_configs = ['direnv', 'gh', 'starship.toml', 'bat', 'htop']

        for config_name in important_configs:
            config_path = join(config_dir, config_name)
            if exists(config_path):
                if isfile(config_path):
                    copy_file(config_path, config_backup_dir)
                    log.debug('Backed up .config/%s', config_name)
                else:
                    config_dest = join(config_backup_dir, config_name + '/')
                    ensure_exists(config_dest)
                    copy_dir(config_path + '/', config_dest)
                    log.debug('Backed up .config/%s/', config_name)


def restore():
    log.info('Restoring environment configs...')
    source = get_env_configs_backup_dir()
    home_dir = get_home_dir()
    files_to_fix = []

    # List of individual config files to restore
    config_files = [
        '.aliases',
        '.exports',
        '.env',
        '.functions',
        '.path',
        '.extra',
    ]

    for config_file in config_files:
        file_source = join(source, config_file)
        if exists(file_source):
            copy_file(file_source, home_dir)
            files_to_fix.append(join(home_dir, config_file))
            log.debug('Restored %s', config_file)

    # Restore .config directory
    config_backup_dir = join(source, 'config/')
    if exists(config_backup_dir):
        config_dest_dir = join(home_dir, '.config/')
        ensure_exists(config_dest_dir)

        # Restore backed up configs
        important_configs = ['direnv', 'gh', 'starship.toml', 'bat', 'htop']

        for config_name in important_configs:
            config_source = join(config_backup_dir, config_name)
            if exists(config_source):
                if isfile(config_source):
                    copy_file(config_source, config_dest_dir)
                    files_to_fix.append(join(config_dest_dir, config_name))
                    log.debug('Restored .config/%s', config_name)
                else:
                    config_final_dest = join(config_dest_dir, config_name + '/')
                    copy_dir(config_source + '/', config_final_dest, with_sudo=True)
                    ensure_dir_owned_by_user(config_final_dest, get_user())
                    log.debug('Restored .config/%s/', config_name)

    # Fix ownership of files
    if files_to_fix:
        ensure_files_owned_by_user(get_user(), files_to_fix)
