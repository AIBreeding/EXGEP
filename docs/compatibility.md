# Compatibility

EXGEP v1.0.0 supports only the following runtime combinations:

| Operating system | Architecture | Python | Archive |
|---|---|---|---|
| Windows 10/11 | x86-64 | CPython 3.9, 64-bit | `EXGEP-v1.0.0-windows-x86_64-py39.zip` |
| Linux | x86-64 | CPython 3.9, 64-bit | `EXGEP-v1.0.0-linux-x86_64-py39.tar.gz` |

macOS, ARM64/AArch64, 32-bit Python, PyPy, and Python versions other than 3.9
are not supported by this release. A compatible Python version alone is not
enough: the operating system and CPU architecture must also match.

Linux compatibility depends on the system C/C++ runtime libraries required by
the compiled extensions and their dependencies. If import fails with a missing
shared-library or `GLIBC`/`GLIBCXX` message, include the exact message and
distribution version in a support request.
