#!/usr/bin/env bash

DOCKER=${DOCKER:-docker}
OPTS="--privileged --rm"
CTR_WIN="cdrx/pyinstaller-windows"
CTR_LIN="cdrx/pyinstaller-linux"

${DOCKER} run ${OPTS} -v "$(pwd):/src/" ${CTR_WIN} "pyinstaller -F -c compare_db.py"

${DOCKER} run ${OPTS} -v "$(pwd):/src/" ${CTR_LIN} "pyinstaller -F -c compare_db.py"
