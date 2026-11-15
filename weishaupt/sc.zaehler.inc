# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Daniel Knoop
# type (r;w;u;1-9),class,name,comment,QQ,ZZ,PBSB,ID,field1,part (m;s),type / templates,divider / values,unit,comment,field2,...
# WTC-Info I40/I41 aus Bank 3 Adresse F0, Lesebefehl 5000 03 (F0^98) B3 F0, siehe ../docs/wtc.md
# Nur Lesen. I40 = Schaltspielzähler Brenner seit Reset (0..999, big-endian), I41 = Brennerstunden seit Reset.
*r,,,,,,"5000",,,,,,,
r9,,Zaehler,WTC-Info I40/I41,,,,"68B3F0",,s,IGN:5,,,,StartsSinceReset,s,UIR,,,I40: Schaltspielzähler Brenner seit Reset,HoursSinceReset,s,UCH,,h,I41: Betriebsstunden Brenner seit Reset
