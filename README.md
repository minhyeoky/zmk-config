# zmk-config — wireless Corne (beekeeb, nice!nano v2 + nice!view)

ZMK v0.3. Keymap ported from the QMK keymap [`crkbd/keymaps/minhyeoky`](https://github.com/minhyeoky/qmk_firmware/tree/master/keyboards/crkbd/keymaps/minhyeoky).

## Build

```sh
./build.sh          # Docker; outputs firmware/{corne_left,corne_right,settings_reset}.uf2
```

- The ZMK workspace lives in the Docker volume `zmk-workspace` (first build clones ZMK + Zephyr).
- `SEC_PW` comes from the QMK `secrets.h` (override with `SECRETS=...`). `scripts/gen_secrets.py` turns it into `config/secrets.dtsi`, which is gitignored. Without it, `SEC_PW` does nothing.
- Builds run locally rather than in GitHub Actions, so the password never leaves the machine.

## Flash

1. Plug one half in by USB and double-tap its reset button. A `NICENANO` drive mounts.
2. Copy `corne_left.uf2` to the left half and `corne_right.uf2` to the right half.
3. If the halves won't pair with each other: flash `settings_reset.uf2` to both, then flash the real firmware again, then reset both halves at the same time.

Once the firmware runs, the DANGER layer also has `&bootloader` (left: Q position, right: top outer key).

## Layers

| # | Name | Reached by |
|---|---|---|
| 0 | BASE (MAC) | default |
| 1 | BASE_W (WIN) | `&pc_win` / `&tog BASE_W` |
| 2 | SYMBOL | hold Space |
| 3 | NAV | hold Enter (mac) |
| 4 | NAV_W | hold Enter (win) |
| 5 | MANAGE | NAV + left pinky bottom |
| 6 | DANGER | MANAGE + right pinky bottom |

MANAGE top row left: `PC1 mac` (BT 0) · `PC2 win` (BT 1) · `phone` (BT 2). Home row outer left: mac/win toggle without switching the profile.

Pairing: select a profile, then pair from the host. To forget the current profile's host, use `BT_CLR` on DANGER (left, A position).

## Differences from the QMK keymap

- The 4 ex2 keys are gone (42 keys). KVM_TOGGLE becomes BT profile + platform switching. SEC_PW moves to NAV Y. KVM_BEEP_OFF is dropped.
- The platform is not persisted across power cycles; the BT profile is. After a reboot on the win PC, press `PC2 win` once.
- No RGB (the board has none), so the RGB keys on MANAGE are removed.
- `ONESHOT_TAP_TOGGLE` has no ZMK equivalent.
- Unused QMK keycodes (BRACKET_COMPLETE, VIM_CNEXT/CPREV, SEC_ID) are not ported.
- Brightness sends consumer Brightness Up/Down instead of QMK's Scroll Lock/Pause aliases (macOS handles them natively). Sleep sends consumer Sleep (`C_SLEEP`); whether the hosts act on it is untested.
- Combos fire only from BASE/BASE_W, so `,`+`.` while holding Space types `,.` instead of `]`.
