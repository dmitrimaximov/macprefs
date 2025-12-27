from os.path import exists, join
import logging as log
from config import get_macprefs_dir, get_home_dir, ensure_exists
from utils import execute_shell, copy_file


def get_package_managers_backup_dir():
    return_val = join(get_macprefs_dir(), 'package_managers/')
    ensure_exists(return_val)
    return return_val


def backup():
    log.info('Backing up package manager lists...')
    dest = get_package_managers_backup_dir()

    # Backup Homebrew bundle
    try:
        log.debug('Creating Homebrew bundle...')
        brewfile_path = join(dest, 'Brewfile')
        execute_shell(['brew', 'bundle', 'dump', '--file=' + brewfile_path, '--force'])
        log.debug('Backed up Homebrew packages to Brewfile')
    except Exception as e:
        log.info('Could not backup Homebrew packages (brew may not be installed): %s', str(e))

    # Backup npm global packages
    try:
        log.debug('Listing npm global packages...')
        npm_list = execute_shell(['npm', 'list', '-g', '--depth=0', '--json'], suppress_errors=True)
        npm_file = join(dest, 'npm-global.json')
        with open(npm_file, 'w') as f:
            f.write(npm_list)
        log.debug('Backed up npm global packages')
    except Exception as e:
        log.info('Could not backup npm global packages (npm may not be installed): %s', str(e))

    # Backup asdf .tool-versions if exists
    tool_versions = join(get_home_dir(), '.tool-versions')
    if exists(tool_versions):
        copy_file(tool_versions, dest)
        log.debug('Backed up .tool-versions')

    # Backup other version manager configs
    for config_file in ['.nvmrc', '.node-version', '.python-version', '.ruby-version']:
        config_path = join(get_home_dir(), config_file)
        if exists(config_path):
            copy_file(config_path, dest)
            log.debug('Backed up %s', config_file)


def restore():
    log.info('Restoring package manager lists...')
    source = get_package_managers_backup_dir()

    # Restore Homebrew bundle
    brewfile = join(source, 'Brewfile')
    if exists(brewfile):
        try:
            log.info('Installing Homebrew packages from Brewfile...')
            log.info('This may take a while...')
            execute_shell(['brew', 'bundle', '--file=' + brewfile])
            log.debug('Restored Homebrew packages')
        except Exception as e:
            log.warning('Could not restore Homebrew packages: %s', str(e))
            log.info('You can manually run: brew bundle --file=%s', brewfile)
    else:
        log.info('No Brewfile backup found... skipping.')

    # Restore npm global packages (informational only - requires manual installation)
    npm_file = join(source, 'npm-global.json')
    if exists(npm_file):
        log.info('npm global packages backup found at: %s', npm_file)
        log.info('To restore npm packages, review the file and install manually.')

    # Restore .tool-versions
    tool_versions_source = join(source, '.tool-versions')
    if exists(tool_versions_source):
        tool_versions_dest = join(get_home_dir(), '.tool-versions')
        copy_file(tool_versions_source, get_home_dir())
        log.debug('Restored .tool-versions')

    # Restore other version manager configs
    home_dir = get_home_dir()
    for config_file in ['.nvmrc', '.node-version', '.python-version', '.ruby-version']:
        config_source = join(source, config_file)
        if exists(config_source):
            copy_file(config_source, home_dir)
            log.debug('Restored %s', config_file)
