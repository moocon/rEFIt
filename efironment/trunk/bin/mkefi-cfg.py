#
# bin/mkefi-cfg.py
# Configuration script for mkefi
#

import sys, os, os.path
import ConfigStore


def main():
    
    config = {}
    
    # detect platform
    
    if sys.platform == "win32":
        config['toolchain'] = "vc"
        config['vcversion'] = "2003"    # TODO: autodetect!
    
    elif sys.platform == "linux2":
        config['toolchain'] = "gcc-linux"
    
    elif sys.platform == "darwin":
        config['toolchain'] = "gcc-darwin"
    
    else:
        print "ERROR: Platform '%s' not recognized." % sys.platform
        return
    
    # other defaults
    
    config['arch'] = "ia32"
    config['efiversion'] = "efi110"
    
    # installation path
    
    path = os.getcwd()
    (path, dirname) = os.path.split(path)
    if os.access(os.path.join(path, "efi110"), os.R_OK):
        config['instpath'] = path
    else:
        print "ERROR: Cannot determine installation directory."
        return
    
    # save to persistent storage
    
    ConfigStore.save_config(config)
    
    # generate mkefi.bat on Windows
    
    if sys.platform == "win32":
        mkefibatpath = os.path.join(os.path.join(config['instpath'], "bin"), "mkefi.bat")
        f = open("%s.in" % mkefibatpath, "rb")
        script = f.read()
        f.close()
        
        script = script.replace("@INSTPATH@", config['instpath'])
        
        f = open(mkefibatpath, "wb")
        f.write(script)
        f.close()


if __name__ == '__main__':
    main()

# EOF
