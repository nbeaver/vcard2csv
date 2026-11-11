#! /usr/bin/env false
# Use a false shebang since it won't work if run as executable.

# Default to .venv but allow overriding from environment variable.
VENV_PATH=${VENV_PATH:-.venv}
if test -d "${VENV_PATH}"/bin
then
    # Linux / macOS
    . "${VENV_PATH}"/bin/activate
elif test -d "${VENV_PATH}"/Scripts
then
    # Windows
    . "${VENV_PATH}"/Scripts/activate
else
    printf "Error: cannot find virtual environment: '%s'\n" "${VENV_PATH}" >&2
    # Don't exit here as this will close the shell.
fi
if test -n "$BASH_VERSION"
then
    if ! (return 0 2>/dev/null)
    then
        printf "Error: this script must be sourced, not executed directly:\n" >&2
        printf ". $0\n" >&2
    fi
fi
if test "$ZSH_EVAL_CONTEXT" = "toplevel"
then
    printf "Error: this script must be sourced, not executed directly:\n" >&2
    printf ". $0\n" >&2
fi
