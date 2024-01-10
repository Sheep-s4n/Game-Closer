Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "python main.py"
oShell.Run strArgs, 0, false