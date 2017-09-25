# NIMO
NIMO is Nova Instance Monitoring tool.

NIMO tracks life cycle events for every VM running on a hypervisor.
On create, reboot events on a VM, NIMO will reconnaissance boot stages of that
VM. These boot stages are sent to configured RMQ service as event messages.

NIMO uses libvirt-python module to connect with libvirt on hypervisor, and
get callbacks for VM instance life cycle events.
NIMO makes use of reconn module to perform reconnaissance on console.log
file of the VM.


## Download, Setup and Installing NIMO
```
$ virtualenv -v -p python2.7 virtual_env
$ source virtual_env/bin/activate
$ cd nimo
$ pip -v install .
```

## Running NIMO
```
$ nimo --config-file=./etc/nimo/nimo.conf --log-file=/var/log/nimo/nimo.log
```


## Developing and testing NIMO
##### Unit test execution:
Unit tests are located under: nimo/nimo/tests/unit/
```
$ cd nimo
$ tox -epy27
```
