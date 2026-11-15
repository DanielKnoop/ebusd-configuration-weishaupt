# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Daniel Knoop
# Uhr des Raumgeraets (Heizkreisregler 1, Slave 35) – nicht in der Weishaupt-Config, per ID-Suchlauf gefunden (30.10.2026).
# Schreiben nur mit Absender 00: ebusctl write -s 00 -c hc1 ClockMinute 8
# type (r;w;u;1-9),class,name,comment,QQ,ZZ,PBSB,ID,field1,part (m;s),type / templates,divider / values,unit,comment,field2,part (m;s),type / templates,divider / values,unit,comment
*r,,,,,,"0902",,,,,,,
*w,,,,,,"0903",,,,,,,
r,,ClockTime,Uhrzeit Raumgeraet ,,,,"090002",Hour,,UCH,,,Stunde,Minute,,UCH,,,Minute
r,,ClockWeekday,Wochentag Raumgeraet ,,,,"210102",,,UIN,,,Mo=1
w,,ClockWeekday, ,,,,"2101",,,UIN,,,
r,,ClockDay,Tag Raumgeraet ,,,,"220102",,,UIN,,,
w,,ClockDay, ,,,,"2201",,,UIN,,,
r,,ClockMonth,Monat Raumgeraet ,,,,"230102",,,UIN,,,
w,,ClockMonth, ,,,,"2301",,,UIN,,,
r,,ClockYear,Jahr Raumgeraet ,,,,"240102",,,UIN,,,zweistellig
w,,ClockYear, ,,,,"2401",,,UIN,,,
r,,ClockHour,Stunde Raumgeraet ,,,,"250102",,,UIN,,,
w,,ClockHour, ,,,,"2501",,,UIN,,,
r,,ClockMinute,Minute Raumgeraet ,,,,"260102",,,UIN,,,
w,,ClockMinute, ,,,,"2601",,,UIN,,,
