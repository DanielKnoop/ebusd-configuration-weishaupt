# eBUS-Konfiguration für Weishaupt WTC, WCM-FB und WRSol

Dieser Fork erweitert die [Weishaupt-Konfiguration von J0EK3R](https://github.com/J0EK3R/ebusd-configuration-weishaupt)
für [ebusd](https://github.com/john30/ebusd). Er enthält CSV-Gerätedefinitionen,
keine Firmware und keine vollständige Home-Assistant-Konfiguration.

## Getesteter Aufbau

| Gerät | Busadresse | Definition | Erprobung |
|---|---|---|---|
| Weishaupt WTC 15-A, Ausführung W | f1 / f6 | `weishaupt/f6..sc.csv` | Status, Fachmannparameter und I40/I41 |
| Raumgerät WCM-FB, Identifikation Kromschröder „W“, SW 9634 | 30 / 35 | `weishaupt/35..hc1.csv` | Sollwerte, Uhr, ausgewählte Parameter |
| WRSol, Herstellerkennung TEM, SW 2422 | f7 / fc | `tem/fc.wrsol.csv` | Temperatur- und Prozesswerte; Einschränkungen unten |

Die Ergänzungen wurden mit ebusd 26.1 erprobt. Andere Geräte und Firmwarestände
sind nicht bestätigt. Weitere vom Ursprungsprojekt unterstützte Geräte bleiben
enthalten; sie wurden für diesen Fork nicht neu geprüft.

## Ergänzungen gegenüber dem Ursprungsprojekt

- WTC-Broadcast `sc Act`: Flamme, Pumpe und Fehler als `off/on`, Last in Prozent,
  gedämpfte Außentemperatur sowie das abgeleitete Feld `HeatingActive`.
- WTC-Fachmannparameter: zwei ausschließlich lesende EEPROM-Abfragen mit Rohwerten
  und dokumentierten Umrechnungen.
- WTC-Zähler I40/I41: Brennerstarts und Brennerstunden seit Rückstellung.
- WCM-FB: passives Dekodieren der Sollwerttelegramme und des Zeit-Broadcasts,
  Lesen und Stellen der Uhr, gezielte Poll-Prioritäten ausgewählter Werte.
- WRSol: Definitionen für Temperaturen, Pumpendrehzahl, Solarertrag und Fehlerregister.
- Bestehender Parserfehler in `sc.manufacturer.inc`: drei nicht definierte
  `temp0`-Verweise durch das vorhandene Template `_8_Temp0` ersetzt. Die
  betreffenden Herstellerfelder wurden am Gerät nicht neu validiert.

Details: [WTC](docs/wtc.md), [WCM-FB und Betrieb](docs/betrieb.md).

## Sicherheit und Grenzen

Die Definitionen greifen in die Kommunikation mit einer Heizungsanlage ein.
Falsche Definitionen oder Schreibzugriffe können den Betrieb beeinträchtigen.
Es gilt der Gewährleistungsausschluss der [GPL v3](LICENSE).

- **WTC-Fachmannparameter niemals per eBUS schreiben.** Die neuen Definitionen
  lesen ausschließlich. Änderungen am Gerät gehören in fachkundige Hände;
  Parameterblöcke enthalten auch Sicherheitswerte und Prüfsummen.
- **Keine rohen WTC-Speicherabfragen auf Bank 0.** Solche Abfragen haben bei der
  Erprobung einen Neustart ausgelöst. Keine Suchläufe oder schnellen Wiederholungen.
- Das WCM-FB antwortet teils erst nach mehreren Anfragen. Polling sparsam halten.
- Vorhandene `w`-Definitionen können Einstellungen ändern. Wer ausschließlich
  beobachten möchte, betreibt ebusd mit `--readonly` und prüft dessen Verhalten
  anhand der [ebusd-Dokumentation](https://github.com/john30/ebusd/wiki/2.-Run).
- Niemals einen zweiten Master mit Adresse `30` betreiben, solange das Raumgerät
  angeschlossen ist. Eine Raumgerät-Emulation ist nicht Teil dieses Forks.

## Installation

Die Dateien werden lokal über `--configpath` verwendet. Sie sind kein Ersatz für
alle Dateien einer vorhandenen ebusd-Installation. Vor Änderungen die bestehende
Konfiguration und die Startoptionen sichern; Zugangsdaten separat behalten.

```sh
git clone https://github.com/DanielKnoop/ebusd-configuration-weishaupt.git
cd ebusd-configuration-weishaupt
ebusd --checkconfig --scanconfig=off --configpath="$PWD"
```

`--checkconfig` prüft die Definitionen und beendet sich, ohne den Bus zu öffnen.
**Bekannte Einschränkung:** Der vollständige Altbestand enthält in den nur von
Adresse `08` eingebundenen Prozesswerten überlange Nachrichten-IDs. ebusd 26.1
beendet die Gesamtprüfung deshalb mit `max message ID length exceeded` und Status 1.
Die Prüfung ohne diese alte Definition besteht; eine Anleitung für eine
unveränderte Arbeitskopie steht unter [Konfigurationsprüfung](docs/betrieb.md#konfigurationsprüfung).
Für den regulären Betrieb `--configpath=/absoluter/pfad/ebusd-configuration-weishaupt`
und `--scanconfig` in die vorhandenen Startoptionen aufnehmen. Adapter-, MQTT-
und Netzwerkparameter hängen von der eigenen Installation ab.

Der Symlink `kromschroeder -> weishaupt` gehört zum Ursprungsprojekt und wird für
die Herstellerzuordnung benötigt. Beim Kopieren muss er erhalten bleiben.

Nach dem Laden lassen sich beispielsweise folgende Werte lesen:

```sh
ebusctl read -c sc Act
ebusctl read -c sc Zaehler
ebusctl read -c sc Fachmann1
ebusctl read -c hc1 ClockTime
ebusctl read -c WRSol TKO
```

`sc Act` wird passiv empfangen; zunächst einen Broadcast abwarten. Aktive
Leseabfragen setzen einen passenden Adapter und eine geladene Gerätedefinition voraus.
Weitere Hinweise zum Scan, zu Adresse `08` und zum Polling: [Betrieb](docs/betrieb.md).

## WRSol: bekannte Grenzen

Die RAM-Adressen stammen aus der Weishaupt-Protokolldokumentation
„Implementierte eBUS-Befehle der Weishaupt-Geräte“, Kapitel 11 (WRSol 2.40).
Das Herstellerdokument wird hier nicht mitverteilt.

Die Definitionen sind mit SW 2422 in Betrieb. `TSO` und `TSU` können je nach
Fühlerbestückung identische Werte liefern. Solarleistung, Pumpendrehzahl und
`TKOMax` sind noch nicht abschließend unter sonnigen Bedingungen plausibilisiert.
Die Skalierung dieser Werte daher vor weiterer Verwendung am eigenen Gerät prüfen.

## Herkunft und Lizenz

Die ursprünglichen Weishaupt-Definitionen und ihre Git-Historie stammen von
[J0EK3R und den Mitwirkenden](https://github.com/J0EK3R/ebusd-configuration-weishaupt).
Deren Hinweise und Dokumentation bleiben erhalten; die bisherige README liegt
unter [docs/upstream-readme.md](docs/upstream-readme.md).

Die neuen Definitionen und die Dokumentation dieses Forks stammen von Daniel Knoop
(2026) und werden ebenfalls unter **GNU GPL Version 3** veröffentlicht. Der
ursprüngliche [Lizenztext](LICENSE) bleibt unverändert. Bestehende Urheberhinweise
bleiben bestehen. Es besteht keine Verbindung zum Gerätehersteller.

## Beiträge

Bei Fehlerberichten bitte Gerätetyp, Firmware, ebusd-Version, betroffene Definition
und einen kurzen, bereinigten Telegrammausschnitt angeben. Keine Zugangsdaten,
vollständigen Anlagenmitschnitte oder persönlichen Verbrauchsverläufe veröffentlichen.
Bestätigte Zuordnungen und Vermutungen bitte klar unterscheiden.
