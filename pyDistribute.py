#!/usr/bin/env python

###################################################################################################
# CybeSystems PyDistribute
#
# Distribute Python programs
#
# Distribute your python program with real python interpreter (full stdlibs)
# without freezer like cx_freeze or pyinstaller
#
# This script strip down the python interperter to 4-5MB and can create a launcher with nuitka
# additional options are e.g. zip stdlibs (less files -> better for USB Sticks) and
# includes a "Hooks" section for PyQt (manually pick the needed files -> much smaller distriubution)
#
# It includes also a option to crate a NSIS launcher
#
# I've made this script because cx_freeze and pyinstaller need (for my programs) a lot of workarounds
# and I need a real interpreter for subscripts (like updates)
#
# Please make sure to read the section description before using this script
#
###################################################################################################

###################################################################################################
# SECTION INDEX
#
#    NSIS Config
#    Build Config
#    PERFORMANCE SETTINGS
#
###################################################################################################

import os, sys, json

#scriptpath = os.path.realpath(os.path.dirname(sys.argv[0])).replace('/','\\')
scriptpath = os.path.dirname(os.path.realpath(__file__))

scriptpathParentFolder = os.path.dirname(scriptpath)
sys.path.insert(0, os.path.join(scriptpath, 'lib'))

from pyDistributeHelper import *

###################################################################################################
# NSIS Config
#
#    PythonVersion
#        Description: The used Python Version (use 27 for 2.7, 34 for 3.4...)
#        Default:     34  - Python 3.4
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

config["nsisConfig"] = {}
config["nsisConfig"]['PythonVersion'] = '34'
config["nsisConfig"]['CreateConsoleAndWindowVersion'] = True
config["nsisConfig"]['OutFileName'] = 'CybeSystemsPortable.exe'
config["nsisConfig"]['OutConsoleFileName'] = 'CybeSystemsPortable-Console.exe'
config["nsisConfig"]['ProductName'] = "CybeSystems"
config["nsisConfig"]['Comments'] = ""
config["nsisConfig"]['CompanyName'] = "CybeSystems.com"
config["nsisConfig"]['LegalCopyright'] = "(c) CybeSystems.com"
config["nsisConfig"]['FileDescription'] = "CybeSystems Python Launcher"
config["nsisConfig"]['FileVersion'] = '1.0.0.0'
config["nsisConfig"]['ProductVersion'] = '1.0.0.0'
config["nsisConfig"]['InternalName'] ="CybeSystems"
config["nsisConfig"]['LegalTrademarks'] = "CybeSystems"
config["nsisConfig"]['OriginalFilename'] ="CybeSystems.exe"
config["nsisConfig"]['PrivateBuild'] = ""
config["nsisConfig"]['SpecialBuild'] = ""

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

config["buildConfig"] = {}
config["buildConfig"]["cyDistributePath"] = scriptpath
config["buildConfig"]["pythonCustomInterpreter"] = True
config["buildConfig"]["pythonExeName"] = "CybeSystems.exe"
config["buildConfig"]["pythonWExeName"] = "CybeSystemsW.exe"
config["buildConfig"]['startFile'] = "PyQt5HelloWorld.py"
config["buildConfig"]['copyStartFile'] = True
config["buildConfig"]['appIcon'] = "\\AppInfo\\appicon.ico"
config["buildConfig"]['pyFileMinfifier'] = 0
config["buildConfig"]['zipPythonStdLib'] = True
config["buildConfig"]['pythonReleasePath'] = "\\Python"
config["buildConfig"]['useCustomSite.py'] = True
config["buildConfig"]['useCustomSite.py'] = True
config["buildConfig"]['createNuitkaLauncher'] = True
config["buildConfig"]['useUpx'] = True

config["buildConfig"]['libPath'] ="\\Lib\\site-packages\\"
config["buildConfig"]['dllPath'] ="\\Lib\\site-packages\\"
if config["buildConfig"]['zipPythonStdLib']:
    config["buildConfig"]['dllPath'] = "\\DLLs\\"

#Some files like Qt Plugins dont support UPX (plugins dont load)
config["buildConfig"]["upxIgnore"] =[]
config["buildConfig"]["upxIgnore"].append("qwindows.dll")
config["buildConfig"]["upxIgnore"].append("qoffscreen.dll")
config["buildConfig"]["upxIgnore"].append("qminimal.dll")

###################################################################################################
# Packages
#
#    packagesArray
#        Description: Any package that should get included
#                     if you want to zip the stdlibs all libs contains pyd or dll files
#                     files get copied to config["buildConfig"]['dllPath']
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

config["packagesArray"] = []
config["packagesArray"].append('psutil')

config["packagesHookArray"] = []
config["packagesHookArray"].append("PyQt5")

config["packagesPyQt5Array"] = []
config["packagesPyQt5Array"].append("icudt53.dll")
config["packagesPyQt5Array"].append("icuin53.dll")
config["packagesPyQt5Array"].append("icuuc53.dll")
config["packagesPyQt5Array"].append("libeay32.dll")
config["packagesPyQt5Array"].append("ssleay32.dll")
config["packagesPyQt5Array"].append("qt5core.dll")
config["packagesPyQt5Array"].append("qt5gui.dll")
config["packagesPyQt5Array"].append("qt5widgets.dll")
config["packagesPyQt5Array"].append("Qt.pyd")
config["packagesPyQt5Array"].append("QtCore.pyd")
config["packagesPyQt5Array"].append("QtGui.pyd")
config["packagesPyQt5Array"].append("QtWidgets.pyd")

#configFile="pyDistribute.json"

config['runtime'] = {}
config['runtime']['configFile'] = "pyDistribute.json"
config['runtime']['outputFolder'] = scriptpath

def createConfigJson():
    if not os.path.isfile("pyDistribute.json"):
        with open('pyDistribute.json', 'w') as outfile:
            json.dump(config, outfile, sort_keys = True, indent = 4)
createConfigJson()

def getOptions(base_path, args):
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--config',
                        dest = 'config', help = 'Use config file -> ABSOLUTE Path needed !')

    options, unknown = parser.parse_known_args(args)
    return options

def parseCommandLine():
    options = getOptions(scriptpath, sys.argv[1:])
    if options.config:
        config['runtime']['configFile'] = options.config
        print (options.config)
        print (config['runtime']['configFile'])


parseCommandLine()

if not os.path.isfile(config['runtime']['configFile']):
    print("Config File " + config['runtime']['configFile'] + " not exist")
    sys.exit()

with open(config['runtime']['configFile']) as json_file:
    json_data = json.load(json_file)

config= dict_merge(config, json_data)

#Update config['runtime']['configFile'] if new keys was added in config
with open(config['runtime']['configFile'], 'w') as outfile:
    configSave = config.copy()
    #Dont save runtime generated values
    del configSave['runtime']
    del configSave["buildConfig"]["cyDistributePath"]
    json.dump(configSave, outfile, sort_keys = True, indent = 4)

config['runtime']['outputFolder'] = os.path.dirname(config['runtime']['configFile'])

#Override runtime generated configs
config["buildConfig"]["cyDistributePath"] = scriptpath
config["buildConfig"]['appIcon'] = config['runtime']['outputFolder'] + config["buildConfig"]['appIcon']
config["buildConfig"]['pythonReleasePath'] = config['runtime']['outputFolder'] + config["buildConfig"]['pythonReleasePath']

if not os.path.isfile(config["buildConfig"]['appIcon']):
    print("Icon File " + config["buildConfig"]['appIcon'] + " not found")
    sys.exit()

print(config["buildConfig"]['appIcon'])
print(config["buildConfig"]['pythonReleasePath'])

run_command(getNsisFlags(config))
if os.path.isfile(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutFileName']):
    shutil.copyfile(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutFileName'], config['runtime']['outputFolder'] + "\\" + config["nsisConfig"]['OutFileName'])
    os.remove(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutFileName'])
if config["nsisConfig"]['CreateConsoleAndWindowVersion']:
    run_command(getNsisFlags(config, True))
    if os.path.isfile(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutConsoleFileName']):
        shutil.copyfile(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutConsoleFileName'], config['runtime']['outputFolder'] + "\\" + config["nsisConfig"]['OutConsoleFileName'])
        os.remove(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutConsoleFileName'])

###################################################################################################
# Build Script
###################################################################################################

try:
    os.remove(config["buildConfig"]['pythonReleasePath'] + '\\' + config["nsisConfig"]['OutFileName'])
except:
    pass

shutil.rmtree(config["buildConfig"]['pythonReleasePath'] ,ignore_errors=True)

run_command(getNsisFlags(config))
if os.path.isfile(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutFileName']):
    shutil.copyfile(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutFileName'], config['runtime']['outputFolder'] + "\\" + config["nsisConfig"]['OutFileName'])
    os.remove(scriptpath + "\\Runtime\\" + config["nsisConfig"]['OutFileName'])

run_command(extractDefaultPython(config, quoteFolder(scriptpath + '\\Runtime\\Python\\Python' + config["nsisConfig"]['PythonVersion'] + '.7z'), config["buildConfig"]['pythonReleasePath']))

print("############################################################################")
print("# include Temp Liberarys if added from other script")
print("############################################################################")
if os.path.exists(scriptpath + "\\TempLib"):
    copytree(scriptpath + "\\TempLib", config["buildConfig"]['pythonReleasePath'] + '\\Lib')

if os.path.exists(scriptpath + "\\TempDll"):
    copytree(scriptpath + "\\TempDll", config["buildConfig"]['pythonReleasePath'] + '\\DLLs')

shutil.rmtree(scriptpath + '/TempLib' ,ignore_errors=True)
shutil.rmtree(scriptpath + '/TempDll' ,ignore_errors=True)

print("############################################################################")
print("# Drop Files")
print("############################################################################")

dropCacheFiles(config["buildConfig"]['pythonReleasePath'])
dropDocFiles(config["buildConfig"]['pythonReleasePath'])
dropTestFiles(config["buildConfig"]['pythonReleasePath'])
dropDevFiles(config["buildConfig"]['pythonReleasePath'])
dropTKInterTCLFiles(config["buildConfig"]['pythonReleasePath'])
dropBuildFiles(config["buildConfig"]['pythonReleasePath'])

print("############################################################################")
print("# Resolve requirements.txt")
print("############################################################################")

#Requirements not always work -> They e.g. dont worl if MS VC is not installed
#Copy packages is in normal cases the better method

def pip3install(package):
    flags=[]
    flags.append('Release\\Scripts\\pip3.exe')
    flags.append("install")
    flags.append("-I --root " + quoteFolder(config["buildConfig"]['pythonReleasePath'] + '\\Release\\Lib\\site-packages'))

    flags.append(package)
    return(flags)

def parseRequirements(library):
    requirements = open("requirements.txt", "r")
    lines=requirements.readlines()
    for line in lines:
        line = line.strip()
        if not line.startswith("#") and line != "":
            print (line)
            run_command(pip3install(line))

print("############################################################################")
print("# Copy Packages (See Hooks section for e.g. PyQt and other libs that need hooks")
print("############################################################################")

#Setup packages that dont need any Hook - Almost any Python package

#config["packagesArray"].append("PyQt5")
#shutil.rmtree(config["buildConfig"]['pythonReleasePath'] ,ignore_errors=True)

for package in config["packagesArray"]:
    copyLibrary(config["buildConfig"], package)

dropCacheFiles(config["buildConfig"]['pythonReleasePath'])
dropTestFiles(config["buildConfig"]['pythonReleasePath'])

print("############################################################################")
print("# Hooks (like PyQt, Pywin32...")
print("############################################################################")

if "PyQt5" in config["packagesHookArray"]:
    #Sip is always needed

    copytree(os.path.dirname(sys.executable) + '\\Lib\\site-packages\\PyQt5\\plugins\\platforms', config["buildConfig"]['pythonReleasePath'] + '\\DLLs\\PyQt5\\plugins\\platforms')
    shutil.copyfile(os.path.dirname(sys.executable) + '\\Lib\\site-packages\\sip.pyd', config["buildConfig"]['pythonReleasePath'] + '\\DLLs\\sip.pyd')
    for file in config["packagesPyQt5Array"]:
        shutil.copyfile(os.path.dirname(sys.executable) + '\\Lib\\site-packages\\PyQt5\\' + file, config["buildConfig"]['pythonReleasePath'] + '\\DLLs\\PyQt5\\' + file)
    # We use site.py to init Qt -> Ignore
    shutil.copyfile(scriptpath + '\\Runtime\\Python\\qt.conf', config["buildConfig"]['pythonReleasePath'] + '\\qt.conf')
    #msvcp100.dll is needed for PyQt
    shutil.copyfile(scriptpath + '\\Runtime\\Python\\msvcp100.dll', config["buildConfig"]['pythonReleasePath'] + '\\msvcp100.dll')

#Move all .pyd and .dll files to /DLLs
#copyDllFilesExtension(config["buildConfig"], config["buildConfig"]['pythonReleasePath'] + "\\lib",".pyd")
#copyDllFilesExtension(config["buildConfig"], config["buildConfig"]['pythonReleasePath'] + "\\lib",".dll")

print("############################################################################")
print("# Create named interpreter")
print("############################################################################")

if config["buildConfig"]["pythonCustomInterpreter"]:
    run_command(getCybeSystemsIconChangerFlags(config, config["buildConfig"]['pythonReleasePath'], "python.exe", config["buildConfig"]["pythonExeName"]))
    run_command(getCybeSystemsIconChangerFlags(config, config["buildConfig"]['pythonReleasePath'], "pythonw.exe", config["buildConfig"]["pythonWExeName"]))

if config["buildConfig"]['pyFileMinfifier'] != 0:
    # 1: Compile to pyc
    if config["buildConfig"]['pyFileMinfifier'] == True:
        compileall.compile_dir(config["buildConfig"]['pythonReleasePath'],1000, legacy=True, ddir="",optimize=2)
        remove_file_extension(config["buildConfig"]['pythonReleasePath'],".py")
    # 2: PyMinifier
    elif config["buildConfig"]['pyFileMinfifier'] == 2:
        print("############################################################################")
        print("# Create named interpreter")
        print("############################################################################")
        pyminifierFile(config["buildConfig"]['pythonReleasePath'], ".py")

#Replace site.py -> Set Environment variables for PyQt5 etc.
if config["buildConfig"]['useCustomSite.py']:
    os.remove(config["buildConfig"]['pythonReleasePath'] + '\\Lib\\site.py')
    shutil.copyfile(scriptpath + '\\Runtime\\Python\\site.py', config["buildConfig"]['pythonReleasePath'] + '\\Lib\\site.py')

if config["buildConfig"]['zipPythonStdLib'] == True:
    run_command(zipStdLib(config))
    shutil.rmtree(config["buildConfig"]['pythonReleasePath'] + "\\Lib" ,ignore_errors=True)

shutil.copyfile(scriptpath + '\\Runtime\\Python\\msvcr100.dll', config["buildConfig"]['pythonReleasePath'] + '\\msvcr100.dll')
shutil.copyfile(scriptpath + '\\Runtime\\Python\\python34.dll', config["buildConfig"]['pythonReleasePath'] + '\\python34.dll')

print("############################################################################")
print("# Compile Launcher with Nuitka")
print("############################################################################")

if config["buildConfig"]['createNuitkaLauncher'] == True:
    runCommandWithPath(nuitkaCompileMain(quoteFolder(config['runtime']['outputFolder'] + '\\' + config["buildConfig"]['startFile']), config["buildConfig"]), os.path.dirname(sys.executable))
    #runCommandWithPath(nuitkaCompileStandaloneMain(quoteFolder(scriptpath + '\\' + config["buildConfig"]['startFile']), config["buildConfig"]), os.path.dirname(sys.executable))
    shutil.copyfile(config['runtime']['outputFolder'] + '\\' + config["buildConfig"]['startFile'].replace('.py','.exe'), config["buildConfig"]['pythonReleasePath'] + '\\' + config["buildConfig"]['startFile'].replace('.py','.exe'))
    os.remove(config['runtime']['outputFolder'] + '\\' + config["buildConfig"]['startFile'].replace('.py','.exe'))

if config["buildConfig"]['copyStartFile'] == True:
    shutil.copyfile(config['runtime']['outputFolder'] + '\\' + config["buildConfig"]['startFile'], config["buildConfig"]['pythonReleasePath'] + '\\' + config["buildConfig"]['startFile'])

if config["buildConfig"]['useUpx'] == True:
    compressUpx(config, ".dll")
    compressUpx(config,".exe")

if config["buildConfig"]['useCustomSite.py'] == False and config["buildConfig"]['zipPythonStdLib'] == True:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("You use zip for Stdlibs without custom site.py - Make sure to include lib\\site-packages in your init script !")
    print("Sample:")
    print("    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'lib\\site-packages'))")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

if config["buildConfig"]['zipPythonStdLib'] == True and config["buildConfig"]['createNuitkaLauncher']:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("You use zip for Stdlibs and use Nuitka Launcher - Make sure to include lib\\site-packages in your init script !")
    print("Nutika seems to ignore site.py -> Need a workaround for this")
    print("Sample:")
    print("    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'lib\\site-packages'))")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#
###################################################################################################