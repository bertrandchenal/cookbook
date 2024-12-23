from pathlib import Path
import os
import platform


def cache_dir():
    '''
    Returns (and automatically creates) platform-specific cache
    directory
    '''
    system = platform.system()
    fallback = os.path.expanduser('~/.cache')
    if system == 'Windows':
        parent_dir = os.environ.get('LOCALAPPDATA', fallback)
    elif system == 'MacOS':
        parent_dir = os.path.expanduser('~/Library/Caches')
    else:
        parent_dir = os.environ.get('XDG_CACHE_HOME', fallback)
    parent_dir = Path(parent_dir)
    parent_dir.mkdir(exist_ok=True)
    res =  parent_dir/ 'singularity'
    res.mkdir(exist_ok=True)
    return res
