# shout it out ( Simple telegram notification maker)



# Install

## clone and install dependencies:

```bash
cd /opt
git clone https://github.com/jcatala/shout-it-out
cd shout-it-out
pip3 install -r requeriments.txt --user
# optional
chmod 755 main.py
ln -s /opt/shout-it-out/main.py /usr/local/bin/sio-notification.py
```


* Create the `.SIO.conf` in your home directory, with the following syntax:

```
[DEFAULT]
apikey = YOUR API KEY

```

* The apikey is the one that the `botfather` gives to you.

# Usage 

```
usage: sio-notification.py [-h] [-c CONFIG] [-i INFILE] [-v] [-F FILTER] [-f] [-m]

Simple Shout-it-out telegram notificator

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Full path to config file (default is ~/.SIO.conf
  -i INFILE, --infile INFILE
                        Send a text file (default is stdin)
  -v, --verbose         Turn on the verbose mode
  -F FILTER, --filter FILTER
                        Add a filter before sending the message (string: default: None)
  -f, --follow          Send one line at a time
  -m, --markdown        Force markdown on the entire message, if is not, do it by yourself adding backquotes

```


# Example and use case:


```bash

cat /etc/passwd | sio-notification.py

```

```
## To check for OOB via dns:

tail -f bind.log | sio-notification.py -v -f -m

```
