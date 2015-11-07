#NoTrayIcon
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=appicon.ico
#AutoIt3Wrapper_UseUpx=n
#AutoIt3Wrapper_Res_Description=CygwinPortable
#AutoIt3Wrapper_Res_Fileversion=0.8.0.0
#AutoIt3Wrapper_Res_ProductVersion=0.8
#AutoIt3Wrapper_Res_LegalCopyright=CybeSystems
#AutoIt3Wrapper_Res_Language=1031
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
#Region AutoIt3Wrapper directives section
;===============================================================================================================
;** AUTOIT3 settings
#AutoIt3Wrapper_Run_Debug_Mode=n                ;(Y/N)Run Script with console debugging. Default=N
;===============================================================================================================
;** AUT2EXE settings
;===============================================================================================================
;** Target program Resource info
;===============================================================================================================
; Obfuscator
;===============================================================================================================

#Include <WinAPIEx.au3>

Func _ChangeIconResource($sTarget, $sIcon)
    If IsAdmin() = 0 Then
        ConsoleWrite("This might fail, due to the lack of privilege!")
        SetError(1)
    EndIf

    Local $tagICONRESDIR = 'byte Width;byte Height;byte ColorCount;byte Reserved;ushort Planes;ushort BitCount;dword BytesInRes;ushort IconId;'
    Local $tagNEWHEADER = 'ushort Reserved;ushort ResType;ushort ResCount;'

    Local $tIcon = DllStructCreate('ushort Reserved;ushort Type;ushort Count;byte[' & (FileGetSize($sIcon) - 6) & ']')
    Local $pIcon = DllStructGetPtr($tIcon)
    Local $hFile = _WinAPI_CreateFile($sIcon, 2, 2)
    Local $iBytes = 0
    _WinAPI_ReadFile($hFile, $pIcon, DllStructGetSize($tIcon), $iBytes)
    _WinAPI_CloseHandle($hFile)

    $hUpdate = _WinAPI_BeginUpdateResource($sTarget)
    Local $iCount = DllStructGetData($tIcon, 'Count')
    Local $tDir = DllStructCreate($tagNEWHEADER & 'byte[' & (14 * $iCount) & ']')
    Local $pDir = DllStructGetPtr($tDir)
    DllStructSetData($tDir, 'Reserved', 0)
    DllStructSetData($tDir, 'ResType', 1)
    DllStructSetData($tDir, 'ResCount', $iCount)
    Local $tInfo, $iSize, $tData, $ID = 400
    For $i = 1 To $iCount
        $tInfo = DllStructCreate('byte Width;byte Heigth;byte Colors;byte Reserved;ushort Planes;ushort BPP;dword Size;dword Offset', $pIcon + 6 + 16 * ($i - 1))
        $iSize = DllStructGetData($tInfo, 'Size')
        _WinAPI_UpdateResource($hUpdate, $RT_ICON, $ID, 0, $pIcon + DllStructGetData($tInfo, 'Offset'), $iSize)
        $tData = DllStructCreate($tagICONRESDIR, $pDir + 6 + 14 * ($i - 1))
        DllStructSetData($tData, 'Width', DllStructGetData($tInfo, 'Width'))
        DllStructSetData($tData, 'Height', DllStructGetData($tInfo, 'Heigth'))
        DllStructSetData($tData, 'ColorCount', DllStructGetData($tInfo, 'Colors'))
        DllStructSetData($tData, 'Reserved', 0)
        DllStructSetData($tData, 'Planes', DllStructGetData($tInfo, 'Planes'))
        DllStructSetData($tData, 'BitCount', DllStructGetData($tInfo, 'BPP'))
        DllStructSetData($tData, 'BytesInRes', $iSize)
        DllStructSetData($tData, 'IconId', $ID)
        $ID += 1
    Next

    _WinAPI_UpdateResource($hUpdate, $RT_GROUP_ICON, 'MAINICON', 0, $pDir, DllStructGetSize($tDir))
    _WinAPI_EndUpdateResource($hUpdate)
 EndFunc   ;==>_ChangeIconResource

ConsoleWrite($CmdLine[0])
;FileCopy ("python.exe", "python2.exe")
FileCopy ($CmdLine[1], $CmdLine[2])

;_ChangeIconResource("python2.exe","appicon.ico")
_ChangeIconResource($CmdLine[2],$CmdLine[3])

