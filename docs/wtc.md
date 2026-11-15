# WTC: Status, Fachmannparameter und Zähler

Stand der Erprobung: November 2026, WTC 15-A, ebusd 26.1.
Die Adressen und Umrechnungen sind nicht für andere Firmwarestände bestätigt.

## Passiver Status: `sc Act` (`500A`)

Die WTC sendet dieses Telegramm etwa einmal pro Minute. Die Ergänzungen ändern
keine Sollwerte und lösen keine zusätzlichen Abfragen aus.

| Feld | Bedeutung / Sicherheit |
|---|---|
| `Flame`, `Pump`, `Error` | Statusbits als `off/on`; `Error` enthält keinen numerischen Störcode |
| `Load` | Laststellung in Prozent; Umrechnung in kW hängt vom Gerät ab |
| `HeatingActive` | Status3 Bit 6; aus Beobachtungen als Brenner im Heizbetrieb abgeleitet |
| `TrendTemp` | Gedämpfte Außentemperatur, keine kurzfristige Wetterprognose |
| `SupplySetTemp` | Vom Regler übernommener Vorlauf-Sollwert; bildet ohne Regler nicht zuverlässig die interne Heizkurve ab |

Die Bedeutung von `HeatingActive` ist eine beobachtete Zuordnung, keine
Herstellerbestätigung. Weitere unbekannte Felder bleiben unverändert enthalten.

## Fachmannparameter: ausschließlich lesen

`sc.fachmann.inc` ergänzt `sc Fachmann1` und `sc Fachmann2` mit Poll-Priorität 9.
Verwendet wird `5000` mit drei Datenbytes. Die Antworten enthalten ein Statusbyte
und bis zu zwölf Nutzbytes. Die festen Anfragen lesen Bank 2:

| Nachricht | Anfrage-ID | Bereich |
|---|---|---|
| `Fachmann1` | `D3 B2 17` | 0x17–0x22 |
| `Fachmann2` | `E7 B2 23` | 0x23–0x2E |

Es gibt hier keinen Schreibbefehl und keine Anleitung für Speicher-Suchläufe.
Bank 0 darf nicht abgefragt werden: entsprechende Versuche führten zu einem
Neustart der WTC. Sicherheitswerte und die Prüfsumme des Parameterblocks dürfen
nicht verändert werden.

| Feld | Bedeutung | Auswertung / Sicherheit |
|---|---|---|
| `P31` | Maximaler Vorlauf-Sollwert | °C; plausible Zuordnung |
| `P32` | Schaltdifferenz Vorlauf | Betrag in K (Regelung ± Wert); plausible Zuordnung |
| `P34` | Brenner-Taktsperre | Untere 5 Bit, Minuten; bestätigt |
| `P36Raw` | Minimale Kesselleistung | Rohwert; bestätigt |
| `P37Raw` | Maximale Heizleistung | Rohwert; bestätigt |
| `P38Raw` | Maximale Warmwasserleistung | Rohwert; bestätigt |
| `P41` | Pumpennachlaufzeit | Unteres Halbbyte, Minuten; bestätigt |
| `P50` | Vorlaufüberhöhung Warmwasser | K; plausible Zuordnung |
| `P51Raw` | Schaltdifferenz Warmwasser | Unteres Halbbyte; Zuordnung bestätigt, Formel vorläufig |
| `P52` | Maximale Warmwasser-Ladezeit | Minuten; plausible Zuordnung |
| `P53Raw` | Speicher-Absenkung | Betrag in K; bestätigt |
| `P20` | Außenfühlerkorrektur | Vorzeichenbehaftete °C; bestätigt |

Leistungswerte werden als `floor(Prozent × 2,55)` gespeichert. Für die Anzeige
kann auf die nächste ganze Prozentzahl von `Rohwert / 2,55` gerundet werden.
Für P51 passt bisher `-(Rohwert + 3)` K, geprüft an −5 und −6 K; andere Werte
sind noch offen. P53 wird als `-Rohwert` K ausgewertet.

Die Abfragen liefern gelegentlich einen ganzen Block unplausibler Werte, der bei
späteren Abfragen verschwindet. Einzelwerte deshalb nicht als Parameteränderung
werten und nicht für automatische Regelentscheidungen verwenden. Bei Timeouts
keine schnellen Wiederholungsschleifen starten.

## Zähler: `sc Zaehler`

`sc.zaehler.inc` liest Bank 3 ab Adresse F0 mit der festen Anfrage-ID `68 B3 F0`
und Poll-Priorität 9. Nach dem Statusbyte und vier übersprungenen Nutzbytes folgen:

- `StartsSinceReset`: I40, zwei Bytes big-endian, Brennerstarts seit Rückstellung.
- `HoursSinceReset`: I41, ein Byte, Brennerstunden seit Rückstellung.

I40 ist ein rückstellbarer Zähler mit einem Anzeigebereich von 0 bis 999 und
kein unbegrenzt wachsender Gesamtzähler. Überlauf und manuelle Rückstellung
müssen bei Differenzen berücksichtigt werden. I41 ist auf ein Byte begrenzt.
I42/I43 (Gesamtzähler am Gerät) werden hier nicht dekodiert.

## Prüfbytes: inzwischen mit historischen Daten bestätigt

Die von aghulas beschriebenen Rechenverfahren passen auch zu den vorhandenen
WTC-15-Aufzeichnungen: Telegramm-CRC (Polynom `0x5C`) und ein davon verschiedenes
Prüfbyte des Fachmannblocks (Schiebeverfahren mit `0x21`, abschließend komplementiert).
Der Fachmannblock `0x17–0x3B` samt Prüfbyte an `0x3C` stimmt in allen fünf
historischen Vergleichsfällen überein. Der Fremdfork hat andere Blockgrenzen;
diese werden nicht übernommen. Quellen, Belege, Grenzen und Offline-Werkzeug:
[Abgleich mit anderen Forks](forks.md). Die Erkenntnis ermöglicht keine
Freigabe von Speicher-Schreibzugriffen.
