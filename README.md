taht
====

"taht" is "that" misspelled on purpose.

Outside the python standard library it uses the
[Requests](http://python-requests.org) module for HTTP client functionality
and [Flask](http://flask.pocoo.org) for HTTP server functionality.

## Howto

- Clone the git repo

- On a separate window start up server.py

- On your main window run client.py

- Kill them both when you are done

## The making of

- `server.py` is a rogue HTTP server. It only accepts request to '/'
  it returns random error codes even though every now and then it will
  produce actual content and a 200 status code. Beware though because
  even then the response content also varies randomly. Essentially it
  is used to model an unreliable HTTP-abiding resource.

- `client.py` is the actual multiprocess monitoring client. It's
  nothing fancy: creates a process for each resource to monitor and
  runs harnessed HTTP GET verbs with the information contained in each
  `Resource` class. How to deal with the returned content is define in
  the configuration file.

- `config.py` is the configuration file and is valid executable python
  code. There it defines a `Resource` type and a list of resources to
  monitor. Notice than some resources are monitored more than once in
  order to increase the number of processes and the chances of race
  conditions to happen.

- The `Resource` type requires a name, a url, a function generating
  polling intervals and a content checking function.

- `monitor.py` essentially defines an execution harness for HTTP
  requests. Sometimes i has come to my mind something like this in
  cloud environments and somehow I thought today was a good day to
  implement something like this. The number of test cases kind of
  reflect the creation process. It uses a python decorator instead of
  implementing a decorator pattern, YMMV.

- There is a `Logger` class which is nothing else than a print
  function protected with a lock in order to avoid race
  conditions. More complex logging can be constructed but the sync
  primitives will be needed anyway. Notice that it becomes a single
  resource under potentially heavy demand hence it may produce
  contention.


