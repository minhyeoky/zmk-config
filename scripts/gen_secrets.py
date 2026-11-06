#!/usr/bin/env python3
"""Generate config/secrets.dtsi (gitignored) from the QMK secrets.h.

Usage: gen_secrets.py <path/to/secrets.h> <out/secrets.dtsi>
Prints only the character count, never the secret.
"""
import re
import sys

SYMBOLS = {
    " ": "SPACE", "!": "EXCL", "@": "AT", "#": "HASH", "$": "DLLR", "%": "PRCNT",
    "^": "CARET", "&": "AMPS", "*": "STAR", "(": "LPAR", ")": "RPAR",
    "-": "MINUS", "_": "UNDER", "=": "EQUAL", "+": "PLUS",
    "[": "LBKT", "]": "RBKT", "{": "LBRC", "}": "RBRC",
    "\\": "BSLH", "|": "PIPE", ";": "SEMI", ":": "COLON",
    "'": "SQT", '"': "DQT", ",": "COMMA", "<": "LT", ".": "DOT", ">": "GT",
    "/": "FSLH", "?": "QMARK", "`": "GRAVE", "~": "TILDE",
}


def keycode(ch):
    if "a" <= ch <= "z":
        return ch.upper()
    if "A" <= ch <= "Z":
        return f"LS({ch})"
    if "0" <= ch <= "9":
        return f"N{ch}"
    if ch in SYMBOLS:
        return SYMBOLS[ch]
    sys.exit(f"unsupported character (code point {ord(ch)})")


def main():
    src, out = sys.argv[1], sys.argv[2]
    text = open(src, encoding="utf-8").read()
    m = re.search(r'#define\s+SECRET_PW\s+"((?:[^"\\]|\\.)*)"', text)
    if not m:
        sys.exit("SECRET_PW not found")
    pw = bytes(m.group(1), "utf-8").decode("unicode_escape")
    taps = " ".join(f"&kp {keycode(c)}" for c in pw)
    with open(out, "w", encoding="utf-8") as f:
        f.write(
            "/ {\n    macros {\n        sec_pw: sec_pw {\n"
            '            compatible = "zmk,behavior-macro";\n'
            "            #binding-cells = <0>;\n"
            f"            bindings = <&macro_tap {taps}>;\n"
            "        };\n    };\n};\n"
        )
    print(f"secrets.dtsi: {len(pw)} keystrokes")


if __name__ == "__main__":
    main()
