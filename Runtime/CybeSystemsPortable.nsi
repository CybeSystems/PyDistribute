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
!ifndef PythonVersion
	!define PythonVersion "34"
!endif

!ifndef OutFileName
	!define OutFileName "TestApplicationPortable.exe"
!endif
	
!ifndef ProductName
	!define ProductName "TestApplication"
!endif
!ifndef Comments
	!define Comments "A test comment"
!endif
!ifndef CompanyName
	!define CompanyName "Your company"
!endif
!ifndef LegalCopyright
	!define LegalCopyright "© Your company"
!endif
!ifndef FileDescription
	!define FileDescription "Test Application Description"
!endif
!ifndef ProductVersion
	!define ProductVersion "1.0.0.0"
!endif
!ifndef InternalName
	!define InternalName ""
!endif
!ifndef LegalTrademarks
	!define LegalTrademarks ""
!endif
!ifndef OriginalFilename
	!define OriginalFilename ""
!endif
!ifndef PrivateBuild
	!define PrivateBuild ""
!endif
!ifndef SpecialBuild
	!define SpecialBuild ""
!endif
!ifndef PyFolder
	!define PyFolder "Python"
!endif 
!ifndef PyStartFile
	!define PyStartFile "PyQt5HelloWorld.py"
!endif 
!ifndef ConsoleMode
	!define ConsoleMode "1"
!endif 

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
VIAddVersionKey Comments "${Comments}"
VIAddVersionKey CompanyName "${CompanyName}"
VIAddVersionKey LegalCopyright "${LegalCopyright}"
VIAddVersionKey FileDescription "${FileDescription}"
VIAddVersionKey FileVersion "${FileVersion}"
VIAddVersionKey ProductVersion "${ProductVersion}"
VIAddVersionKey InternalName "${InternalName}"
VIAddVersionKey LegalTrademarks "${LegalTrademarks}"
VIAddVersionKey OriginalFilename "${OriginalFilename}"
VIAddVersionKey PrivateBuild "${PrivateBuild}"
VIAddVersionKey SpecialBuild "${SpecialBuild}"

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
OutFile "${OutFileName}"
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
	
	IfFileExists "$EXEDIR\${PyFolder}\python.exe" OneFolder
	OneFolder:
		
		!define PYTHON_PATH "$EXEDIR\${PyFolder}"

		;StrCpy $R0 "$R0${PYTHON_PATH}"
		;StrCpy $R1 "$R1${PyStartFile}"

		;System::Call 'Kernel32::SetEnvironmentVariable(t "PYTHONPATH",t R0)i' 	; Set PYTHONPATH temporarily
		;System::Call 'Kernel32::SetEnvironmentVariable(t "PYTHONSTARTUP",t R1)i'			; Set Python prompt temporarily	
		;SetOutPath "$EXEDIR"
		${If} ${ConsoleMode} == "1"
			Exec "cmd.exe /K $EXEDIR\${PyFolder}\python.exe ${PyStartFile}" 	; EXEC app with parameters	
		${Else}
			Exec "$EXEDIR\${PyFolder}\pythonw.exe ${PyStartFile}" 	; EXEC app with parameters	
		${EndIf}
		goto end_of_test ;<== important for not continuing on the else branch

			
	PastMissingCheck:
		MessageBox MB_OK|MB_ICONEXCLAMATION `${ProductName} was not found in $EXEDIR`
	end_of_test:
FunctionEnd