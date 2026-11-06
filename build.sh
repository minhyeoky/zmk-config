#!/bin/sh
# Build the firmware locally in Docker. Output: firmware/*.uf2
# SECRETS points at the QMK secrets.h; the generated secrets.dtsi stays local (gitignored).
set -eu
cd "$(dirname "$0")"

SECRETS=${SECRETS:-$HOME/qmk-osmode/keyboards/crkbd/keymaps/minhyeoky/secrets.h}
if [ -f "$SECRETS" ]; then
    python3 scripts/gen_secrets.py "$SECRETS" config/secrets.dtsi
else
    echo "no secrets.h at $SECRETS — SEC_PW will be a no-op"
    rm -f config/secrets.dtsi
fi

mkdir -p firmware
docker run --rm \
    -v zmk-workspace:/zmk \
    -v "$PWD/config":/src-config:ro \
    -v "$PWD/firmware":/out \
    -w /zmk \
    zmkfirmware/zmk-build-arm:3.5 sh -euc '
        rm -rf config && cp -r /src-config config
        [ -d .west ] || west init -l config
        west update --fetch-opt=--filter=tree:0
        west zephyr-export >/dev/null
        build() {
            name=$1; shift
            west build -p -s zmk/app -d build/$name -b nice_nano_v2 -- -DZMK_CONFIG=/zmk/config "$@"
            cp build/$name/zephyr/zmk.uf2 /out/$name.uf2
        }
        build corne_left     -DSHIELD="corne_left nice_view_adapter nice_view"
        build corne_right    -DSHIELD="corne_right nice_view_adapter nice_view"
        build settings_reset -DSHIELD=settings_reset
    '
ls -l firmware
