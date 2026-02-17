Dim shell, fso, projectRoot, batPath, cmd
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

projectRoot = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
batPath = projectRoot & "\scripts\iniciar_erp.bat"

cmd = "cmd /c """ & batPath & """"

' 0 = hidden window, False = don't wait
shell.Run cmd, 0, False
