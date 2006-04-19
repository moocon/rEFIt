#
# bin/mkefi.py
# Main script to build EFI binaries
#

import sys, os, os.path, shlex, glob
from optparse import OptionParser
import ConfigStore

### load configuration

config = ConfigStore.load_config()

if not config.has_key('arch'):
    print "ERROR: Not configured, please run mkefi-cfg.py."
    sys.exit(1)

arch       = config['arch']
efiversion = config['efiversion']
instpath   = config['instpath']
toolchain  = config['toolchain']

builddirname = ".obj-%s-%s" % (arch, toolchain)
libdirname   = "lib-%s-%s"  % (arch, toolchain)

### main entry point

def main():
    
    parser = OptionParser(usage="%prog command", version="%prog 0.1")
    parser.add_option("-f", "--file", dest="filename",
                      help="use FILE as the .mkefi description", metavar="FILE")
    #parser.add_option("-q", "--quiet",
    #                  action="store_false", dest="verbose", default=True,
    #                  help="don't print status messages to stdout")
    (options, args) = parser.parse_args()
    
    if options.filename is None:
        # search for an .mkefi file
        filenames = glob.glob("*.mkefi")
        if len(filenames) == 0:
            print "No .mkefi file found!"
            sys.exit(1)
        options.filename = filenames[0]
    
    spec = BuildSpec(options.filename)
    spec.build()

### BuildSpec class, represents a .mkefi file

class BuildSpec:
    
    def __init__(self, filename):
        self.filename = filename
        
        self.name = "a"
        self.bintype = "app"
        self.entrypoint = "efi_main"
        self.defines = [ "EFI32", "EFI_APP_110", "EFI_DEBUG", "CONFIG_%s" % arch ]
        self.includedirs = map_paths([ "%s/efi110/include" % instpath, "%s/efi110/include/%s" % (instpath, arch), "%s/efi110/include/protocol" % instpath ])
        self.libdirs = map_paths([ "%s/efi110/%s" % (instpath, libdirname) ])
        self.libs = [ "efi" ]
        self.sources = []
        
        self.read_spec()
        self.post_spec()
    
    def read_spec(self):
        f = open(self.filename, "r")
        lexer = shlex.shlex(f, self.filename)
        lexer.wordchars = lexer.wordchars + ".-/\\="
        lexer.whitespace = " \t"
        
        line = []
        while True:
            token = lexer.get_token()
            if token is None or token == "":
                break
            if token in "\r\n":
                if len(line) > 0:
                    self.process_line(line)
                line = []
            else:
                line.append(token)
        if len(line) > 0:
            self.process_line(line)
        
        f.close()
    
    def process_line(self, line):
        cmd = line[0]
        args = line[1:]

        if hasattr(self, "cmd_"+cmd):
            getattr(self, "cmd_"+cmd)(args)
        elif cmd == "source_"+arch:
            self.cmd_source(args)
        elif cmd[0:7] == "source_":
            pass
        else:
            print " Unknown command in %s: %s" % (self.filename, cmd)
    
    def cmd_name(self, args):
        # TODO: check that we have exactly one arg
        self.name = args[0]
    def cmd_type(self, args):
        # TODO: check that we have exactly one arg
        # TODO: check that the type is valid
        self.bintype = args[0]
    def cmd_entrypoint(self, args):
        # TODO: check that we have exactly one arg
        self.entrypoint = args[0]
    def cmd_define(self, args):
        self.defines.extend(args)
    def cmd_includedir(self, args):
        self.includedirs.extend(map_paths(args))
    def cmd_libdir(self, args):
        self.libdirs.extend(map_paths(args))
    def cmd_lib(self, args):
        self.libs.extend(args)
    def cmd_source(self, args):
        self.sources.extend(map_paths(args))
    
    def post_spec(self):
        if self.bintype == "lib":
            if self.name[0:3] != "lib":
                self.name = "lib"+self.name
    
    def build(self):
        # ensure ".obj" exists
        if not os.access(builddirname, os.F_OK):
            run_cmd("mkdir %s" % builddirname)
        
        # build all sources
        for source in self.sources:
            self.build_source(source)
        
        # build the final binary (or lib)
        objpaths = map(object_path, self.sources)
        if self.bintype == "lib":
            self.build_lib(objpaths)
        elif self.bintype == "app":
            self.build_app(objpaths)
        elif self.bintype == "bsdrv":
            self.build_bsdrv(objpaths)
        elif self.bintype == "rtdrv":
            self.build_rtdrv(objpaths)
        else:
            raise "Unsupported binary type '%s'" % self.bintype
    
    
    def build_source(self, srcpath):
        objpath = object_path(srcpath)
        # TODO: check if the object file is up-to-date
        
        print "*** %s -> %s" % (srcpath, objpath)
        
        if toolchain == "vc":
            cmd = "cl /nologo /W3 /Gm /Zi /O1 /GF /Gy /Gs8192 /QIfist"
            cmd = cmd + " /X"
            for define in self.defines:
                cmd = cmd + " /D %s" % define
            for includedir in self.includedirs:
                cmd = cmd + " /I %s" % includedir
            cmd = cmd + " /c %s /Fo%s /Fd%s\\" % (srcpath, objpath, builddirname)
            run_cmd(cmd)
        
        else:
            cmd = "gcc"
            if toolchain == "gcc-darwin":
                cmd = "gcc-4.0 -arch i386"
            cmd = cmd + " -O2 -fPIC -Wall -fshort-wchar -fno-strict-aliasing -fno-merge-constants -fasm-blocks"
            for define in self.defines:
                cmd = cmd + " -D%s" % define
            for includedir in self.includedirs:
                cmd = cmd + " -I%s" % includedir
            cmd = cmd + " -o %s -c %s" % (objpath, srcpath)
            run_cmd(cmd)
    
    
    def build_lib(self, objpaths):
        if toolchain == "vc":
            binpath = "%s.lib" % self.name
        else:
            binpath = "%s.a" % self.name
        print "*** -> %s" % binpath
        
        if toolchain == "vc":
            cmd = "lib /nologo"
            for objpath in objpaths:
                cmd = cmd + " %s" % objpath
            cmd = cmd + " /OUT:%s" % binpath
            run_cmd(cmd)
        
        else:
            cmd = "ar cq %s" % binpath
            for objpath in objpaths:
                cmd = cmd + " %s" % objpath
            run_cmd(cmd)
    
    
    def build_app(self, objpaths):
        binpath = "%s.efi" % self.name
        if toolchain == "vc":
            shobjpath = "%s.dll" % self.name
        else:
            shobjpath = "%s.so" % self.name
        shobjpath = os.path.join(builddirname, shobjpath)
        
        print "*** -> %s" % shobjpath
        if toolchain == "vc":
            cmd = "link /nologo /MACHINE:IX86 /subsystem:console /NODEFAULTLIB /INCREMENTAL:NO /MAP /DEBUG /opt:REF /DLL /ENTRY:%s" % self.entrypoint
            for libdir in self.libdirs:
                cmd = cmd + " /LIBPATH:%s" % libdir
            for objpath in objpaths:
                cmd = cmd + " %s" % objpath
            for lib in self.libs:
                cmd = cmd + " lib%s.lib" % lib
            cmd = cmd + " /OUT:%s" % shobjpath
            run_cmd(cmd)
        
        elif toolchain == "gcc-linux":
            cmd = "ld -nostdlib"
            # TODO: special flags for linux
            # TODO: additional glue code for (self.entrypoint != "efi_main")
            for libdir in self.libdirs:
                cmd = cmd + " -L%s" % libdir
            for objpath in objpaths:
                cmd = cmd + " %s" % objpath
            for lib in self.libs:
                cmd = cmd + " -l%s" % lib
            cmd = cmd + " -lgcc -o %s" % shobjpath
            run_cmd(cmd)
        
        elif toolchain == "gcc-darwin":
            cmd = "gcc-4.0 -arch i386 -nostdlib"
            for libdir in self.libdirs:
                cmd = cmd + " -L%s" % libdir
            for objpath in objpaths:
                cmd = cmd + " %s" % objpath
            for lib in self.libs:
                cmd = cmd + " -l%s" % lib
            cmd = cmd + " -lgcc -o %s" % shobjpath
            run_cmd(cmd)
        
        else:
            print "WARNING: Building binaries is not yet supported on this platform."
            return
        
        print "*** %s -> %s" % (shobjpath, binpath)
        if toolchain == "vc":
            cmd = "fwimage app %s %s" % (shobjpath, binpath)
            run_cmd(cmd)
        
        elif toolchain == "gcc-linux":
            cmd = "objcopy -j .text -j .sdata -j .data -j .dynamic -j .dynsym -j .rel -j .rela -j .reloc --target=FORMAT %s %s" % (shobjpath, binpath)
            run_cmd(cmd)
        
        else:
            print "WARNING: Building binaries is not yet supported on this platform."
            return
    
    
    def build_bsdrv(self, objpaths):
        raise "Building EFI drivers is not supported yet!"
    
    
    def build_rtdrv(self, objpaths):
        raise "Building EFI drivers is not supported yet!"



def run_cmd(cmd):
    print ">>> %s" % cmd
    
    retval = os.system(cmd)
    
    signal = retval % 128
    exitcode = retval / 256
    if signal != 0:
        raise "Killed by signal %d" % signal
    elif exitcode != 0:
        raise "Exit code %d" % exitcode

def map_paths(paths):
    return map(lambda path: os.path.normpath(path.replace("\\", "/")), paths)

def object_path(srcpath):
    objname = srcpath.replace("/", "_").replace("\\", "_")
    (objname, extension) = os.path.splitext(objname)
    if toolchain == "vc":
        objname = objname + ".obj"
    else:
        objname = objname + ".o"
    return os.path.join(builddirname, objname)


if __name__ == '__main__':
    main()

# EOF
