# Troubleshooting

## `ImportError`, `DLL load failed`, or an invalid binary message

Confirm that you downloaded the archive for your operating system, are using
64-bit CPython 3.9, and installed every locked dependency in a clean environment.
The Windows and Linux archives are not interchangeable.

## `ModuleNotFoundError: exgep`

Run commands from the extracted `EXGEP-v1.0.0` directory, or add that directory
to `PYTHONPATH`. EXGEP v1.0.0 is an extracted runtime, not a package installed by
cloning the documentation repository.

## Dependency installation fails

Upgrade pip inside a fresh Python 3.9 virtual environment and retry
`python -m pip install -r requirements.txt`. Preserve the complete output for a
support report.

## Data or metric import errors

Use the files included under `data/` and import metrics from
`exgep.data.reg_metrics`. The obsolete `exgep.utils.reg_metrics` path is not part
of v1.0.0.

## Reporting a reproducible defect

Include the archive filename and SHA-256, operating system and architecture,
Python version, dependency installation output, exact command, and complete
traceback. Never post proprietary datasets, credentials, or personal data.
