import os, sys, glob, subprocess, platform, compileall, shutil, distutils, json



def defaultConfig():
    ###################################################################################################
    # NSIS Config
    #
    #    OutFileName
    #        Description: The Generated .exe launcher filename
    #        Default:     CybeSystemsPortable.exe
    #
    #    ProductName
    #        Description: Windows Detail: ProductName
    #        Default:     CybeSystems
    #
    #    Comments
    #        Description: Windows Detail -> Comments
    #        Default:     ""
    #
    #    CompanyName
    #        Description: Windows Detail -> CompanyName
    #        Default:     CybeSystems.com
    #
    #    LegalCopyright
    #        Description: Windows Detail -> LegalCopyright
    #        Default:     "(c) CybeSystems.com"
    #
    #    FileDescription
    #        Description: Windows Detail -> FileDescription
    #        Default:     "CybeSystems Python Launcher"
    #
    #    FileVersion
    #        Description: Windows Detail -> FileVersion
    #        Default:     '1.0.0.0'
    #
    #    ProductVersion
    #        Description: Windows Detail -> ProductVersion
    #        Default:     '1.0.0.0'
    #
    #    InternalName
    #        Description: Windows Detail -> InternalName
    #        Default:     "CybeSystems"
    #
    #    LegalTrademarks
    #        Description: Windows Detail -> LegalTrademarks
    #        Default:     "CybeSystems"
    #
    #    OriginalFilename
    #        Description: Windows Detail -> OriginalFilename
    #        Default:     "CybeSystems.exe"
    #
    #    PrivateBuild
    #        Description: Windows Detail -> PrivateBuild
    #        Default:     ""
    #
    #    SpecialBuild
    #        Description: Windows Detail -> SpecialBuild
    #        Default:     ""
    #
    ###################################################################################################
    config = {}

    config['nsisConfig'] = {}
    config['nsisConfig']['CreateConsoleAndWindowVersion'] = True
    config['nsisConfig']['OutFileName'] = 'CybeSystemsPortable.exe'
    config['nsisConfig']['OutConsoleFileName'] = 'CybeSystemsPortable-Console.exe'
    config['nsisConfig']['ProductName'] = "CybeSystems"
    config['nsisConfig']['Comments'] = ""
    config['nsisConfig']['CompanyName'] = "CybeSystems.com"
    config['nsisConfig']['LegalCopyright'] = "(c) CybeSystems.com"
    config['nsisConfig']['FileDescription'] = "CybeSystems Python Launcher"
    config['nsisConfig']['FileVersion'] = '1.0.0.0'
    config['nsisConfig']['ProductVersion'] = '1.0.0.0'
    config['nsisConfig']['InternalName'] ="CybeSystems"
    config['nsisConfig']['LegalTrademarks'] = "CybeSystems"
    config['nsisConfig']['OriginalFilename'] ="CybeSystems.exe"
    config['nsisConfig']['PrivateBuild'] = ""
    config['nsisConfig']['SpecialBuild'] = ""

    ###################################################################################################
    # Build Config
    #
    #    appIcon
    #        Description: Path to your .ico file
    #        Default:     scriptpath + "\\AppInfo\\appicon.ico"
    #
    #    pyFileMinfifier
    #        Description: Minify Python libraries
    #        Default:     0  - Disable -> Recommend if you use zipPythonStdLib
    #                     1  - Compile Py files to pyc (Save ca 3,5MB)
    #                     2  - Minify with Pyminifier Script (Save ca 2MB)
    #
    #    Zip Python StdLibs
    #        Description: PythonXX.zip (in w.g. 3.4: Python34.zip) get autoincluded at Runtime
    #                     It save much space and make copies (e.g. on USB Stick) much faster
    #        Default:     True - (Enabled) Recommend
    #
    #    Release Python Path
    #        Description: Python build script is working in this folder until it's done
    #        Default:     scriptpath + "\\Release"
    #
    ###################################################################################################

    config['buildConfig'] = {}
    config['buildConfig']['pythonCustomInterpreter'] = True
    config['buildConfig']['pythonExeName'] = "CybeSystems.exe"
    config['buildConfig']['pythonWExeName'] = "CybeSystemsW.exe"
    config['buildConfig']['startFile'] = "PyQt5HelloWorld.py"
    config['buildConfig']['copyStartFile'] = True
    config['buildConfig']['appIcon'] = "\\AppInfo\\appicon.ico"
    config['buildConfig']['pyFileMinfifier'] = 0
    config['buildConfig']['zipPythonStdLib'] = True
    config['buildConfig']['useCustomSite.py'] = True
    config['buildConfig']['useCustomSite.py'] = True
    config['buildConfig']['createNuitkaLauncher'] = True
    config['buildConfig']['useUpx'] = True

    config['buildConfig']['libPath'] ="\\Lib\\site-packages\\"
    config['buildConfig']['dllPath'] ="\\Lib\\site-packages\\"
    if config['buildConfig']['zipPythonStdLib']:
        config['buildConfig']['dllPath'] = "\\DLLs\\"

    #Some files like Qt Plugins dont support UPX (plugins dont load)
    config['buildConfig']['upxIgnore'] =[]
    config['buildConfig']['upxIgnore'].append("qwindows.dll")
    config['buildConfig']['upxIgnore'].append("qoffscreen.dll")
    config['buildConfig']['upxIgnore'].append("qminimal.dll")

    ###################################################################################################
    # Packages
    #
    #    packagesArray
    #        Description: Any package that should get included
    #                     if you want to zip the stdlibs all libs contains pyd or dll files
    #                     files get copied to config['buildConfig']['dllPath']
    #        Default:     none
    #
    #    packagesHookArray
    #        Description: Files that need special work - e.g. PyQt
    #        Default:     none
    #
    #    packagesHookArray
    #        Description: Files that need special work - e.g. PyQt
    #        Default:     none
    #
    #    packagesPyQt5Array
    #        Description: Files that should copied from PyQt
    #        Default:     none
    #
    ###################################################################################################

    config['packagesArray'] = []
    config['packagesArray'].append('psutil')

    config['packagesHookArray'] = []
    config['packagesHookArray'].append("PyQt5")

    config['packagesPyQt5Array'] = []
    config['packagesPyQt5Array'].append("icudt53.dll")
    config['packagesPyQt5Array'].append("icuin53.dll")
    config['packagesPyQt5Array'].append("icuuc53.dll")
    config['packagesPyQt5Array'].append("libeay32.dll")
    config['packagesPyQt5Array'].append("ssleay32.dll")
    config['packagesPyQt5Array'].append("qt5core.dll")
    config['packagesPyQt5Array'].append("qt5gui.dll")
    config['packagesPyQt5Array'].append("qt5widgets.dll")
    config['packagesPyQt5Array'].append("Qt.pyd")
    config['packagesPyQt5Array'].append("QtCore.pyd")
    config['packagesPyQt5Array'].append("QtGui.pyd")
    config['packagesPyQt5Array'].append("QtWidgets.pyd")

    #configFile="pyDistribute.json"

    config['runtime'] = {}
    config['runtime']['configFile'] = "pyDistribute.json"
    config['runtime']['outputFolder'] = os.path.realpath(os.path.dirname(__file__))
    config['runtime']['pythonVersion'] =  ', '.join(map(str,sys.version_info[:2])).replace(", ","")
    config['runtime']['cyDistributePath'] = os.path.realpath(os.path.dirname(__file__))
    config['runtime']['pythonReleasePath'] = "\\Python" + ', '.join(map(str,sys.version_info[:2])).replace(", ","")


    return config

def getOptions(base_path, args):
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--config',
                        dest = 'config', help = 'Use config file -> ABSOLUTE Path needed !')

    options, unknown = parser.parse_known_args(args)
    return options

def createConfigJson(config):
    if not os.path.isfile(config['runtime']['configFile']):
        with open(config['runtime']['configFile'], 'w') as outfile:
            json.dump(config, outfile, sort_keys = True, indent = 4)

def getConfig(configFile=None):
    config = defaultConfig()
    #scriptpath = os.path.realpath(os.path.dirname(sys.argv[0]))
    scriptpath = os.path.realpath(os.path.dirname(__file__))
    options = getOptions(scriptpath, sys.argv[1:])
    config['runtime']['pythonVersion']= ', '.join(map(str,sys.version_info[:2])).replace(", ","")
    if configFile == None:
        config['runtime']['configFile'] = scriptpath + '\\' + config['runtime']['configFile']
        if options.config:
            config['runtime']['configFile'] = options.config
            print (options.config)
            print (config['runtime']['configFile'])
    else:
        config['runtime']['configFile'] = configFile

    if not os.path.isfile(config['runtime']['configFile']):
        print("Config File " + config['runtime']['configFile'] + " not exist")
        sys.exit()
    with open(config['runtime']['configFile']) as json_file:
        json_data = json.load(json_file)

    config= dict_merge(config, json_data)

    with open(config['runtime']['configFile'], 'w') as outfile:
        configSave = config.copy()
        #Dont save runtime generated values
        del configSave['runtime']
        json.dump(configSave, outfile, sort_keys = True, indent = 4)

    # Override runtime generated configs
    config['runtime']['outputFolder'] = os.path.dirname(config['runtime']['configFile'])
    config['buildConfig']['appIcon'] = config['runtime']['outputFolder'] + config['buildConfig']['appIcon']
    config['runtime']['pythonReleasePath'] = config['runtime']['outputFolder'] + config['runtime']['pythonReleasePath']

    #createConfigJson(config)
    validatePyDistribute(config)
    return config

#def mergeDefaultConfg(file):

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

def validatePyDistribute(config):
    if not os.path.isfile(config['runtime']['cyDistributePath'] + "\\Runtime\\Python\\Python" + config['runtime']['pythonVersion'] + ".7z"):
        print('Python' + config['runtime']['pythonVersion'] + ' not found (' + config['runtime']['cyDistributePath'] + '\\Runtime\\Python\\Python' + config['runtime']['pythonVersion'] + '.7z)')
        sys.exit()
    if not os.path.isdir(config['runtime']['cyDistributePath'] + "\\Runtime"):
        print("Runtime Folder not found - PyDistribute in wrong Path ?")
        sys.exit()
    if not os.path.isfile(config['runtime']['configFile']):
        print("Config File " + config['runtime']['configFile'] + " not exist")
        sys.exit()
    if not os.path.isfile(config['buildConfig']['appIcon']):
        print("Icon File " + config['buildConfig']['appIcon'] + " not found")
        sys.exit()



def movePydDll(config, recursive=False):
    ignoreFolder = ['site-packages','Lib']
    resolvedFolder = []
    extension = ['.pyd', '.dll']
    for root, _, files in os.walk(config['runtime']['pythonReleasePath'] + "\\Lib"):
        for afile in files:
            fullpath = os.path.join(root, afile)
            if os.path.splitext(afile)[1].endswith(tuple(extension)):
                if os.path.split(os.path.dirname(fullpath))[1] not in ignoreFolder:
                    if not os.path.dirname(fullpath).startswith(tuple(resolvedFolder)):
                        resolvedFolder.append(os.path.dirname(fullpath))
                        print("Moving Folder " + os.path.dirname(fullpath) + " to DLL Folder (contains .pyd or .dll files)")
                        libraryName = os.path.split(os.path.dirname(fullpath))[1]
                        shutil.copytree(os.path.dirname(fullpath), config['runtime']['pythonReleasePath'] + '\\DLLs\\' + libraryName)
                        shutil.rmtree(os.path.dirname(fullpath) ,ignore_errors=True)
                else:
                    print("Moving File " + os.path.dirname(fullpath) + " to DLL Folder (contains .pyd or .dll files)")
                    shutil.copyfile(fullpath, config['runtime']['pythonReleasePath'] + '\\DLLs\\' + afile)
                    os.remove(fullpath)

def parseRequirementsTxt(config, requirements):
    if os.path.isfile(requirements):
        requirements = open(requirements, "r")
        lines=requirements.readlines()
        for line in lines:
            line = line.strip()
            if not line.startswith("#") and line != "":
                print (line)
                run_command(pip3install(config, line))
    else:
        print("Cant find " + requirements + " -> Ignore")



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

def runCommandWithPath(config, command, path, includeSysPath = True):
    if isinstance(command, list):
        print("Runnning Shell command: " + ' '.join(command))
        command = ' '.join(command)
    else:
        print("Runnning Shell command: " + command)

    commandEnviron= {}
    if includeSysPath:
        commandEnviron = os.environ
        commandEnviron['PATH'] = path + ";" + os.environ['PATH']
        #We need to alternate the APPDATA Path -> Nuitka is searching for depends.exe in AppData\\Roaming
        # It searches for zip file NOT for binaries (e.g. C:\Users\USERNAME\AppData\Roaming\nuitka\depends22_x86.zip
        commandEnviron['APPDATA'] = config['runtime']['cyDistributePath'] + "\\Runtime"
    else:
        commandEnviron['PATH'] = path
    #commandEnviron['PYTHONPATH'] = path
    print(commandEnviron['PATH'])

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

def remove_folder_endswith(path,pathToDelete):
    for curdir, dirs, files in os.walk(path):
        for d in dirs:
            if d.endswith(pathToDelete):
                shutil.rmtree(os.path.join(curdir, d))

def remove_folder_startswith(path,pathToDelete):
    for curdir, dirs, files in os.walk(path):
        for d in dirs:
            if d.startswith(pathToDelete):
                shutil.rmtree(os.path.join(curdir, d))


def silentremove(filename):
    try:
        os.remove(filename)
    except:
        pass


def detectOS():
    # Detect OS platform and set the approriate script paths, i.e. build/[patform]
    if platform.system() == 'Darwin':
        print('Mac OS detected')
        return 'osx'
    elif platform.system() == 'Linux':
        print('Linux OS detected')
        return 'linux'
    elif platform.system() == 'Windows':
        print('Windows OS detected')
        os.environ['PYTHONPATH'] = sys.exec_prefix
        os.environ['PATH'] = sys.exec_prefix + '\\Scripts'
        return 'windows'
    # make sure Mac/Linux user is not root
    if (platform.system() == 'Darwin' or platform.system() == 'Linux') and os.getuid() == 0:
        print('This script does not require sudo!')
        print("To avoid changing PyQt permissions, simply run with 'python build.py'")
        sys.exit()

def detectArchitecture():
    if sys.maxsize == 2147483647:
        print ("Running x86")
        return 'X86'
    else:
        print ("Running x64")
        return 'X64'

def compressUpx(config,extension):
    for root, _, files in os.walk(config['runtime']['pythonReleasePath']):
        for afile in files:
            fullpath = os.path.join(root, afile)
            if os.path.splitext(afile)[1] == extension:
                print (afile)
                if afile not in config['buildConfig']['upxIgnore']:
                    print("UPX compressing", fullpath)
                    run_command(upxFile(config, fullpath))



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

def addPackages(config):
    for library in config['packagesArray']:
        if os.path.isdir(os.path.dirname(sys.executable) + config['buildConfig']['libPath'] + library):
            copytree(os.path.dirname(sys.executable) + config['buildConfig']['libPath'] + library, config['runtime']['pythonReleasePath'] + '\\Lib\\' + library)
        elif os.path.isfile(os.path.dirname(sys.executable) + config['buildConfig']['libPath'] + library):
            shutil.copyfile(os.path.dirname(sys.executable) + config['buildConfig']['libPath'] + library, config['runtime']['pythonReleasePath'] + '\\Lib\\' + library)


###################################################################################################
# Build scripts
###################################################################################################

def addNsisLauncher(config):
    run_command(createNsisLauncher(config))
    if os.path.isfile(config['runtime']['cyDistributePath'] + "\\Runtime\\" + config['nsisConfig']['OutFileName']):
        shutil.copyfile(config['runtime']['cyDistributePath'] + "\\Runtime\\" + config['nsisConfig']['OutFileName'], config['runtime']['outputFolder'] + "\\" + config['nsisConfig']['OutFileName'])
        os.remove(config['runtime']['cyDistributePath'] + "\\Runtime\\" + config['nsisConfig']['OutFileName'])
    if config['nsisConfig']['CreateConsoleAndWindowVersion']:
        run_command(createNsisLauncher(config, True))
        if os.path.isfile(config['runtime']['cyDistributePath'] + "\\Runtime\\" + config['nsisConfig']['OutConsoleFileName']):
            shutil.copyfile(config['runtime']['cyDistributePath'] + "\\Runtime\\" + config['nsisConfig']['OutConsoleFileName'], config['runtime']['outputFolder'] + "\\" + config['nsisConfig']['OutConsoleFileName'])
            os.remove(config['runtime']['cyDistributePath'] + "\\Runtime\\" + config['nsisConfig']['OutConsoleFileName'])

def addPythonInterpreter(config):
    try:
        os.remove(config['runtime']['pythonReleasePath'] + '\\' + config['nsisConfig']['OutFileName'])
    except:
        pass
    shutil.rmtree(config['runtime']['pythonReleasePath'] ,ignore_errors=True)
    run_command(extractDefaultPython(config, quoteFolder(config['runtime']['cyDistributePath'] + '\\Runtime\\Python\\Python' + config['runtime']['pythonVersion'] + '.7z'), config['runtime']['pythonReleasePath']))

def addCustomLibrarys(config):
    if os.path.exists(config['runtime']['cyDistributePath'] + "\\TempLib"):
        copytree(config['runtime']['cyDistributePath'] + "\\TempLib", config['runtime']['pythonReleasePath'] + '\\Lib')

    if os.path.exists(config['runtime']['cyDistributePath'] + "\\TempDll"):
        copytree(config['runtime']['cyDistributePath'] + "\\TempDll", config['runtime']['pythonReleasePath'] + '\\DLLs')

    shutil.rmtree(config['runtime']['cyDistributePath'] + '/TempLib' ,ignore_errors=True)
    shutil.rmtree(config['runtime']['cyDistributePath'] + '/TempDll' ,ignore_errors=True)

def minifyPythonInterpreter(config):
    dropCacheFiles(config['runtime']['pythonReleasePath'])
    dropDocFiles(config['runtime']['pythonReleasePath'])
    dropTestFiles(config['runtime']['pythonReleasePath'])
    dropDevFiles(config['runtime']['pythonReleasePath'])
    dropTKInterTCLFiles(config['runtime']['pythonReleasePath'])
    dropBuildFiles(config['runtime']['pythonReleasePath'])



def addHookPackages(config):
    if "PyQt5" in config['packagesHookArray']:
        #Sip is always needed

        copytree(os.path.dirname(sys.executable) + '\\Lib\\site-packages\\PyQt5\\plugins\\platforms', config['runtime']['pythonReleasePath'] + '\\DLLs\\PyQt5\\plugins\\platforms')
        shutil.copyfile(os.path.dirname(sys.executable) + '\\Lib\\site-packages\\sip.pyd', config['runtime']['pythonReleasePath'] + '\\DLLs\\sip.pyd')
        for file in config['packagesPyQt5Array']:
            shutil.copyfile(os.path.dirname(sys.executable) + '\\Lib\\site-packages\\PyQt5\\' + file, config['runtime']['pythonReleasePath'] + '\\DLLs\\PyQt5\\' + file)
        # We use site.py to init Qt -> Ignore
        shutil.copyfile(config['runtime']['cyDistributePath'] + '\\Runtime\\Python\\qt.conf', config['runtime']['pythonReleasePath'] + '\\qt.conf')
        #msvcp100.dll is needed for PyQt
        shutil.copyfile(config['runtime']['cyDistributePath'] + '\\Runtime\\Python\\msvcp100.dll', config['runtime']['pythonReleasePath'] + '\\msvcp100.dll')

def createDistribution(config):
    if config['buildConfig']['pythonCustomInterpreter']:
        run_command(getCybeSystemsIconChangerFlags(config, config['runtime']['pythonReleasePath'], "python.exe", config['buildConfig']['pythonExeName']))
        run_command(getCybeSystemsIconChangerFlags(config, config['runtime']['pythonReleasePath'], "pythonw.exe", config['buildConfig']['pythonWExeName']))

    if config['buildConfig']['pyFileMinfifier'] != 0:
        # 1: Compile to pyc
        if config['buildConfig']['pyFileMinfifier'] == True:
            compileall.compile_dir(config['runtime']['pythonReleasePath'],1000, legacy=True, ddir="",optimize=2)
            remove_file_extension(config['runtime']['pythonReleasePath'],".py")
        # 2: PyMinifier
        elif config['buildConfig']['pyFileMinfifier'] == 2:
            print("############################################################################")
            print("# Create named interpreter")
            print("############################################################################")
            pyminifierFile(config['runtime']['pythonReleasePath'], ".py")

    #Replace site.py -> Set Environment variables for PyQt5 etc.
    if config['buildConfig']['useCustomSite.py']:
        os.remove(config['runtime']['pythonReleasePath'] + '\\Lib\\site.py')
        shutil.copyfile(config['runtime']['cyDistributePath'] + '\\Runtime\\Python\\site.py', config['runtime']['pythonReleasePath'] + '\\Lib\\site.py')

    if config['buildConfig']['zipPythonStdLib'] == True:
        run_command(zipStdLib(config))
        shutil.rmtree(config['runtime']['pythonReleasePath'] + "\\Lib" ,ignore_errors=True)

    shutil.copyfile(config['runtime']['cyDistributePath'] + '\\Runtime\\Python\\msvcr100.dll', config['runtime']['pythonReleasePath'] + '\\msvcr100.dll')
    shutil.copyfile(config['runtime']['cyDistributePath'] + '\\Runtime\\Python\\python34.dll', config['runtime']['pythonReleasePath'] + '\\python34.dll')

    if config['buildConfig']['createNuitkaLauncher'] == True:
        runCommandWithPath(config, nuitkaCompileMain(quoteFolder(config['runtime']['outputFolder'] + '\\' + config['buildConfig']['startFile']), config['buildConfig']), os.path.dirname(sys.executable))
        #runCommandWithPath(nuitkaCompileStandaloneMain(quoteFolder(config['runtime']['cyDistributePath'] + '\\' + config['buildConfig']['startFile']), config['buildConfig']), os.path.dirname(sys.executable))
        shutil.copyfile(config['runtime']['outputFolder'] + '\\' + config['buildConfig']['startFile'].replace('.py','.exe'), config['runtime']['pythonReleasePath'] + '\\' + config['buildConfig']['startFile'].replace('.py','.exe'))
        os.remove(config['runtime']['outputFolder'] + '\\' + config['buildConfig']['startFile'].replace('.py','.exe'))

    if config['buildConfig']['copyStartFile'] == True:
        shutil.copyfile(config['runtime']['outputFolder'] + '\\' + config['buildConfig']['startFile'], config['runtime']['pythonReleasePath'] + '\\' + config['buildConfig']['startFile'])

    if config['buildConfig']['useUpx'] == True:
        compressUpx(config, ".dll")
        compressUpx(config,".exe")

    if config['buildConfig']['useCustomSite.py'] == False and config['buildConfig']['zipPythonStdLib'] == True:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("You use zip for Stdlibs without custom site.py - Make sure to include lib\\site-packages in your init script !")
        print("Sample:")
        print("    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'lib\\site-packages'))")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    if config['buildConfig']['zipPythonStdLib'] == True and config['buildConfig']['createNuitkaLauncher']:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("You use zip for Stdlibs and use Nuitka Launcher - Make sure to include lib\\site-packages in your init script !")
        print("Nutika seems to ignore site.py -> Need a workaround for this")
        print("Sample:")
        print("    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'lib\\site-packages'))")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

def cyDistribute(config):

    addNsisLauncher(config)
    addPythonInterpreter(config)
    print("############################################################################")
    print("# include Temp Liberarys if added from other script")
    print("############################################################################")
    addCustomLibrarys(config)
    print("############################################################################")
    print("# Copy Packages (See Hooks section for e.g. PyQt and other libs that need hooks")
    print("############################################################################")
    addPackages(config)
    print("############################################################################")
    print("# Resolve requirements.txt")
    print("############################################################################")
    parseRequirementsTxt(config, config['runtime']['outputFolder'] + "\\requirements.txt")
    print("############################################################################")
    print("# Move .pyd and .dll files/librarys to DLLs Folder")
    print("############################################################################")
    movePydDll(config)
    print("############################################################################")
    print("# Drop Files")
    print("############################################################################")
    minifyPythonInterpreter(config)
    print("############################################################################")
    print("# Hooks (like PyQt, Pywin32...")
    print("############################################################################")
    addHookPackages(config)
    print("############################################################################")
    print("# Create named interpreter")
    print("############################################################################")
    createDistribution(config)

###################################################################################################
# CMDLine Commands
###################################################################################################

def pip3install(config, package):
    flags=[]
    flags.append(os.path.dirname(sys.executable) + '\\Scripts\\pip3.exe')
    flags.append("install")
    flags.append("-I --root " + quoteFolder(config['runtime']['outputFolder']))
    flags.append(package)
    return(flags)

def runPyDistribute(pyDistributeFolder, configFile):
    flags=[]
    flags.append(sys.executable)
    flags.append(pyDistributeFolder + '\\pyDistribute.py')
    flags.append('--config=' + configFile)
    return(flags)

def createPortableAppsInstaller(PortableAppsInstallerPath, releaseFolderName):
    flags=[]
    flags.append(PortableAppsInstallerPath)
    flags.append(releaseFolderName)
    return(flags)

def create7zipRelease(pyDistributeFolder, releaseFolderName, outFile):
    flags=[]
    flags.append(pyDistributeFolder + '\\Runtime\\7zip\\7z.exe')
    flags.append('a -r -t7z -mx=9 ' + quoteFolder(outFile))
    flags.append(quoteFolder(releaseFolderName))
    return(flags)

def createNsisLauncher(config, consoleMode=False):
    flags=[]
    flags.append(config['runtime']['cyDistributePath'] + '\\Runtime\\NSIS\\makensis.exe')
    flags.append('/DFileIcon=' + quoteParameter(config['buildConfig']['appIcon']))
    flags.append('/DPythonVersion=' + config['runtime']['pythonVersion'])

    flags.append('/DProductName=' + quoteParameter(config['nsisConfig']['ProductName']))
    flags.append('/DComments=' + quoteParameter(config['nsisConfig']['Comments']))
    flags.append('/DCompanyName=' + quoteParameter(config['nsisConfig']['CompanyName']))
    flags.append('/DLegalCopyright=' + quoteParameter(config['nsisConfig']['LegalCopyright']))
    flags.append('/DFileDescription=' + quoteParameter(config['nsisConfig']['FileDescription']))
    flags.append('/DFileVersion=' + config['nsisConfig']['FileVersion'])
    flags.append('/DProductVersion=' + config['nsisConfig']['ProductVersion'])
    flags.append('/DInternalName=' + quoteParameter(config['nsisConfig']['InternalName']))
    flags.append('/DLegalTrademarks=' + quoteParameter(config['nsisConfig']['LegalTrademarks']))
    flags.append('/DOriginalFilename=' + quoteParameter(config['nsisConfig']['OriginalFilename']))
    flags.append('/DPrivateBuild=' + quoteParameter(config['nsisConfig']['PrivateBuild']))
    flags.append('/DSpecialBuild=' + quoteParameter(config['nsisConfig']['SpecialBuild']))
    flags.append('/DPyStartFile=' + config['buildConfig']['startFile'])
    if config['buildConfig']['pythonCustomInterpreter']:
        flags.append('/DInterpreter=' + config['buildConfig']['pythonExeName'])
        flags.append('/DInterpreterW=' + config['buildConfig']['pythonWExeName'])
    if consoleMode == True:
        flags.append('/DOutFileName=' + config['nsisConfig']['OutConsoleFileName'])
        flags.append('/DConsoleMode=1')
    else:
        flags.append('/DOutFileName=' + config['nsisConfig']['OutFileName'])
        flags.append('/DConsoleMode=0')
    #ToDo:
    flags.append('/DPyFolder=Python')
    flags.append(config['runtime']['cyDistributePath'] + '\\Runtime\\CybeSystemsPortable.nsi')
    return(flags)

def extractDefaultPython(config, path, releasePath):
    flags=[]
    flags.append(config['runtime']['cyDistributePath'] + '\\Runtime\\7zip\\7z.exe')
    flags.append('x -o' + quoteFolder(releasePath))
    flags.append(path)
    return(flags)

def getCybeSystemsIconChangerFlags(config, releasePath, oldname, newname):
    flags=[]
    flags.append(config['runtime']['cyDistributePath'] + '\\Runtime\\CybeSystemsIconChanger\\changeIcon.exe')
    flags.append(quoteFolder(releasePath + '\\' + oldname))
    flags.append(quoteFolder(releasePath + '\\' + newname))
    flags.append(quoteFolder(config['buildConfig']['appIcon']))
    return(flags)

def zipStdLib(config):
    flags=[]
    flags.append(config['runtime']['cyDistributePath'] + '\\Runtime\\7zip\\7z.exe')
    flags.append('a -tzip -r -mx=9 ' + quoteFolder(config['runtime']['pythonReleasePath'] + "\\Python") + config['runtime']['pythonVersion'] + '.zip')
    flags.append(quoteFolder(config['runtime']['pythonReleasePath'] + "\\lib\\*"))
    return(flags)

def upxFile(config, file):
    flags=[]
    flags.append(config['runtime']['cyDistributePath'] + '\\Runtime\\upx.exe')
    flags.append(quoteFolder(file))
    return(flags)

def pyminifierFile(fullpath):
    flags=[]
    flags.append(sys.executable)
    flags.append("-m pyminifier")
    flags.append("--outfile " + fullpath.replace("\\","/"))
    flags.append(fullpath.replace("\\","/"))
    return(flags)

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

###################################################################################################
# Drop unneeded files
###################################################################################################
def dropCacheFiles(path):
    print("############################################################################")
    print("# Drop Cache Files")
    print("############################################################################")
    remove_file_extension(path,".pyc")
    remove_file_extension(path,".pyo")
    remove_file_extension(path,".orig")
    remove_file_extension(path,".bak")
    remove_file_extension(path,".rej")

    remove_folder_startswith(path,"__pycache__")
    remove_folder_startswith(path,"psutil.egg-info")

    remove_folder_endswith(path, ".dist-info")


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
    remove_folder_startswith(path,"test")
    remove_folder_startswith(path,"tests")
    remove_folder_startswith(path,"examples")
    remove_folder_startswith(path,"samples")
    remove_folder_startswith(path,"doc")
    remove_folder_startswith(path,"demos")
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
    shutil.rmtree(path + "\\Lib\\site-packages\\setuptools" ,ignore_errors=True)
    shutil.rmtree(path + "\\Lib\\site-packages\\pip" ,ignore_errors=True)

#
###################################################################################################
