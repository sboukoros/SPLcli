import click
import src.reader as reader


@click.group()
@click.argument("inputFile", required=True, type=click.Path(exists=True,
                file_okay=True, dir_okay=True, readable=True))
@click.argument("outputFile", required=True,   type=click.Path(file_okay=True,
                dir_okay=False, writable=True))
@click.pass_context
def cli(ctx, inputfile, outputfile):
    ctx.obj = reader.Reader(inputfile, outputfile)


@cli.command()
@click.option('--ip-type', type=click.Choice(['client', 'remote', 'all'],
                                             case_sensitive=False),
              default='all')
@click.option("-k", "--topk",  default=1,
                    help="Returns the top K most frequent IPs.Default=1")
@click.option("-ah", "--autoheal",  default=0,
              help="Makes a best effort to keep IPs and not URLS. Default=1")
@click.pass_obj
def mfip(myreader, topk, ip_type='all', autoheal=0):
    """This script returns the most frequent IP. In case of multiple IPs with
    the same count, they are returned in random order."""
    print(ip_type)
    myreader.returnFip(topk, ip_type, autoheal, mfip=True)


@cli.command()
@click.option('--ip-type', type=click.Choice(['client', 'remote', 'all'],
                                             case_sensitive=False),
              default='all')
@click.option("-k", "--topk",  default=1,
              help="Returns the top K least frequent IPs. Default=1")
@click.option("-ah", "--autoheal",  default=0,
              help="Makes a best effort to keep IPs and not URLS. Default=1")
@click.pass_obj
def lfip(myreader, topk, ip_type='all', autoheal=0):
    """This script returns the least frequent IP. In case of multiple IPs with
        the same count, they are returned in random order."""
    myreader.returnFip(topk, ip_type, autoheal, mfip=False)


@cli.command()
@click.option('--resp-type', type=click.Choice(['header', 'body', 'all'],
                                               case_sensitive=False),
              default='all')
@click.option("-src", "--source",  default=0,
              help="Source of the traffic")
@click.option("-dest", "--destination",  default=0,
              help="Destination of the traffic")
@click.pass_obj
def bytesexc(myreader, source, destination, resp_type):
    """This script returns the total amount of bytes exchanged between 2 IPs
        specified in -src and -dst. If not specified it returns the whole
        traffic"""
    myreader.sumbytes(source, destination, resp_type)


@cli.command()
@click.pass_obj
def eps(myreader):
    """This script returns the total amount of bytes exchanged between 2 IPs
        specified in -src and -dst. If not specified it returns the whole
        traffic"""
    myreader.eventsPerSecond()


def main():
    try:
        cli()
        print(click.get_current_context().info_name)
    except SystemExit:
        pass
