#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import qrcode
import subprocess
import sys
import os
import argparse
from PIL import Image
import importlib.resources as pkg_resources
import qrgen.words

def main():
    qr_version = "0.1"
    banner = '''
  e88 88e   888 88e    e88'Y88
 d888 888b  888 888D  d888  'Y   ,e e,  888 8e
C8888 8888D 888 88"  C8888 eeee d88 88b 888 88b
 Y888 888P  888 b,    Y888 888P 888   , 888 888
  "88 88"   888 88b,   "88 88"   "YeeP" 888 888
      b
      8b,    {}'''.format("QRGen ~ v" + qr_version + " ~ by h0nus\n")
    print(banner)

    parser = argparse.ArgumentParser(
        description="Tool to generate Malformed QRCodes for fuzzing QRCode parsers/reader",
        usage='qrgen -l [number]\n       qrgen -w /path/to/custom/wordlist',
        epilog="Pay attention everywhere, even in the dumbest spot"
    )
    sgroup = parser.add_argument_group("Options for QRGen")
    sgroup.add_argument("--list", "-l", type=int, help="Set wordlist to use", choices=list(range(8)))
    sgroup.add_argument("--wordlist", "-w", type=str, help="Use a custom wordlist")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()

    lists = [
        'sqli.txt', 'xss.txt', 'cmdinj.txt', 'formatstr.txt',
        'xxe.txt', 'strfuzz.txt', 'ssi.txt', 'lfi.txt'
    ]

    os.makedirs('genqr', exist_ok=True)

    for f in os.listdir('genqr'):
        try:
            os.remove(os.path.join('genqr', f))
        except Exception:
            pass

    payloads = []

    if options.list is not None:
        filename = lists[options.list]
        with pkg_resources.open_text(qrgen.words, filename) as f:
            payloads = [line.strip() for line in f]
    elif options.wordlist:
        with open(options.wordlist, 'r') as f:
            payloads = [line.strip() for line in f]

    for i, payload in enumerate(payloads):
        img = qrcode.make(payload)
        img.save(f"genqr/payload-{i}.png")

    print(f"Generated {len(payloads)} payloads!")
    if payloads:
        Image.open(f"genqr/payload-{len(payloads) - 1}.png").show()
        print("Opening last generated payload...")

    print("Thanks for using QRGen, made by h0nus..")

if __name__ == '__main__':
    main()
