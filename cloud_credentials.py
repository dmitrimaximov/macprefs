from os.path import exists, join
import logging as log
from config import get_macprefs_dir, get_home_dir, get_user, ensure_exists
from utils import copy_dir, ensure_dir_owned_by_user


def get_cloud_credentials_backup_dir():
    return_val = join(get_macprefs_dir(), 'cloud_credentials/')
    ensure_exists(return_val)
    return return_val


def backup():
    log.info('Backing up cloud credentials...')
    home_dir = get_home_dir()
    dest = get_cloud_credentials_backup_dir()

    # Backup AWS credentials
    aws_dir = join(home_dir, '.aws/')
    if exists(aws_dir):
        aws_dest = join(dest, 'aws/')
        ensure_exists(aws_dest)
        copy_dir(aws_dir, aws_dest)
        log.debug('Backed up .aws/')
    else:
        log.debug('No .aws/ directory found... skipping.')

    # Backup Kubernetes config
    kube_dir = join(home_dir, '.kube/')
    if exists(kube_dir):
        kube_dest = join(dest, 'kube/')
        ensure_exists(kube_dest)
        copy_dir(kube_dir, kube_dest)
        log.debug('Backed up .kube/')
    else:
        log.debug('No .kube/ directory found... skipping.')

    # Backup Docker config
    docker_dir = join(home_dir, '.docker/')
    if exists(docker_dir):
        docker_dest = join(dest, 'docker/')
        ensure_exists(docker_dest)
        copy_dir(docker_dir, docker_dest)
        log.debug('Backed up .docker/')
    else:
        log.debug('No .docker/ directory found... skipping.')


def restore():
    log.info('Restoring cloud credentials...')
    source = get_cloud_credentials_backup_dir()
    home_dir = get_home_dir()

    # Restore AWS credentials
    aws_source = join(source, 'aws/')
    if exists(aws_source):
        aws_dest = join(home_dir, '.aws/')
        copy_dir(aws_source, aws_dest, with_sudo=True)
        ensure_dir_owned_by_user(aws_dest, get_user())
        log.debug('Restored .aws/')
    else:
        log.debug('No .aws/ backup found... skipping.')

    # Restore Kubernetes config
    kube_source = join(source, 'kube/')
    if exists(kube_source):
        kube_dest = join(home_dir, '.kube/')
        copy_dir(kube_source, kube_dest, with_sudo=True)
        ensure_dir_owned_by_user(kube_dest, get_user())
        log.debug('Restored .kube/')
    else:
        log.debug('No .kube/ backup found... skipping.')

    # Restore Docker config
    docker_source = join(source, 'docker/')
    if exists(docker_source):
        docker_dest = join(home_dir, '.docker/')
        copy_dir(docker_source, docker_dest, with_sudo=True)
        ensure_dir_owned_by_user(docker_dest, get_user())
        log.debug('Restored .docker/')
    else:
        log.debug('No .docker/ backup found... skipping.')
