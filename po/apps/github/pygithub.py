# XXX - jump through some hoops to import shadowed github module
import sys
orig_sys_path = sys.path
orig_module = sys.modules['github']
sys.path = filter(lambda p: '/po/apps' not in p, sys.path)
del sys.modules['github']
from github import *
sys.path = orig_sys_path
sys.modules['github'] = orig_module
