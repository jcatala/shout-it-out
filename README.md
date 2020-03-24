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
usage: main.py [-h] [-c CONFIG] [-f FILE] [-v]

Simple Shout-it-out telegram notificator

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Full path to config file (default is ~/.SIO.conf
  -f FILE, --file FILE  Send a text file (default is stdin)
  -v, --verbose         Turn on the verbose mode

```


# Example and use case:


```bash

cat /etc/passwd | sio-notification.py

```

```
## To check for OOB via dns:

tail -f bind.log | sio-notification.py

```
