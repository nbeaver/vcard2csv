#! /usr/bin/env false
VENV_PATH=.venv
if test -d "${VENV_PATH}"/bin
then
    # Linux
    . "${VENV_PATH}"/bin/activate
elif test -d "${VENV_PATH}"/Scripts
then
    # Windows
    . "${VENV_PATH}"/Scripts/activate
else
    printf "Error: cannot find virtual environment: '%s'.\n" "${VENV_PATH}" >&2
fi
