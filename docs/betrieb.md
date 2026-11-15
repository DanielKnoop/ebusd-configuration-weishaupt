# WCM-FB und Betriebshinweise

## Raumgerät WCM-FB

Die Ergänzungen wurden mit dem Gerät an Masteradresse 30 / Slaveadresse 35,
Softwarestand 9634, erprobt.

- `hc1 Set` dekodiert das etwa alle 20 Sekunden vom Raumgerät an die WTC
  gesendete Telegramm `30 f1 0507` passiv als Typ `u`.
- `hc1 DateTime` dekodiert den Zeit-Broadcast `30 fe 0700` mit Außentemperatur,
  Uhrzeit und Datum.
- `hc.clock.inc` ergänzt `ClockTime` (Stunde/Minute, nur lesen) sowie
  `ClockWeekday`, `ClockDay`, `ClockMonth`, `ClockYear`, `ClockHour`, `ClockMinute`.
  Der Wochentag ist Montag=1, das Jahr zweistellig.

Die Einzelwerte der Uhr sind les- und schreibbar. Die erprobten Schreibzugriffe
funktionieren nur mit Absenderadresse `00`. Von `31` oder `10` kann das Gerät
antworten, ohne den Wert zu übernehmen. Änderungen deshalb immer zurücklesen.
Schreibbefehle nicht unbeabsichtigt über MQTT oder Automationen freigeben.

Das Gerät besitzt im erprobten Aufbau keine Gangreserve und verliert bei
Stromausfall seine Uhrzeit. Ein fremder Zeit-Broadcast hat die Uhr nicht gestellt.

## Zeitprogramme: WCM-FB richtig beschriftet

Im erprobten WCM-FB SW 9634 enthält das Telegramm die Reihenfolge **Ende, Start**
in Viertelstunden; `80 80` bezeichnet ein leeres Fenster. Dies ist anhand der
früheren Displayprüfung und erneut durch den Abgleich von ebusd mit einer
getrennten Rohdaten-Auslesung bestätigt.

Für Adresse `35` bindet dieser Fork deshalb `hc1.timer.inc` (Heizprogramme)
und `hc1.hwc.timer.inc` (Warmwasser) ein. Das erste Feld heißt nun korrekt
`End`, das zweite `Start`. **Die Reihenfolge auf dem Bus bleibt unverändert.**
Beim Lesen mit ausführlicher Ausgabe (`ebusctl read -v -c hc1 HP1.Mo.1`)
ist die Zuordnung sichtbar. Schreibwerte wären weiterhin in physischer
Reihenfolge Ende;Start anzugeben; ein Geräte-Schreibtest wurde dafür nicht ausgeführt.

Diese beiden Dateien sind aus den ursprünglichen Timer-Includes abgeleitet;
Nachrichtennamen, IDs, Typ `TTQ` und Polling bleiben erhalten. Andere
Heizkreisgeräte nutzen die unveränderten ursprünglichen Includes. Auch das
Zirkulationsprogramm bleibt unverändert, da es am erprobten Aufbau nicht genutzt wird.
Vorhandene Anwendungen, die die alte vertauschte Feldbenennung selbst korrigieren,
müssen die nun richtigen Namen beachten. Die getrennte HA-Rohdaten-Auslesung
ist von dieser Beschriftungskorrektur nicht betroffen.

## Sparsames Polling

Ausgewählte Raumgerät-Prozesswerte verwenden `r3`, die Außentemperatur `r5`,
ausgewählte Einstellwerte `r9`. Das sind relative Poll-Prioritäten, keine
Abstände in Sekunden; der tatsächliche Abstand hängt vom Pollintervall und der
Zahl der aktiven Nachrichten ab.

Das WCM-FB beantwortet Anfragen teilweise 10–30 Sekunden lang nicht. Ein
Timeout allein bedeutet daher keinen Busfehler. Nicht alle vorhandenen
Definitionen dauerhaft pollen. Bei MQTT-Discovery kann ein Filter, der jede
jemals gesehene Nachricht dauerhaft aktiviert, nach einem Suchlauf sehr viele
Abfragen erzeugen. In der erprobten Integration half `filter-seen = 1`;
diese Einstellung ist abhängig von der verwendeten MQTT-Integrationsvorlage.

Die Heizkreise 3–8 und die Definitionen von Adresse `08` bleiben aus dem
Ursprungsprojekt erhalten. Nur tatsächlich vorhandene Heizkreise aktiv abfragen.
Wenn `08..sc.csv` und `f6..sc.csv` auf derselben Anlage unter demselben Kreisnamen
`sc` konkurrieren, gezielt prüfen, ob die Datei für Adresse 08 benötigt wird.
Im erprobten Aufbau wurde sie außerhalb des Repositorys deaktiviert. Das ist
keine allgemeine Empfehlung für andere Anlagen.

## Konfiguration nach dem Start nicht geladen

Die WTC-Konfiguration an f6 wird nach einem ebusd-Start gelegentlich nicht
geladen, obwohl ihre Identifikation passiv gesehen wurde. Zuerst mit
`ebusctl info` prüfen, welche Dateien tatsächlich geladen sind. Im erprobten
Aufbau half ein gezieltes `ebusctl scan f6` und anschließend `ebusctl reload`.
Ein Reload verwirft zunächst die geladenen Gerätedefinitionen; deren erneutes
Laden dauerte ungefähr 1–4 Minuten. Keine Scan-/Reload-Schleife einrichten.

## Konfigurationsprüfung

Die übernommenen `ProcessValues1` bis `ProcessValues5` in `sc.processvalues.inc`
verwenden teilweise überlange IDs. Sie werden von der alten Definition
`08..sc.csv` eingebunden und führen bei der Gesamtprüfung mit ebusd 26.1 zu
`max message ID length exceeded` (Status 1). Diese Definitionen sind weiterhin
enthalten, wurden für diesen Fork aber nicht modernisiert oder neu am Gerät geprüft.

Die für WTC an f6, WCM-FB und WRSol relevante Konfiguration kann auf einer
**temporären Kopie** geprüft werden. Vom Wurzelverzeichnis des Forks aus:

```sh
check_dir=$(mktemp -d)
cp -R weishaupt tem "$check_dir/"
ln -s weishaupt "$check_dir/kromschroeder"
mv "$check_dir/weishaupt/08..sc.csv" "$check_dir/weishaupt/08..sc.csv.disabled"
ebusd --checkconfig --scanconfig=off --configpath="$check_dir"
check_status=$?
rm -r -- "$check_dir"
printf 'Prüfstatus: %s\n' "$check_status"
```

Diese Prüfung bestand mit ebusd 26.1.26.1 (3312 Nachrichten einschließlich der
Hersteller-Aliasdateien). Sie öffnet keinen Bus und ersetzt keine Prüfung der
Feldbedeutungen am jeweiligen Gerät. Die Arbeitskopie und die laufende
Konfiguration werden dabei nicht geändert.
