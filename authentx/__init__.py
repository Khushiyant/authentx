from authentx._version import __version__ as _version
from authentx.cli import cli

__version__ = _version

def main():
    cli()

if __name__ == "__main__":
    main()