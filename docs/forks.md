# Abgleich mit anderen Forks

Stand: 15.11.2026. Verglichen wurden die 14 anderen direkten Forks des
Ursprungsprojekts einschließlich ihrer Branches. Acht enthielten keine
zusätzlichen Commits. Die folgenden Erkenntnisse wurden gezielt bewertet;
ein vollständiger Merge eines fremden Forks findet nicht statt.

## Übernommen: vollständige Auswahl der Urlaubstage

[NGallmann, Commit 9a659d1](https://github.com/NGallmann/ebusd-configuration-weishaupt/commit/9a659d11111bfc3cbb93e9d79863709c865b9a97)
ergänzt `_16_HolidayDay` um die Einträge 1 bis 31 zusätzlich zu `0=Off`.
Diese Änderung ist übernommen. Vorher konnte ebusd solche Tage bereits als
Zahl dekodieren; die Ergänzung vervollständigt die aufgezählten Auswahlwerte.

Gespeicherte Antworten eines WCM-FB SW 9634 enthalten gültige Urlaubstage mit
16-Bit-Little-Endian-Kodierung. Die neue Liste wurde mit dem ebusd-26.1-Dekoder
und -Encoder für alle 32 Werte (`Off`, 1–31) in beide Richtungen geprüft
(64 Prüfungen). Ein tatsächlicher Schreibzugriff oder eine
Aktivierung des Urlaubsprogramms wurde nicht getestet und nicht ausgeführt.

## Übernommen und offline bestätigt: zwei Prüfbyte-Verfahren

Quelle ist [aghulas, Stand b9f0acc](https://github.com/aghulas/ebusd-configuration-weishaupt/tree/b9f0accf4980a8fa74bec661dbccff09c7daa60a),
insbesondere die [Telegramm-CRC](https://github.com/aghulas/ebusd-configuration-weishaupt/blob/b9f0accf4980a8fa74bec661dbccff09c7daa60a/diag/calculate_weishaupt_crc.py)
und die [Beschreibung der Parameterblöcke](https://github.com/aghulas/ebusd-configuration-weishaupt/blob/b9f0accf4980a8fa74bec661dbccff09c7daa60a/catalog/README.md).
Die Arbeit von aghulas liefert die Algorithmen; der Abgleich mit der WTC 15
und das kleine Offline-Werkzeug stammen aus diesem Fork. Lizenz: GPL v3.

### Telegramm-CRC

Das erste Nutzbyte nach dem Prüfbyte bildet den Startwert. Vor jedem weiteren
Nutzbyte wird achtmal nach links geschoben (Polynom `0x5C`), anschließend wird
das nächste Byte per XOR eingerechnet. Es gibt kein abschließendes Komplement.

Für die kurzen WTC-Leseanfragen erklärt das die bisher empirisch ermittelten
Schlüssel: `CRC(B2, Adresse) = 0xC4 XOR Adresse`, entsprechend `B1 → 0x20`
und `B3 → 0x98`. Offline bestätigt an **52 erfolgreichen früheren Leseantworten**
einer WTC 15 sowie **66 aktiven 5000-Lesedefinitionen** dieses Forks; keine
CRC-Abweichung. Fehlgeschlagene Abfragen und Bank 0 wurden beim historischen
Abgleich nicht als Belege gezählt.

### Parameterblock-Prüfbyte

Dieses Verfahren ist von der Telegramm-CRC zu unterscheiden: Startwert 0,
pro Blockbyte einmal verdoppeln, bei Überlauf das reduzierte Byte mit `0x21`
verknüpfen, dann das Datenbyte per XOR einrechnen. Abschließend `0xFF - Wert`.
Das Prüfbyte selbst gehört nicht zum Block, über den gerechnet wird.

Für die WTC 15 passt das Verfahren zum Fachmannblock `0x17–0x3B` mit Prüfbyte
an `0x3C`: **fünf von fünf Übereinstimmungen** mit dem Ausgangsstand und vier
bereits dokumentierten Parameteränderungsfällen. Das sind historische Abgleiche,
keine fünf neu ausgeführten Geräteversuche. Im gespeicherten Ausgangsdump fehlt
das Prüfbyte; sein Vergleichswert stammt aus den damaligen Versuchsnotizen.
Persönliche Dumps und Anlagenwerte werden hier nicht mitverteilt.

Das bestätigt das Rechenverfahren für diesen Block. Es bestätigt weder die
Speicheradressen anderer Firmwarestände noch einen sicheren Schreibweg.
**WTC-Parameter bleiben ausschließlich lesend.**

### Werkzeug und Tests

[tools/weishaupt_crc.py](../tools/weishaupt_crc.py) rechnet lokal, ohne Netzwerk,
ebusd-Prozess oder Gerät. Es erzeugt keine vollständigen Schreibtelegramme.

```sh
python3 tools/weishaupt_crc.py telegramm B217
# D3
python3 tools/weishaupt_crc.py block '80 00'
# DE – synthetischer Zweibyteblock
python3 -m unittest discover -s tests -v
```

Die Tests umfassen bekannte kurze und verkettete Telegramme, alle 256 Adressen
für sechs dokumentierte Kurzabfrage-Schlüssel, synthetische Blockprüfungen und
die gepflegten 5000-Lesedefinitionen. Rohdaten privater Anlagen sind nicht nötig.

## Bestätigte Erkenntnis, bestehende Definitionen noch unverändert

Die [Reglernotizen von aghulas](https://github.com/aghulas/ebusd-configuration-weishaupt/blob/b9f0accf4980a8fa74bec661dbccff09c7daa60a/catalog/README.md)
beschreiben Zeitfenster ebenfalls als **Ende, Start** in Viertelstunden,
mit `80 80` für ein leeres Fenster. Das stimmt mit den vorhandenen WCM-FB-
Aufzeichnungen und dem früheren Displayabgleich überein. Die bisherigen
Timer-Templates sind weiterhin vertauscht beschriftet (siehe [Betrieb](betrieb.md)).
Eine Korrektur wird hier noch nicht auf alle unterstützten Regler ausgedehnt;
die ursprünglichen Includes werden auch für andere Geräte verwendet.

## Nicht übernommen: anderes WTC-Speicherlayout und Reglerfamilien

Die [WTC-Notizen von aghulas](https://github.com/aghulas/ebusd-configuration-weishaupt/blob/b9f0accf4980a8fa74bec661dbccff09c7daa60a/notes/wtc-writes.md)
nennen als erprobtes Gerät eine WTC 250 mit Firmware 11.0e. Der Katalog führt
den Fachmannblock bei `0x01B–0x050` mit Prüfbyte `0x051`; bei unserer WTC 15
liegt er bei `0x17–0x3B` mit Prüfbyte `0x3C`. Eine pauschale Adressverschiebung
ist nicht belegt. Auch Skalierungen von Leistungswerten unterscheiden sich.

- **Fehlerhistorie:** `wtc.history.inc` beschreibt sechs Plätze ab EEPROM
  `0x0202` und Fehlerzähler ab `0x0196`. Der vorhandene WTC-15-Dump enthält nur
  die kurze Bank-2-Adressierung im Bereich `0x00–0xFF`; diese Ziele sind damit
  nicht abgedeckt. Kein Nachweis für unsere Firmware, keine Übernahme oder Abfrage.
- **Regler und Uhr:** KA/EM/FS-Definitionen und Schreiben von Adresse `ff`
  betreffen die dortige Anlage. Am WCM-FB SW 9634 ist Absender `00` erprobt.
  Auch das Übernehmen fremder Zeit-Broadcasts unterscheidet sich.
- **Urlaubstemperatur:** `HolidayTempLevel` an `3D01` ist dort als Moduswahl
  korrigiert. Unser WCM-FB verwendet dafür bereits `2D01` mit `_16_TempReduced`.
  Die zusätzlichen FS-Register werden nicht ungeprüft aufgenommen.
- **Wochentag:** Montag=1 stimmt mit unseren Uhren-Definitionen überein;
  daraus ergibt sich bei uns keine zusätzliche Änderung.
- **Schreibzugriffe:** Aus den fremden Speicher-Schreibversuchen wird keine
  Schreibdefinition übernommen. Prüfsummenkenntnis hebt diese Grenze nicht auf.

## Weitere Forks

[guido4096](https://github.com/guido4096/ebusd-configuration-weishaupt)
hat den `temp0`-Verweis bereits korrigiert; dieselbe Korrektur war beim ersten
Konfigurationscheck dieses Forks unabhängig aufgefallen und ist hier enthalten.
Die dortige Umbenennung `_8_Time…` in `_7_Time…` ändert den Datentyp `TTQ` nicht
und behebt insbesondere nicht die vertauschte Reihenfolge der Zeitfenster.
Sie wird deshalb nicht als funktionale Korrektur übernommen.

Der zusätzliche `hwc.expert2.inc`-Include auf dem Branch `patch-1` von
[jmm-neuv](https://github.com/jmm-neuv/ebusd-configuration-weishaupt/tree/patch-1)
verweist auf eine dort fehlende Datei und wird nicht übernommen. Die übrigen
Änderungen (Übersetzungen, Diagramme) lösen hier kein zusätzliches Geräteproblem.

## Konfigurationsprüfung

Mit ebusd 26.1.26.1 wurden die Identifikationen der drei getesteten Geräte
jeweils einzeln offline eingespeist (`--checkconfig --scanconfig --inject=stop`):
WCM-FB lädt 291 Nachrichten, WTC f6 lädt 23 und WRSol lädt 13, jeweils Status 0.
Die Gesamtprüfung ohne die alte Adresse-08-Definition besteht ebenfalls
(3312 Nachrichten einschließlich Hersteller-Aliasdateien). Die bekannte
Einschränkung der Gesamtprüfung mit Adresse 08 bleibt bestehen.
