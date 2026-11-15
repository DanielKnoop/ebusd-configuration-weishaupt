# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Daniel Knoop
# type (r;w;u;1-9),class,name,comment,QQ,ZZ,PBSB,ID,field1,part (m;s),type / templates,divider / values,unit,comment,field2,...
# WTC-Fachmannparameter aus dem EEPROM (Bank 2), Lesebefehl 5000 03 (Adr^C4) B2 Adr, siehe ../docs/wtc.md
# Nur Lesen. Leistungen sind als abgerundet(% x 2,55) gespeichert; P51 vermutlich -(Roh+3), P53 = -Roh.
*r,,,,,,"5000",,,,,,,
r9,,Fachmann1,WTC-Fachmannparameter 0x17-0x22,,,,"D3B217",,s,IGN:1,,,,P31,s,UCH,,°C,Max. Vorlaufsollwert,P32,s,UCH,,,Schaltdifferenz Vorlauf (±K),P34,s,BI0:5,,min,Brenner-Taktsperre,,s,IGN:2,,,,P36Raw,s,UCH,,,Min. Kesselleistung (% x 2.55),,s,IGN:1,,,,P37Raw,s,UCH,,,Max. Leistung Heizung (% x 2.55),P41,s,BI0:4,,min,Pumpennachlaufzeit,,s,IGN:1,,,,P52,s,UCH,,min,Max. WW-Ladezeit,P51Raw,s,BI0:4,,,Schaltdifferenz WW (vermutlich -(Roh+3) K)
r9,,Fachmann2,WTC-Fachmannparameter 0x23-0x2E,,,,"E7B223",,s,IGN:1,,,,P50,s,UCH,,,Vorlaufüberhöhung WW (K),P38Raw,s,UCH,,,Max. Leistung Warmwasser (% x 2.55),,s,IGN:6,,,,P53Raw,s,UCH,,,Speicher-Absenkung (Betrag K),,s,IGN:2,,,,P20,s,SCH,,,Korrektur Außenfühler (K)
