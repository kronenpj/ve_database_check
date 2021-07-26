#!/usr/bin/env bash

DOCKER=${DOCKER:-podman}
OPTS="--privileged --rm"
#CTR_WIN="cdrx/pyinstaller-windows"
#CTR_LIN="cdrx/pyinstaller-linux"
CTR_WIN="pyinstaller-win64:4.3"
CTR_LIN="pyinstaller-linux:4.3"

${DOCKER} run ${OPTS} -v "$(pwd):/src/" ${CTR_WIN} "pyinstaller -F -c compare_db.py"

${DOCKER} run ${OPTS} -v "$(pwd):/src/" ${CTR_LIN} "pyinstaller -F -c compare_db.py"
