; Quick combos for apostrophes and quotes

#NoEnv
#Warn
SendMode Input
SetWorkingDir %A_ScriptDir%


; Alt+Single Quote is Apostrophe
<!'::
  Send, ’
return

; Alt+Left Bracket is Left Single Quote
<![::
  Send, ‘
return

; Alt+Right Bracket is Right Single Quote
<!]::
  Send, ’
return

; Shift+Alt+Left Bracket is Left Double Quote
+<![::
  Send, “
return

; Shift+Alt+Right Bracket is Right Double Quote
+<!]::
  Send, ”
return
