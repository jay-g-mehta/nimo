# NIMO
NIMO is Nova Instance Monitoring tool.

It uses libvirt-python module to connect with libvirt on hypervisor, and get callbacks for
VM instance life cycle events.

## Download, Setup and Installing NIMO
```
$ virtualenv -v -p python2.7 virtual_env
$ source virtual_env/bin/activate
$ cd nimo
$ pip -v install .
```

## Running nimo
```
$ nimo --config-file=./etc/nimo/nimo.conf --log-file=/var/log/nimo/nimo.log
```