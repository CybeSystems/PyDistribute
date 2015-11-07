import os, sys, glob, subprocess, platform, compileall, shutil, distutils

scriptpath = os.path.realpath(os.path.dirname(sys.argv[0])).replace('/','\\')
scriptpathParentFolder = os.path.dirname(scriptpath)
sys.path.insert(0, os.path.join(scriptpath, 'lib'))

###################################################################################################
# Functions
#

from copy import deepcopy
def dict_merge(a, b):
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

def run_command(command):
    if isinstance(command, list):
        print("Runnning Shell command: " + ' '.join(command))
        command = ' '.join(command)
    else:
        print("Runnning Shell command: " + command)
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE,stderr=sys.stdout.buffer)
    #process = subprocess.Popen(command, env=dict(os.environ, PATH="C:\\Python34"), shell=False, stdout=subprocess.PIPE,stderr=sys.stdout.buffer)
    #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print (output.strip().decode('utf-8'))

def runCommandWithPath(command, path, includeSysPath = True):
    if isinstance(command, list):
        print("Runnning Shell command: " + ' '.join(command))
        command = ' '.join(command)
    else:
        print("Runnning Shell command: " + command)

    commandEnviron= {}
    if includeSysPath:
        commandEnviron = os.environ
        commandEnviron["PATH"] = path + ";" + os.environ["PATH"]
        #We need to alternate the APPDATA Path -> Nuitka is searching for depends.exe in AppData\\Roaming
        # It searches for zip file NOT for binaries (e.g. C:\Users\USERNAME\AppData\Roaming\nuitka\depends22_x86.zip
        commandEnviron["APPDATA"] = scriptpath + "\\Runtime"
    else:
        commandEnviron["PATH"] = path
    #commandEnviron["PYTHONPATH"] = path
    print(commandEnviron["PATH"])

    process = subprocess.Popen(command, env=commandEnviron, shell=True, stdout=subprocess.PIPE,stderr=sys.stdout.buffer)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print (output.strip().decode('utf-8'))

def quoteParameter(parameter):
    return "\"" + parameter + "\""

def quoteFolder(folder, relative = False):
    folder = folder.replace("/","\\")
    return "\"" + folder + "\""

def remove_file_extension(path,extension):
    for root, _, files in os.walk(path):
        for afile in files:
            fullpath = os.path.join(root, afile)
            if os.path.splitext(afile)[1] == extension:
                print("removing", fullpath)
                os.remove(fullpath)

def remove_folder(path,pathToDelete):
    for curdir, dirs, files in os.walk(path):
        for d in dirs:
            if d.startswith(pathToDelete):
                shutil.rmtree(os.path.join(curdir, d))


def silentremove(filename):
    try:
        os.remove(filename)
    except:
        pass

def getNsisFlags(config, consoleMode=False):
    flags=[]
    flags.append(config["buildConfig"]["cyDistributePath"] + '\\Runtime\\NSIS\\makensis.exe')
    flags.append('/DFileIcon=' + quoteParameter(config["buildConfig"]['appIcon']))
    flags.append('/DPythonVersion=' + config["nsisConfig"]['PythonVersion'])

    flags.append('/DProductName=' + quoteParameter(config["nsisConfig"]['ProductName']))
    flags.append('/DComments=' + quoteParameter(config["nsisConfig"]['Comments']))
    flags.append('/DCompanyName=' + quoteParameter(config["nsisConfig"]['CompanyName']))
    flags.append('/DLegalCopyright=' + quoteParameter(config["nsisConfig"]['LegalCopyright']))
    flags.append('/DFileDescription=' + quoteParameter(config["nsisConfig"]['FileDescription']))
    flags.append('/DFileVersion=' + config["nsisConfig"]['FileVersion'])
    flags.append('/DProductVersion=' + config["nsisConfig"]['ProductVersion'])
    flags.append('/DInternalName=' + quoteParameter(config["nsisConfig"]['InternalName']))
    flags.append('/DLegalTrademarks=' + quoteParameter(config["nsisConfig"]['LegalTrademarks']))
    flags.append('/DOriginalFilename=' + quoteParameter(config["nsisConfig"]['OriginalFilename']))
    flags.append('/DPrivateBuild=' + quoteParameter(config["nsisConfig"]['PrivateBuild']))
    flags.append('/DSpecialBuild=' + quoteParameter(config["nsisConfig"]['SpecialBuild']))
    flags.append('/DPyStartFile=' + config["buildConfig"]['startFile'])
    if config["buildConfig"]["pythonCustomInterpreter"]:
        flags.append('/DInterpreter=' + config["buildConfig"]["pythonExeName"])
        flags.append('/DInterpreterW=' + config["buildConfig"]["pythonWExeName"])
    if consoleMode == True:
        flags.append('/DOutFileName=' + config["nsisConfig"]['OutConsoleFileName'])
        flags.append('/DConsoleMode=1')
    else:
        flags.append('/DOutFileName=' + config["nsisConfig"]['OutFileName'])
        flags.append('/DConsoleMode=0')
    #ToDo:
    flags.append('/DPyFolder=Python')
    flags.append(scriptpath + '\\Runtime\\CybeSystemsPortable.nsi')
    return(flags)

def extractDefaultPython(config, path, releasePath):
    flags=[]
    flags.append(config["buildConfig"]["cyDistributePath"] + '\\Runtime\\7zip\\7z.exe')
    flags.append('x -o' + quoteFolder(releasePath))
    flags.append(path)
    return(flags)

def getCybeSystemsIconChangerFlags(config, releasePath, oldname, newname):
    flags=[]
    flags.append(config["buildConfig"]["cyDistributePath"] + '\\Runtime\\CybeSystemsIconChanger\\changeIcon.exe')
    flags.append(quoteFolder(releasePath + '\\' + oldname))
    flags.append(quoteFolder(releasePath + '\\' + newname))
    flags.append(quoteFolder(config["buildConfig"]['appIcon']))
    return(flags)

def zipStdLib(config):
    flags=[]
    flags.append(config["buildConfig"]["cyDistributePath"] + '\\Runtime\\7zip\\7z.exe')
    flags.append('a -tzip -r -mx=9 ' + quoteFolder(config["buildConfig"]['pythonReleasePath'] + "\\Python") + config['nsisConfig']['PythonVersion'] + '.zip')
    flags.append(quoteFolder(config["buildConfig"]['pythonReleasePath'] + "\\lib\\*"))
    return(flags)

dontUpx=[]
dontUpx.append("qwindows.dll")
dontUpx.append("qoffscreen.dll")
dontUpx.append("qminimal.dll")

def compressUpx(config,extension):
    for root, _, files in os.walk(config["buildConfig"]['pythonReleasePath']):
        for afile in files:
            fullpath = os.path.join(root, afile)
            if os.path.splitext(afile)[1] == extension:
                print (afile)
                if afile not in dontUpx:
                    print("UPX compressing", fullpath)
                    run_command(upxFile(config, fullpath))

def upxFile(config, file):
    flags=[]
    flags.append(config["buildConfig"]["cyDistributePath"] + '\\Runtime\\upx.exe')
    flags.append(quoteFolder(file))
    return(flags)

def pyminifierFile(fullpath):
    flags=[]
    flags.append(sys.executable)
    flags.append("-m pyminifier")
    flags.append("--outfile " + fullpath.replace("\\","/"))
    flags.append(fullpath.replace("\\","/"))
    return(flags)

def compressFiles(path,extension):
    for root, _, files in os.walk(path):
        for afile in files:
            fullpath = os.path.join(root, afile)
            if os.path.splitext(afile)[1] == extension:
                print("compressing", fullpath)
                run_command(pyminifierFile(fullpath))

def copytree(src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)
                os.symlink(os.readlink(s), d)
            """try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass # lchmod not available"""
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def copyLibrary(buildConfig, library):
    #Check if this folder contains Pyd files
    dllFile = False
    if countDllFilesExtension(os.path.dirname(sys.executable) + buildConfig['libPath'] + library, '.pyd') != 0:
        dllFile = True
    if countDllFilesExtension(os.path.dirname(sys.executable) + buildConfig['libPath'] + library, '.dll') != 0:
        dllFile = True

    fullpath = os.path.dirname(sys.executable) + buildConfig['libPath'] + library
    stripPath = fullpath.replace(os.path.dirname(sys.executable) + "\\Lib\\site-packages","")
    print(os.path.dirname(sys.executable) + "\\lib\\site-packages")
    print(stripPath)
    if not os.path.exists(os.path.dirname(buildConfig['pythonReleasePath'] + buildConfig['dllPath'] + stripPath)):
        os.makedirs(os.path.dirname(buildConfig['pythonReleasePath'] + buildConfig['dllPath'] + stripPath))

    if dllFile == False:
        if os.path.isdir(os.path.dirname(sys.executable) + buildConfig['libPath'] + library):
            copytree(os.path.dirname(sys.executable) + buildConfig['libPath'] + library, buildConfig['pythonReleasePath'] + '\\Lib\\' + library)
        elif os.path.isfile(os.path.dirname(sys.executable) + buildConfig['libPath'] + library):
            shutil.copyfile(os.path.dirname(sys.executable) + buildConfig['libPath'] + library, buildConfig['pythonReleasePath'] + '\\Lib\\' + library)
    else:
        if os.path.isdir(os.path.dirname(sys.executable) + buildConfig['libPath'] + library):
            copytree(os.path.dirname(sys.executable) + buildConfig['libPath'] + library, buildConfig['pythonReleasePath'] + buildConfig['dllPath'] + library)
        elif os.path.isfile(os.path.dirname(sys.executable) + buildConfig['libPath'] + library):
            shutil.copyfile(os.path.dirname(sys.executable) + buildConfig['libPath'] + library, buildConfig['pythonReleasePath'] + buildConfig['dllPath'] + library)


#Copy
def copyDllFilesExtension(buildConfig, path,extension):
    for root, _, files in os.walk(path):
        for afile in files:
            fullpath = os.path.join(root, afile)
            if os.path.splitext(afile)[1] == extension:
                stripPath = fullpath.replace(buildConfig['pythonReleasePath'] + "\\lib\\site-packages",'')
                if not os.path.exists(os.path.dirname(buildConfig['pythonReleasePath'] + '\\DLLs' + stripPath)):
                    os.makedirs(os.path.dirname(buildConfig['pythonReleasePath'] + '\\DLLs' + stripPath))
                shutil.copyfile(fullpath, buildConfig['pythonReleasePath'] + '\\DLLs' + stripPath)
                os.remove(fullpath)


#Copy
def countDllFilesExtension(path,extension):
    pydFound = 0
    for root, _, files in os.walk(path):
        for afile in files:
            if os.path.splitext(afile)[1] == extension:
                pydFound = pydFound +1
    return pydFound

#Create Nuitka Bootstrapper
def nuitkaCompileMain(fullpath, buildConfig):
    nuitkaPath = os.path.dirname(sys.executable) + "\\Scripts\\nuitka"
    if not os.path.isfile(nuitkaPath):
        print ("Nutika compiler is not installed")
        sys.exit()
    #http://manpages.ubuntu.com/manpages/utopic/man1/nuitka.1.html
    flags=[]
    flags.append(sys.executable)
    flags.append(nuitkaPath)
    flags.append("--icon=" + quoteFolder(buildConfig['appIcon']))
    flags.append("--recurse-none")
    #flags.append("--nofreeze-stdlib")
    #flags.append("--python-flag=-S")
    #flags.append("--nofreeze-stdlib")
    #flags.append("--windows-disable-console")
    flags.append("--remove-output")
    flags.append(fullpath.replace("\\","/"))
    return(flags)

def nuitkaCompileStandaloneMain(fullpath, buildConfig):
    nuitkaPath = os.path.dirname(sys.executable) + "\\Scripts\\nuitka"
    if not os.path.isfile(nuitkaPath):
        print ("Nutika compiler is not installed")
        sys.exit()
    #http://manpages.ubuntu.com/manpages/utopic/man1/nuitka.1.html
    flags=[]
    flags.append(sys.executable)
    flags.append(nuitkaPath)
    flags.append("--icon=" + quoteFolder(buildConfig['appIcon']))
    flags.append("--standalone")
    flags.append("--recurse-all")
    flags.append("--plugin-enable=qt-plugins")
    flags.append("--improved")
    flags.append("--show-modules")
    flags.append("--show-scons")
    #flags.append("--windows-disable-console")
    flags.append("--remove-output")
    flags.append(fullpath.replace("\\","/"))
    return(flags)

def dropCacheFiles(path):
    print("############################################################################")
    print("# Drop Cache Files")
    print("############################################################################")
    remove_file_extension(path,".pyc")
    remove_file_extension(path,".pyo")
    remove_file_extension(path,".orig")
    remove_file_extension(path,".bak")
    remove_file_extension(path,".rej")

    remove_folder(path,"__pycache__")
    remove_folder(path,"psutil.egg-info")

def dropDocFiles(path):
    print("############################################################################")
    print("# Drop Text and unneeded files")
    print("############################################################################")
    silentremove(path + "\\LICENSE.txt")
    silentremove(path + "\\NEWS.txt")
    silentremove(path + "\\README.txt")

    shutil.rmtree(path + "\\Doc" ,ignore_errors=True)
    shutil.rmtree(path + "\\include" ,ignore_errors=True)
    shutil.rmtree(path + "\\libs" ,ignore_errors=True)

def dropTestFiles(path):
    print("############################################################################")
    print("# Drop Test and Demo Files")
    print("############################################################################")
    remove_folder(path,"test")
    remove_folder(path,"tests")
    remove_folder(path,"examples")
    remove_folder(path,"samples")
    remove_folder(path,"doc")
    remove_folder(path,"demos")
    remove_file_extension(path,".txt")

    shutil.rmtree(path + "\\Lib\\ctypes\\test" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\distutils\\tests" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\idlelib\\idle_test" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\lib2to3\\tests" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\sqlite3\\test" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\test" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\tkinter\\test" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\unittest\\test" ,ignore_errors=True)

def dropDevFiles(path):
    print("############################################################################")
    print("# Drop Developer libraries - We build a runtime and dont need this files")
    print("############################################################################")
    shutil.rmtree(path + "\\Lib\\idlelib" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\unittest" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\turtledemo" ,ignore_errors=True)

def dropTKInterTCLFiles(path):
    print("############################################################################")
    print("# Drop TKInter/TCL - In most cases unneded")
    print("############################################################################")
    shutil.rmtree(path + "\\tcl" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\tkinter" ,ignore_errors=True)
    silentremove(path + "\\DLLs\\tcl86t.dll")
    silentremove(path + "\\DLLs\\tk86t.dll")

def dropBuildFiles(path):
    print("############################################################################")
    print("# Drop Build files -> Needed for PIP")
    print("############################################################################")
    shutil.rmtree(path + "\\Scripts" ,ignore_errors=True)
    shutil.rmtree(path + "\\Tools" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\lib2to3" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\ensurepip" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\distutils" ,ignore_errors=True)

#
###################################################################################################
