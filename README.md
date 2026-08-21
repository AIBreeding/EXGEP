# EXGEP

EXGEP is a framework for predicting genotype-by-environment interactions with
ensembles of explainable machine-learning models.

This repository is the official documentation and release hub. EXGEP is
distributed as compiled binaries and is **not open source**. GitHub's automatic
“Source code” archives contain documentation only and are not runnable EXGEP
packages.

## Download v1.0.0

| Platform | Runtime archive |
|---|---|
| Windows x86-64, CPython 3.9 | [EXGEP-v1.0.0-windows-x86_64-py39.zip](https://github.com/AIBreeding/EXGEP/releases/download/v1.0.0/EXGEP-v1.0.0-windows-x86_64-py39.zip) |
| Linux x86-64, CPython 3.9 | [EXGEP-v1.0.0-linux-x86_64-py39.tar.gz](https://github.com/AIBreeding/EXGEP/releases/download/v1.0.0/EXGEP-v1.0.0-linux-x86_64-py39.tar.gz) |

Download [SHA256SUMS.txt](https://github.com/AIBreeding/EXGEP/releases/download/v1.0.0/SHA256SUMS.txt)
from the same release and verify the archive before extracting it.

## Quick start

1. Download the archive matching your operating system.
2. Verify its SHA-256 checksum.
3. Extract it and open `README.md` inside the extracted directory.
4. Create a Python 3.9 environment and install the locked dependencies.
5. Run the included examples from the extracted directory.

See [installation](docs/installation.md), [compatibility](docs/compatibility.md),
and [troubleshooting](docs/troubleshooting.md) for complete instructions.

## License

EXGEP v1.0.0 may be used without charge for non-commercial research under the
[EXGEP Research Use License 1.0](LICENSE). Any commercial use requires prior
written authorization. Commercial use includes internal research or development
by a for-profit organization. Complete, unmodified official archives may be
forwarded or mirrored for research use under the redistribution conditions in
the license. Commercial authorization is never transferred by redistribution.

For commercial licensing, contact **lihuihui@caas.cn**. Read the
[licensing guide](docs/licensing.md) before use.

## Citation

If EXGEP contributes to a publication, cite the software version and:

> Yu T, Zhang H, Chen S, et al. EXGEP: a framework for predicting
> genotype-by-environment interactions using ensembles of explainable
> machine-learning models. *Briefings in Bioinformatics* (2025).
> https://doi.org/10.1093/bib/bbaf414

Citation metadata is available in [CITATION.cff](CITATION.cff).

## Support and security

For a reproducible bug report, include the EXGEP version, archive filename and
checksum, operating system and architecture, `python --version`, dependency
installation output, the exact command, and the full error traceback. Do not
attach confidential datasets.

See [SECURITY.md](SECURITY.md) for private vulnerability reporting. General
usage questions and reproducible defects may be filed in GitHub Issues.

## Release information

- [Changelog](CHANGELOG.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
- [Latest release](https://github.com/AIBreeding/EXGEP/releases/latest)
