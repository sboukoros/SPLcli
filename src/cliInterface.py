import click
import sys
import src.reader as reader
import src.writer as writer
import datetime


class Config():

    def __init__(self, timeStarted, passedargs, inputfile, outputfile):
        """modifying the ctx.obj from the Click class to do more"""
        self.passedArgs = passedargs
        self.timeStarted = timeStarted
        self.reader = reader.Reader(inputfile)
        self.writer = writer.Writer(outputfile)


@click.group()
@click.argument("inputFile", required=True, type=click.Path(exists=True,
                file_okay=True, dir_okay=True, readable=True))
@click.argument("outputFile", required=True,   type=click.Path(file_okay=True,
                dir_okay=False, writable=True))
@click.pass_context
def cli(ctx, inputfile, outputfile):
    passedargs = sys.argv[1:]
    passedargs = ' '.join(passedargs)
    timeStarted = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    ctx.obj = Config(timeStarted, passedargs, inputfile, outputfile)


@cli.command()
@click.option('--ip-type', type=click.Choice(['client', 'remote', 'all'],
                                             case_sensitive=False),
              default='all')
@click.option("-k", "--topk",  default=1,
                    help="Returns the top K most frequent IPs.Default=1")
@click.option("-ah", "--autoheal",  default=0,
              help="Makes a best effort to keep IPs and not URLS. Default=1")
@click.pass_obj
def mfip(obj, topk, ip_type='all', autoheal=0):
    """This script returns the most frequent IP. In case of multiple IPs with
    the same count, they are returned in random order."""
    resDict = obj.reader.returnFip(topk, ip_type, autoheal, mfip=True)

    """ Create the response to be written"""
    writeDict = {"Timestamp": obj.timeStarted,
                 "Script": f"Top {topk} most frequent IPs",
                 "Params": obj.passedArgs}
    writeDict['IPs'] = {}
    for it1, it2 in resDict:
        writeDict['IPs'][it1] = it2
    obj.writer.write(writeDict)


@cli.command()
@click.option('--ip-type', type=click.Choice(['client', 'remote', 'all'],
                                             case_sensitive=False),
              default='all')
@click.option("-k", "--topk",  default=1,
              help="Returns the top K least frequent IPs. Default=1")
@click.option("-ah", "--autoheal",  default=0,
              help="Makes a best effort to keep IPs and not URLS. Default=1")
@click.pass_obj
def lfip(obj, topk, ip_type='all', autoheal=0):
    """This script returns the least frequent IP. In case of multiple IPs with
        the same count, they are returned in random order."""
    resDict = obj.reader.returnFip(topk, ip_type, autoheal, mfip=False)

    """ Create the response to be written"""
    writeDict = {"Timestamp": obj.timeStarted,
                 "Script": f"Top {topk} least frequent IPs",
                 "Params": obj.passedArgs}
    writeDict['IPs'] = {}

    for it1, it2 in resDict:
        writeDict['IPs'][it1] = it2
    obj.writer.write(writeDict)


@cli.command()
@click.option('--resp-type', type=click.Choice(['header', 'body', 'all'],
                                               case_sensitive=False),
              default='all')
@click.option("-src", "--source",  default=0,
              help="Source of the traffic")
@click.option("-dest", "--destination",  default=0,
              help="Destination of the traffic")
@click.pass_obj
def bytesexc(obj, source, destination, resp_type):
    """This script returns the total amount of bytes exchanged between 2 IPs
        specified in -src and -dst. If not specified it returns the whole
        traffic"""
    totalbytes = obj.reader.sumbytes(source, destination, resp_type)

    """ Create the response to be written"""
    if source and destination:
        iptext = f"from source {source} to destination {destination}"
    elif source:
        iptext = f"from source {source}"
    else:
        iptext = f"to destination {destination}"

    if resp_type == 'all':
        resptext = "using all headers"
    elif resp_type == "body":
        resptext = "using only response size"
    else:
        resptext = "using only headers size"

    txt = f"A total of {totalbytes} excanged, " + resptext + " " + iptext
    writeDict = {"Timestamp": obj.timeStarted,
                 "Script": txt,
                 "Params": obj.passedArgs,
                 "bytes exchanged": totalbytes}
    obj.writer.write(writeDict)


@cli.command()
@click.pass_obj
def eps(obj):
    """This script returns the total amount of bytes exchanged between 2 IPs
        specified in -src and -dst. If not specified it returns the whole
        traffic"""
    evts = obj.reader.eventsPerSecond()

    """ Create the response to be written"""
    writeDict = {"Timestamp": obj.timeStarted,
                 "Script": "Events per second",
                 "Params": obj.passedArgs,
                 "Events per second": evts}
    obj.writer.write(writeDict)


def main():
    try:
        cli()
        print(click.get_current_context().info_name)
    except SystemExit:
        pass
