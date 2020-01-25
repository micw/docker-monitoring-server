


## Configuration options (via environment variable)

### Backend

* BACKEND_ADDRESS (required) - host and port of the backend (e.g. icinga2:6558)
* BACKEND_NAME (default: DefaultBackend) - name of the backend
* BACKEND_TYPE (default: livestatus) - name of the backend
* BACKEND_LMD (default: off) - enable/disable LMD proxy for backend
  (allowed values: on/off)
* BACKEND_ICINGA_FEATURES (default: off) - enable/disable icinga specific features
  (allowed values: on/off)

### Logging

All logging goes to stdout of the docker container.

* APACHE_ERROR_LOG (default: on) - enabled/disable apache error log
  (allowed values: on/off)

* APACHE_ACCESS_LOG (default: off) - enabled/disable apache access log
  (allowed values: on/off)

* THRUK_LOG_LEVEL (default 'WARN') - set log level for thruk
  (allowed values:  OFF, FATAL, ERROR, WARN, INFO, DEBUG, TRACE, ALL)
