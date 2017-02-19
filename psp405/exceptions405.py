class Permissions(Exception):
    '''Useful when program is run with no root privileges'''
    pass
class NoPortParam(Exception):
    '''Useful when no parameter has been given
    to the PSP405() class for its port serial connection'''
    pass
