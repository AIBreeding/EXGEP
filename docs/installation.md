# Installation

Do not clone this repository to install EXGEP. Download the named runtime
archive from [Release v1.0.0](https://github.com/AIBreeding/EXGEP/releases/tag/v1.0.0).
GitHub's automatically generated source archives contain documentation only.

## Windows x86-64

```powershell
Get-FileHash .\EXGEP-v1.0.0-windows-x86_64-py39.zip -Algorithm SHA256
Expand-Archive .\EXGEP-v1.0.0-windows-x86_64-py39.zip -DestinationPath .
cd .\EXGEP-v1.0.0
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import exgep; from exgep.model import RegEXGEP; print(exgep.__version__)"
python test_exgep.py --help
```

## Linux x86-64

```bash
sha256sum EXGEP-v1.0.0-linux-x86_64-py39.tar.gz
tar -xzf EXGEP-v1.0.0-linux-x86_64-py39.tar.gz
cd EXGEP-v1.0.0
python3.9 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import exgep; from exgep.model import RegEXGEP; print(exgep.__version__)"
python test_exgep.py --help
```

Compare the first command's output with `SHA256SUMS.txt` before extracting the
archive. The archive's root-level `README.md` contains the complete workflow.
