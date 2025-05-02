# argo-probe-eudat-b2handles
Three nagios probes are available: `check_handle_api.py`, `check_handle_resolution.pl` and optionally `check_epic_api.py`.

## check_handle_api.py

This plugin is a simple CRUD test of the Handle v8 JSON REST API service on the specified host and the specified prefix. It creates a handle named NAGIOS-{DATE}-{TIME}-{UUID}, and then tries to read it and update it with a new value, and finally tries to delete it.

It uses the PyHandle library (https://github.com/EUDAT-B2HANDLE/PYHANDLE).

### Required option:

`--file, -f <file>` : The JSON credentials file

### Optional options

`--debug, -d` : Debug mode

`--help, -h` : Print a help message and exit

`--timeout, -t <timeout>` : Timeout, in seconds

### Example:

`check_handle_api.py --file credentials.json`

### JSON credentials file example:
```
{
  "handle_server_url": "https://hdl.foo.com:8001",
  "private_key": "/path/to/privkey.pem",
  "certificate_only": "/path/to/certificate_only.pem",
  "prefix": "99.99942",
  "handleowner": "301:99.99942/FOOBAR"
  "HTTPS_verify": "True"
}
```

## check_handle_resolution.pl

This plugin retrieves all the master and mirror handle servers of the specified prefix. It then loops over all IPs to check if the specified suffix is readable.

If no suffix is specified, the default `EUDAT-B2HANDLE-CHECK` is checked.

### Options:

`--debug, -d` : Debug mode

`--help, -h` : Print a help message and exit

`--prefix, -p <prefix>` : The prefix to be tested

`--suffix, -s <suffix>` : The suffix to be tested

`--timeout, -t <timeout>` : Timeout, in seconds

### Examples:
```
check_handle_resolution.pl --prefix 12345 --debug

check_handle_resolution.pl --prefix 12345 --suffix MY_HANDLE --debug --timeout 10
```

## check_epic_api.py

This plugin is a simple CRUD test of the EPIC API service on the specified host and the specified prefix. It creates a handle named NAGIOS-{DATE}-{TIME}, and then tries to read it and update it with a new value, and finally tries to delete it.

It imports the `epicclient` module.

### Required options:

`--username, -U <user>` : The username used to authenticate with the EPIC service

`--url, -u <uri>` : The base URI of the EPIC API service to be tested

`--pass, -P <key>` : The API key of the username

`--prefix, -p <prefix>` : The prefix to be tested


### Optional options

`--debug, -d` : Debug mode

`--help, -h` : Print a help message and exit

`--timeout, -t <timeout>` : Timeout, in seconds

### Example:
```
check_epic_api.py \

	--url "https://epic.domain.com/api/v2/handles/" --prefix 12345 \

	--username nagios --pass deadbabe --debug
```

## Makefile
`make srpm` : Builds a source RPM package compatible with Red Hat Enterprise Linux 9.

`make rpm` : Builds a binary RPM package compatible with Red Hat Enterprise Linux 9.

`make rpm_with_epic` : Builds a binary RPM package that includes the check_epic_api.py probe and is compatible with Red Hat Enterprise Linux 9.

## Dependencies

The following dependencies are automatically installed by rpm :

### check_handle_api_py dependencies

OS repository:

```
python3
```

ARGO repository:

```
pyhandle
```

### check_handle_resolution.pl dependencies

OS repository:

```
perl-interprater
perl-JSON
```

### check_epic_api.py dependencies

OS repository:

```
python3
python3-lxml
```

EPEL repository:

```
python3-defusedxml
python3-httplib2
python3-simplejson
```

