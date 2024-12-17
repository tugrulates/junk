; Swaps Win and Ctrl keys so it's more like Mac on Windows.

#SingleInstance Force

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

RAlt::RCtrl
RCtrl::RAlt
LCtrl::LWin
LWin::LAlt
LAlt::LCtrl
