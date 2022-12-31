
# SPLcli
This a logparser for Squid proxy access logs.
The tool is called SPLcli which stands for SquidProxyLogs cli.
It requires docker to run OR can be build and installed locally. 


The tools is based on the Click framework (https://click.palletsprojects.com/en/8.1.x/) for Python. 
The tools supports 4 basic operations with the ability to pass options to them.
Every command can be run with --help to showcase the usage of the command and the available options.

# On how to setup the tool:

# Option 1 - How to build the docker image
Navigate to the folder where the Dockerfile is.
Build the image: $ docker build -t <nameYOUwant>
Run the app: $ docker run <nameYOUGave> -it

For the program to run, it needs to run interactively. Hence, the -it option.

# Option 2 - Install and run locally
Clone the repo and enter it.
Build the SPLcli package using pip $ pip install .
Run the tool using the SPLcli command.

# On how to run the tool:
Usage: SPLcli [OPTIONS] INPUTFILE OUTPUTFILE COMMAND [ARGS]...
```
Options:
  --help  Show this message and exit.
  ```

Commands:
  - bytesexc  This script returns the total amount of bytes exchanged...
  - eps       This script returns the total amount of bytes exchanged...
  - lfip      This script returns the least frequent IP.
  - mfip      This script returns the most frequent IP.

In details the 4 commands and their options:



## bytesexc for bytes exchanged

Usage: SPLcli bytesexc [OPTIONS]

  This script returns the total amount of bytes exchanged between 2 IPs
  specified in -src and -dst. If not specified it returns the whole traffic
```
Options:
  --resp-type [header|body|all]
  -src, --source INTEGER         Source of the traffic  
  -dest, --destination INTEGER   Destination of the traffic  
```


## eps for events per second
Usage: SPLcli eps 

  This script returns the average events per second


## mfip for top  k most frequent IPs 
Usage: SPLcli mfip [OPTIONS]

  This script returns the most frequent IP. In case of multiple IPs with the
  same count, they are returned in random order.
```
Options:
  --ip-type [client|remote|all]   
  -k, --topk INTEGER             Returns the top K most frequent IPs.Default=1   
  -ah, --autoheal INTEGER        Makes a best effort to keep IPs and not URLS.  
                                 Default=0
```


## lfip for bottom k least frequent IPs 
Usage: SPLcli mfip [OPTIONS]

  This script returns the most frequent IP. In case of multiple IPs with the
  same count, they are returned in random order.
```
Options:
  --ip-type [client|remote|all]
  -k, --topk INTEGER             Returns the top K most frequent IPs.Default=1  
  -ah, --autoheal INTEGER        Makes a best effort to keep IPs and not URLS.  
                                 Default=0
                                 ```