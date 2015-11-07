; =================================================================
; CybeSystems Python Environment Launcher
; Copyright (c) 2015 CybeSystems
;
; This file is needed to create a "Bootstrapper" for Python
;
; Use the provided pyhton build script
; 
; Override this defines with Commandline Switches:
;
; Sample:
; makensis.exe /DPythonVersion=34 /DProductVersion=1.1.1.1 /DProductName=YOURPRODUCTNAME /DFileDescription=YOURDESCRIPTION /DFileVersion=1.1.1.1 /DInternalName=YOURPRODUCTNAME /DOriginalFilename=YOURPRODUCTNAME.exe CybeSystemsPortable.nsi
;
; http://www.cybesystems.com
; =================================================================

!include 'TextFunc.nsh'
!include 'FileFunc.nsh'
!include 'WinMessages.nsh'
!include 'LogicLib.nsh'
!include 'StrFunc.nsh'

!verbose 0
; **************************************************************************
; === Define constants ===
; **************************************************************************
!ifndef FileIcon
	!define FileIcon "appicon.ico"
!endif 
;!define PythonVersion "34"
;!define ProductVersion 1.0.0.0
;!define ProductName "ProductName"
;!define FileDescription "FileDescription"
;!define FileVersion 1.0.0.0
;!define InternalName "InternalName"
;!define OriginalFilename "OriginalFilename"

!define PYTHON_STARTUP "$EXEDIR\helloworld.py"
; **************************************************************************
; === Best Compression ===
; **************************************************************************
SetCompressor /SOLID lzma
SetCompressorDictSize 32

; **************************************************************************
; === Set version information ===
; **************************************************************************
Caption "${ProductName}"
VIProductVersion "${ProductVersion}"
VIAddVersionKey ProductName "${ProductName}"
VIAddVersionKey FileDescription "${FileDescription}"
VIAddVersionKey FileVersion "${FileVersion}"
VIAddVersionKey ProductVersion "${ProductVersion}"
VIAddVersionKey InternalName "${InternalName}"
VIAddVersionKey OriginalFilename "${OriginalFilename}"

; **************************************************************************
; === Includes ===
; **************************************************************************
!insertmacro GetParameters

; **************************************************************************
; === Runtime Switches ===
; **************************************************************************
WindowIcon Off
SilentInstall Silent
AutoCloseWindow True
RequestExecutionLevel user

; **************************************************************************
; === Set basic information ===
; **************************************************************************
Name "${ProductName}"
OutFile "${ProductName}Portable.exe"
Icon "${FileIcon}"

; **************************************************************************
; ==== Running ====
; **************************************************************************

Section "Main"
	Call Launch
SectionEnd


; **************************************************************************
; === Run Application ===
; **************************************************************************

;Launch with make ${FILENAME}
Function Launch
	${GetParameters} $0 	; Read command line parameters
	;ReadIniStr ${TEMP1} 'Launcher.ini' 'Example1' 'Example1Test'
	 
	 ;IntCmp $1 1 +3
	;Check CybeSystems.exe itself (without x86, x64)
	IfFileExists "$EXEDIR\Python${PythonVersion}\python.exe" OneFolder
	OneFolder:

		!define PYTHON_PATH "$EXEDIR\Python${PythonVersion}"

		StrCpy $R0 "$R0${PYTHON_PATH}"
		StrCpy $R1 "$R1${PYTHON_STARTUP}"

		System::Call 'Kernel32::SetEnvironmentVariable(t "PYTHONPATH",t R0)i' 	; Set PYTHONPATH temporarily
		System::Call 'Kernel32::SetEnvironmentVariable(t "PYTHONSTARTUP",t R1)i'			; Set Python prompt temporarily	
		SetOutPath "$EXEDIR"
		Exec "$EXEDIR\Python${PythonVersion}\python.exe" 	; EXEC app with parameters	
		goto end_of_test ;<== important for not continuing on the else branch

			
	PastMissingCheck:
		MessageBox MB_OK|MB_ICONEXCLAMATION `${ProductName} was not found in $EXEDIR`
	end_of_test:
FunctionEnd