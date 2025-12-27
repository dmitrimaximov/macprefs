from os.path import exists, join
import logging as log
from config import get_macprefs_dir, ensure_exists
from utils import execute_shell


def get_runtime_versions_backup_dir():
    return_val = join(get_macprefs_dir(), 'runtime_versions/')
    ensure_exists(return_val)
    return return_val


def backup():
    log.info('Backing up runtime versions...')
    dest = get_runtime_versions_backup_dir()
    versions_info = []

    # Check .NET version
    try:
        log.debug('Checking dotnet version...')
        dotnet_version = execute_shell(['dotnet', '--version'], suppress_errors=True)
        if dotnet_version:
            versions_info.append(f"dotnet: {dotnet_version.strip()}")

            # List all installed SDKs
            dotnet_sdks = execute_shell(['dotnet', '--list-sdks'], suppress_errors=True)
            if dotnet_sdks:
                dotnet_file = join(dest, 'dotnet-sdks.txt')
                with open(dotnet_file, 'w') as f:
                    f.write(dotnet_sdks)
                log.debug('Backed up dotnet SDKs list')

            # List all installed runtimes
            dotnet_runtimes = execute_shell(['dotnet', '--list-runtimes'], suppress_errors=True)
            if dotnet_runtimes:
                dotnet_runtime_file = join(dest, 'dotnet-runtimes.txt')
                with open(dotnet_runtime_file, 'w') as f:
                    f.write(dotnet_runtimes)
                log.debug('Backed up dotnet runtimes list')
    except Exception as e:
        log.info('dotnet not found or could not check version: %s', str(e))
        versions_info.append('dotnet: not installed')

    # Check Node.js version
    try:
        log.debug('Checking node version...')
        node_version = execute_shell(['node', '--version'], suppress_errors=True)
        if node_version:
            versions_info.append(f"node: {node_version.strip()}")
            log.debug('Backed up node version')
    except Exception as e:
        log.info('node not found or could not check version: %s', str(e))
        versions_info.append('node: not installed')

    # Check npm version
    try:
        log.debug('Checking npm version...')
        npm_version = execute_shell(['npm', '--version'], suppress_errors=True)
        if npm_version:
            versions_info.append(f"npm: {npm_version.strip()}")
            log.debug('Backed up npm version')
    except Exception as e:
        log.info('npm not found or could not check version: %s', str(e))
        versions_info.append('npm: not installed')

    # Check Python version
    try:
        log.debug('Checking python version...')
        python_version = execute_shell(['python3', '--version'], suppress_errors=True)
        if python_version:
            versions_info.append(f"python3: {python_version.strip()}")
            log.debug('Backed up python version')
    except Exception as e:
        log.debug('python3 not found: %s', str(e))
        versions_info.append('python3: not installed')

    # Check Ruby version
    try:
        log.debug('Checking ruby version...')
        ruby_version = execute_shell(['ruby', '--version'], suppress_errors=True)
        if ruby_version:
            versions_info.append(f"ruby: {ruby_version.strip()}")
            log.debug('Backed up ruby version')
    except Exception as e:
        log.debug('ruby not found: %s', str(e))
        versions_info.append('ruby: not installed')

    # Check Go version
    try:
        log.debug('Checking go version...')
        go_version = execute_shell(['go', 'version'], suppress_errors=True)
        if go_version:
            versions_info.append(f"go: {go_version.strip()}")
            log.debug('Backed up go version')
    except Exception as e:
        log.debug('go not found: %s', str(e))

    # Write versions summary
    versions_file = join(dest, 'versions.txt')
    with open(versions_file, 'w') as f:
        f.write('\n'.join(versions_info))
    log.info('Backed up runtime versions to %s', versions_file)


def restore():
    log.info('Runtime versions backup is informational only.')
    source = get_runtime_versions_backup_dir()

    versions_file = join(source, 'versions.txt')
    dotnet_file = join(source, 'dotnet-sdks.txt')
    dotnet_runtime_file = join(source, 'dotnet-runtimes.txt')

    if exists(versions_file):
        log.info('\nRuntime versions from backup:')
        with open(versions_file, 'r') as f:
            for line in f:
                log.info('  %s', line.strip())

    if exists(dotnet_file):
        log.info('\n.NET SDKs list saved at: %s', dotnet_file)
        log.info('To install .NET SDKs, visit: https://dotnet.microsoft.com/download')

    if exists(dotnet_runtime_file):
        log.info('.NET Runtimes list saved at: %s', dotnet_runtime_file)

    log.info('\nFor node/npm versions, use nvm, asdf, or package_managers module.')
