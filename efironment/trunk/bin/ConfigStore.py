#
# bin/ConfigStore.py
# Common code for persistent configuration storage
#

import sys, os
import cPickle

if sys.platform == "win32":
    import _winreg


def load_config():
    state = {}

    if sys.platform == "win32":
        try:
            handle = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\efironment")
            (value, regtype) = _winreg.QueryValueEx(handle, "mkefistate")
            handle.Close()
            
            if regtype == _winreg.REG_BINARY:
                state = cPickle.loads(value)
            
        except:
            pass

    else:
        statepath = "%s/.mkefistate.%s" % (os.environ['HOME'], sys.platform)
        if os.access(statepath, os.R_OK):
            f = open(statepath, "rb")
            state = cPickle.load(f)
            f.close()

    return state


def save_config(state):
    if sys.platform == "win32":
        handle = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, "Software\\efironment")
        _winreg.SetValueEx(handle, "mkefistate", 0, _winreg.REG_BINARY, cPickle.dumps(state))
        handle.Close()

    else:
        statepath = "%s/.mkefistate.%s" % (os.environ['HOME'], sys.platform)
        f = open(statepath, "wb")
        cPickle.dump(state, f)
        f.close()


# EOF
