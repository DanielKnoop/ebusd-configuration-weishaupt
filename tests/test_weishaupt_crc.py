# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Daniel Knoop
"""Bekannte Telegramm-Prüfbytes und unabhängige Grenzfälle der Blockprüfung."""

import csv
from pathlib import Path
import re
import unittest

from tools.weishaupt_crc import parameter_block_check, telegram_crc


class Checks(unittest.TestCase):
    def test_known_telegram_vectors(self):
        # Bestehende WTC-Definitionen und Mehrfachabfragen aus aghulas.
        vectors = {
            "B217": 0xD3, "B223": 0xE7, "B3F0": 0x68,
            "0122015B115F01660168": 0x88,
            "029F8263": 0x03, "73BB13AC": 0x0C,
        }
        for payload, expected in vectors.items():
            with self.subTest(payload=payload):
                self.assertEqual(telegram_crc(bytes.fromhex(payload)), expected)

    def test_documented_short_read_keys(self):
        # Prüft die bisher empirisch ermittelten Schlüssel auch über alle Adressen.
        for descriptor, key in ((0xB1, 0x20), (0xB2, 0xC4), (0xB3, 0x98),
                                (0x12, 0x08), (0x62, 0xFC), (0x72, 0x4C)):
            for address in range(256):
                with self.subTest(descriptor=descriptor, address=address):
                    self.assertEqual(telegram_crc(bytes((descriptor, address))), key ^ address)

    def test_parameter_block_check(self):
        # Ein- und Zweibytefälle mit von Hand bestimmbaren Ergebnissen.
        for block, expected in ((b"\x00", 0xFF), (b"\x01", 0xFE),
                                (b"\x80\x00", 0xDE), (b"\xff\xff", 0xDF)):
            with self.subTest(block=block):
                self.assertEqual(parameter_block_check(block), expected)

    def test_existing_memory_read_definitions(self):
        # Verhindert falsche Prüfbytes in gepflegten 5000-Lesedefinitionen.
        root = Path(__file__).resolve().parents[1] / "weishaupt"
        checked = 0
        for path in sorted(root.iterdir()):
            if path.suffix not in (".csv", ".inc"):
                continue
            read_pbsb = ""
            for number, row in enumerate(csv.reader(path.read_text().splitlines()), 1):
                if not row or row[0].startswith("#"):
                    continue
                row += [""] * max(0, 8 - len(row))
                if row[0].startswith("*r"):
                    read_pbsb = row[6]
                    continue
                if not row[0].startswith("r") or (row[6] or read_pbsb) != "5000":
                    continue
                if not re.fullmatch(r"(?:[0-9A-Fa-f]{2}){3,}", row[7]):
                    continue
                data = bytes.fromhex(row[7])
                with self.subTest(file=path.name, line=number, message=row[2]):
                    self.assertEqual(telegram_crc(data[1:]), data[0])
                checked += 1
        self.assertGreater(checked, 0, "Keine Speicher-Lesedefinitionen geprüft")

    def test_empty_input_rejected(self):
        for fn in (telegram_crc, parameter_block_check):
            with self.assertRaises(ValueError):
                fn(b"")


if __name__ == "__main__":
    unittest.main()
