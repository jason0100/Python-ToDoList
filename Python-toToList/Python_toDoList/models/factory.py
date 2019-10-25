"""
Factory for the different types of repositories.
"""

def create_repository(name, setting):
    if name == 'mongodb':
        from .mongodb import Repository
    elif name== 'memory':
         from .memory import Repository
    else:
        raise ValueError('Unknown repository.')
    return Repository(setting)