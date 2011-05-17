'''
Created on Nov 27, 2010

@author: Marco Antonio Islas Cruz
'''

import distutils
import py2exe
import subprocess
import os
import shutil

#working directory
WDIR = os.getcwd()
split = WDIR.split(os.path.sep)
drive = os.path.splitdrive(WDIR)[0]
rpath = drive + "\\\\" + os.path.join(*split[1:-2])
print rpath
GITDIR = r"%s"%rpath
print (GITDIR,)
try:
    shutil.rmtree(GITDIR)
except Exception, e:
    print "Error removign %s: %s"%(GITDIR,repr(e))

#===============================================================================
# if os.path.exists(GITDIR):
#    os.rmdir(GITDIR)
# try:
#    os.mkdir(GITDIR)
# except:
#    pass
#===============================================================================
os.system("chmod -R 777 %s"%GITDIR)
#Get the libw32 files from git
#cmd = 'git clone git://github.com/markuz/w32settings_manager.git "%s"'%GITDIR
#print cmd
#gitprocess = subprocess.Popen(cmd, shell=True,
#                            stdin=subprocess.PIPE,
#                            cwd=WDIR)
#gitprocess.wait()
#Copy everything from libw32s to the current directory.

def copy_directory(dir):
    def procfnames(elements, dirname, fnames):
        elements.extend(map(lambda fname: os.path.join(dirname, fname), fnames))
    elements = []
    os.path.walk(dir, procfnames, elements)
    if not elements:
        return
    return elements
     
for i in ('win32app','libw32s','win32settings_app.py'):
    cpath = os.path.join(GITDIR,i)
    print "cpath", cpath
    if os.path.isfile(cpath):
        try:
            os.makedirs(os.path.split(cpath)[0])
        except Exception, e:
            print e
        shutil.copy(cpath, os.path.join(WDIR, i))
        continue
    elements = copy_directory(cpath)
    for element in elements:
        if element.find('build_win32') > -1:
            #Skip build_win32 
            continue
        directory, file = os.path.split(element)
        try:
            os.makedirs(directory)
        except Exception, e:
            print e
        print "Copying %s -> %s"%(cpath,WDIR)
        shutil.copy(element, os.path.join(WDIR, element))

def getFiles(dir):
    """
    Retorna una tupla de tuplas del directorio
    """
    # dig looking for files
    a= os.walk(dir)
    b = True
    filenames = []

    while (b):
        try: 
            (dirpath, dirnames, files) = a.next()
            filenames.append([dirpath, tuple(files)])
        except:
            b = False
    return filenames


origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    dlls = ("msvcp71.dll", "dwmapi.dll", "jpeg62.dll","mfc71.dll")
    if os.path.basename(pathname).lower() in dlls:
        return 0
    return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

class Target:
    def __init__(self,**kw):
            self.__dict__.update(kw)
            self.author = 'Marco Antonio Islas Islas'
            self.maintainer = 'Marco Antonio Islas Cruz'
            self.maintainer_email = 'markuz@islascruz.org'
            self.url='http://www.islascruz.org'
            self.classifiers=[
                  'Development Status :: 3 - Alpha',
                  'Environment :: Console',
                  'Intended Audience :: End Users/Desktop',
                  'License :: OSI Approved :: GNU/GPL v.2.0',
                  'Operating System :: Microsoft :: Windows',
                  'Programming Language :: Python',
                  ]
            self.platforms = ['Windows 2000', 'Windows XP','Windows Vista','Windows 7']
            self.version        = "0.1.0"
            self.compay_name    = "w32settings manager project"
            self.copyright      = "(c) 2010, Marco Islas"
            self.name           = "Win32 Settings Manager service"
            self.description = 'Keeps trac of several configurations and apply them to the system.'
            self.icon_resources =  [(0, "win32resources/icon.ico")]

target = Target(script = "win32settings_app.py")

setup(
    windows = [target],
    #Useful for debuggin?, I don't know, but if you want you can use the
    #sources.
    #console = [target],
    options = {
                  'py2exe': {
                      'packages':'encodings,libw32s',
                      'includes': 'cairo, pango, pangocairo, atk, gobject, gio',
                      'optimize': 0,
                      'excludes':'doctest,pdb,unittest,difflib,inspect',
                      'compressed': 0,
                      'skip_archive':1,
                      'unbuffered':True,
                  }
              },

    #data_files=[("gui", glob.glob("gui/*.*")),
    #            ("gui/pixmaps",glob.glob("gui/pixmaps/*.*")),
    #],
    #ext_modules=[CLibraryModel,]#,ChristineGtkBuilder],
)




# Create installer
# Requires NSIS to be installed and in the system PATH
print "Building the installer"

program_info = {
        'program_name':'w32settings_manager',
        'exe_name':'win32app',
        'full_product_name': 'Win32 Settings Manager',
        'version':PROGRAM_VERSION,
        'release_name':'',
        'publisher':'islascruz.org',
        }

build_script = file("win32settings_mananger.nsh").read()
build_script = build_script % program_info
header_file = file("_win32settings_mananger.nsh", "w")
header_file.write(build_script)
header_file.close()

print "Building installer..."
build_script = file("win32settings_manager.nsi").read()
# Dynamically insert details into the build script.
build_script = build_script % program_info
makensis = subprocess.Popen("makensis.exe -", shell=True,
                            stdin=subprocess.PIPE,
                            cwd=WDIR)
makensis.communicate(build_script)

