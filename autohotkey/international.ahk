; Quick combos for non-English letters.
; Left Alt is for Turkish, e.g. Left Alt + U -> Ü
; Right Alt is for Spanish, e.g. Right Alt + U -> Ú

#SingleInstance Force

#NoEnv
#Warn
SendMode Input
SetWorkingDir %A_ScriptDir%


; TURKISH

<!c::
  if GetKeyState("CapsLock", "T")
    Send, Ç
  else
    Send, ç
return

+<!c::
  if GetKeyState("CapsLock", "T")
    Send, ç
  else
    Send, Ç
return

<!g::
  if GetKeyState("CapsLock", "T")
    Send, Ğ
  else
    Send, ğ
return

+<!g::
  if GetKeyState("CapsLock", "T")
    Send, ğ
  else
    Send, Ğ
return

<!i::
  if GetKeyState("CapsLock", "T")
    Send, İ
  else
    Send, ı
return

+<!i::
  if GetKeyState("CapsLock", "T")
    Send, ı
  else
    Send, İ
return

<!o::
  if GetKeyState("CapsLock", "T")
    Send, Ö
  else
    Send, ö
return

+<!o::
  if GetKeyState("CapsLock", "T")
    Send, ö
  else
    Send, Ö
return

<!s::
  if GetKeyState("CapsLock", "T")
    Send, Ş
  else
    Send, ş
return

+<!s::
  if GetKeyState("CapsLock", "T")
    Send, ş
  else
    Send, Ş
return

<!u::
  if GetKeyState("CapsLock", "T")
    Send, Ü
  else
    Send, ü
return

+<!u::
  if GetKeyState("CapsLock", "T")
    Send, ü
  else
    Send, Ü
return


; SPANISH

>!a::
  if GetKeyState("CapsLock", "T")
    Send, Á
  else
    Send, á
return

+>!a::
  if GetKeyState("CapsLock", "T")
    Send, á
  else
    Send, Á
return

>!e::
  if GetKeyState("CapsLock", "T")
    Send, É
  else
    Send, é
return

+>!e::
  if GetKeyState("CapsLock", "T")
    Send, é
  else
    Send, É
return

>!i::
  if GetKeyState("CapsLock", "T")
    Send, Í
  else
    Send, í
return

+>!i::
  if GetKeyState("CapsLock", "T")
    Send, í
  else
    Send, Í
return

>!n::
  if GetKeyState("CapsLock", "T")
    Send, Ñ
  else
    Send, ñ
return

+>!n::
  if GetKeyState("CapsLock", "T")
    Send, ñ
  else
    Send, Ñ
return

>!o::
  if GetKeyState("CapsLock", "T")
    Send, Ó
  else
    Send, ó
return

+>!o::
  if GetKeyState("CapsLock", "T")
    Send, ó
  else
    Send, Ó
return

>!u::
  if GetKeyState("CapsLock", "T")
    Send, Ú
  else
    Send, ú
return

+>!u::
  if GetKeyState("CapsLock", "T")
    Send, ú
  else
    Send, Ú
return

>!?::
  Send, ¿
return

>!!::
  Send, ¡
return

>!<::
  Send, «
return

>!>::
  Send, »
return

>!-::
  Send, —
return
