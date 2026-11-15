#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Daniel Knoop
"""Weishaupt-Prüfbytes offline berechnen; kein Netzwerk- oder Gerätezugriff.

Algorithmen nach aghulas/ebusd-configuration-weishaupt, siehe docs/forks.md.
Telegramm-CRC und EEPROM-Blockprüfbyte sind unterschiedliche Verfahren.
Diese Funktionen prüfen Daten; sie senden oder verändern keine Telegramme.
"""

import argparse


def telegram_crc(payload: bytes) -> int:
    """CRC über die Nutzbytes nach dem Prüfbyte (Polynom 0x5C)."""
    if not payload:
        raise ValueError("Mindestens ein Nutzbyte erforderlich")
    value = payload[0]
    for byte in payload[1:]:
        for _ in range(8):
            value = ((value << 1) ^ (0x5C if value & 0x80 else 0)) & 0xFF
        value ^= byte
    return value


def parameter_block_check(block: bytes) -> int:
    """Prüfbyte über einen Parameterblock ohne das abschließende Prüfbyte."""
    if not block:
        raise ValueError("Mindestens ein Blockbyte erforderlich")
    value = 0
    for byte in block:
        value <<= 1
        if value > 0xFF:
            value = (value - 0x100) ^ 0x21
        value ^= byte
    return 0xFF - value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verfahren", choices=("telegramm", "block"))
    parser.add_argument("hexbytes", help="Hexbytes ohne Prüfbyte; Leerzeichen erlaubt")
    args = parser.parse_args()
    try:
        data = bytes.fromhex(args.hexbytes)
        fn = telegram_crc if args.verfahren == "telegramm" else parameter_block_check
        result = fn(data)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"{result:02X}")


if __name__ == "__main__":
    main()
