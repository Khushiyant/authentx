import click
import os
from authentx.utils import ASCII_ART
from authentx._version import __version__ as _version
from authentx.utils import extractor, PDFFile

class ASCIICommandClass(click.Group):
    def get_help(self, ctx):
        return ASCII_ART + '\n' + super().get_help(ctx)
    

@click.group(name='cli', cls=ASCIICommandClass)
@click.version_option(_version, prog_name='Quasar')
@click.help_option('-h', '--help')
def cli() -> None:
    pass

@cli.command()
@click.option('--path', '-p', required=True, type=str, help='Path to the PDF file')
def report(path) -> None:
    file = PDFFile(path=path, text=None, metadata=None)
    text = extractor(file)
    click.echo(text)
