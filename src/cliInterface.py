import click
import src.reader as reader

@click.command()
@click.option("--input", "-i", "input", 
        required = True,  type=click.Path( exists=True, file_okay=True, dir_okay=True, readable=True) )

@click.option ("--output", "-o", "output", 
        required = True,  type=click.Path( file_okay=True, dir_okay=False, writable=True) )
def read(input, output, mfip, lfip, eps, _bytes):
    thisreader = reader.Reader(input, output, mfip, lfip, eps, _bytes)
    #thisreader.main()
    
@click.option("--mfip", 
        is_flag=True, show_default=True, default=False, help="Most frequent IP")

@click.option("--lfip", 
        is_flag=True, show_default=True, default=False, help="Least frequent IP")

@click.option("--eps", 
        is_flag=True, show_default=True, default=False, help="Events per second")

#remember to add a callback validation here
@click.option("---bytes",
        Type=click.Choice(['header', 'body', 'all'], case_sensitive=False),
        args=2, type=str, is_flag=True, show_default=True, default=False, 
                help="Total amount of bytes exchanged. You must specify the option header, body, or all. After the flag specify source and destination IPs like/\
                        --bytes sourceIP destinationIP. If no or wrong IPs are provided, the script will  /\
                         return the total amount of bytes")



if __name__ == '__main__':
    read()
    