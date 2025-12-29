from os import listdir
from os.path import exists, join, isdir
import logging as log
import re
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_dir, ensure_dir_owned_by_user


def get_jetbrains_backup_dir():
    return_val = join(get_macprefs_dir(), 'jetbrains/')
    ensure_exists(return_val)
    return return_val


def get_jetbrains_base_dir():
    return join(get_home_dir(), 'Library/Application Support/JetBrains/')


def parse_ide_version(ide_dir):
    """
    Parse IDE directory name to extract IDE name and version.
    Examples: IntelliJIdea2024.1 -> ('IntelliJIdea', '2024.1')
              PyCharm2023.3 -> ('PyCharm', '2023.3')
    """
    match = re.match(r'^([A-Za-z]+)(\d+(?:\.\d+)*)$', ide_dir)
    if match:
        return match.group(1), match.group(2)
    return None, None


def has_settings(ide_path):
    """
    Check if an IDE directory has actual settings (not empty/newly created).
    Returns True if any of the important settings directories exist.
    """
    important_dirs = ['keymaps', 'colors', 'codestyles', 'fileTemplates', 'templates', 'options', 'tools']
    for subdir in important_dirs:
        if exists(join(ide_path, subdir)):
            return True
    return False


def get_latest_ide_versions(base_dir, ide_dirs):
    """
    Given a list of IDE directories, return only the latest version of each IDE that has settings.
    """
    ide_versions = {}

    for ide_dir in ide_dirs:
        ide_name, version = parse_ide_version(ide_dir)
        if ide_name and version:
            ide_path = join(base_dir, ide_dir)
            # Only consider IDE directories that actually have settings
            if not has_settings(ide_path):
                log.debug('Skipping %s (no settings found)', ide_dir)
                continue

            # Convert version to tuple of integers for comparison (e.g., '2024.1' -> (2024, 1))
            try:
                version_tuple = tuple(int(x) for x in version.split('.'))
                if ide_name not in ide_versions or version_tuple > ide_versions[ide_name][1]:
                    ide_versions[ide_name] = (ide_dir, version_tuple)
            except ValueError:
                log.debug('Could not parse version for %s', ide_dir)

    # Return only the directory names of the latest versions
    return [info[0] for info in ide_versions.values()]


def backup():
    log.info('Backing up JetBrains settings...')
    base_dir = get_jetbrains_base_dir()

    if not exists(base_dir):
        log.info('JetBrains directory not found... skipping.')
        return

    dest = get_jetbrains_backup_dir()

    # Find all JetBrains IDE directories (e.g., IntelliJIdea2024.1, PyCharm2023.3, etc.)
    try:
        all_ide_dirs = [d for d in listdir(base_dir) if isdir(join(base_dir, d))]
    except Exception as e:
        log.info('Could not list JetBrains directories: %s', str(e))
        return

    if not all_ide_dirs:
        log.info('No JetBrains IDE configurations found... skipping.')
        return

    # Filter to only keep the latest version of each IDE that has settings
    ide_dirs = get_latest_ide_versions(base_dir, all_ide_dirs)

    if len(ide_dirs) < len(all_ide_dirs):
        log.info('Found %d IDE directories, backing up only %d latest versions',
                 len(all_ide_dirs), len(ide_dirs))

    for ide_dir in ide_dirs:
        ide_path = join(base_dir, ide_dir)
        ide_backup_path = join(dest, ide_dir + '/')
        ensure_exists(ide_backup_path)

        # Backup important subdirectories for each IDE
        important_dirs = [
            'keymaps',
            'colors',
            'codestyles',
            'fileTemplates',
            'templates',
            'options',
            'tools',
        ]

        backed_up = False
        for subdir in important_dirs:
            subdir_path = join(ide_path, subdir)
            if exists(subdir_path):
                subdir_dest = join(ide_backup_path, subdir + '/')
                ensure_exists(subdir_dest)
                copy_dir(subdir_path + '/', subdir_dest)
                log.debug('Backed up %s/%s', ide_dir, subdir)
                backed_up = True

        if backed_up:
            log.info('Backed up settings for %s', ide_dir)


def restore():
    log.info('Restoring JetBrains settings...')
    source = get_jetbrains_backup_dir()

    if not exists(source):
        log.info('No JetBrains backup found... skipping.')
        return

    base_dir = get_jetbrains_base_dir()
    ensure_exists(base_dir)

    # Find all backed up IDE directories
    try:
        ide_dirs = [d for d in listdir(source) if isdir(join(source, d))]
    except Exception as e:
        log.info('Could not list JetBrains backup directories: %s', str(e))
        return

    for ide_dir in ide_dirs:
        ide_source_path = join(source, ide_dir)
        ide_dest_path = join(base_dir, ide_dir)
        ensure_exists(ide_dest_path)

        # Restore all subdirectories
        try:
            subdirs = [d for d in listdir(ide_source_path) if isdir(join(ide_source_path, d))]
        except Exception as e:
            log.warning('Could not list subdirectories for %s: %s', ide_dir, str(e))
            continue

        for subdir in subdirs:
            subdir_source = join(ide_source_path, subdir + '/')
            subdir_dest = join(ide_dest_path, subdir + '/')
            copy_dir(subdir_source, subdir_dest, with_sudo=True)
            ensure_dir_owned_by_user(subdir_dest, get_user())
            log.debug('Restored %s/%s', ide_dir, subdir)

        log.info('Restored settings for %s', ide_dir)
