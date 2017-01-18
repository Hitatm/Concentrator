## supervisor.addProcessGroup
	 Update the config for a running process from config file.

        @param string name         name of process group to add
        @return boolean result     true if successful
        
## supervisor.clearAllProcessLogs
	 Clear all process log files

        @return array result   An array of process status info structs
        
## supervisor.clearLog
	 Clear the main log.

        @return boolean result always returns True unless error
        
## supervisor.clearProcessLog
	 Clear the stdout and stderr logs for the named process and
        reopen them.

        @param string name   The name of the process (or 'group:name')
        @return boolean result      Always True unless error
        
## supervisor.clearProcessLogs
	 Clear the stdout and stderr logs for the named process and
        reopen them.

        @param string name   The name of the process (or 'group:name')
        @return boolean result      Always True unless error
        
## supervisor.getAPIVersion
	 Return the version of the RPC API used by supervisord

        @return string version version id
        
## supervisor.getAllConfigInfo
	 Get info about all available process configurations. Each struct
        represents a single process (i.e. groups get flattened).

        @return array result  An array of process config info structs
        
## supervisor.getAllProcessInfo
	 Get info about all processes

        @return array result  An array of process status results
        
## supervisor.getIdentification
	 Return identifying string of supervisord

        @return string identifier identifying string
        
## supervisor.getPID
	 Return the PID of supervisord

        @return int PID
        
## supervisor.getProcessInfo
	 Get info about a process named name

        @param string name The name of the process (or 'group:name')
        @return struct result     A structure containing data about the process
        
## supervisor.getState
	 Return current state of supervisord as a struct

        @return struct A struct with keys int statecode, string statename
        
## supervisor.getSupervisorVersion
	 Return the version of the supervisor package in use by supervisord

        @return string version version id
        
## supervisor.getVersion
	 Return the version of the RPC API used by supervisord

        @return string version version id
        
## supervisor.readLog
	 Read length bytes from the main log starting at offset

        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        
## supervisor.readMainLog
	 Read length bytes from the main log starting at offset

        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        
## supervisor.readProcessLog
	 Read length bytes from name's stdout log starting at offset

        @param string name        the name of the process (or 'group:name')
        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        
## supervisor.readProcessStderrLog
	 Read length bytes from name's stderr log starting at offset

        @param string name        the name of the process (or 'group:name')
        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        
## supervisor.readProcessStdoutLog
	 Read length bytes from name's stdout log starting at offset

        @param string name        the name of the process (or 'group:name')
        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        
## supervisor.reloadConfig
	
        Reload configuration

        @return boolean result  always return True unless error
        
## supervisor.removeProcessGroup
	 Remove a stopped process from the active configuration.

        @param string name         name of process group to remove
        @return boolean result     Indicates whether the removal was successful
        
## supervisor.restart
	 Restart the supervisor process

        @return boolean result  always return True unless error
        
## supervisor.sendProcessStdin
	 Send a string of chars to the stdin of the process name.
        If non-7-bit data is sent (unicode), it is encoded to utf-8
        before being sent to the process' stdin.  If chars is not a
        string or is not unicode, raise INCORRECT_PARAMETERS.  If the
        process is not running, raise NOT_RUNNING.  If the process'
        stdin cannot accept input (e.g. it was closed by the child
        process), raise NO_FILE.

        @param string name        The process name to send to (or 'group:name')
        @param string chars       The character data to send to the process
        @return boolean result    Always return True unless error
        
## supervisor.sendRemoteCommEvent
	 Send an event that will be received by event listener
        subprocesses subscribing to the RemoteCommunicationEvent.

        @param  string  type  String for the "type" key in the event header
        @param  string  data  Data for the event body
        @return boolean       Always return True unless error
        
## supervisor.shutdown
	 Shut down the supervisor process

        @return boolean result always returns True unless error
        
## supervisor.signalAllProcesses
	 Send a signal to all processes in the process list

        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return array         An array of process status info structs
        
## supervisor.signalProcess
	 Send an arbitrary UNIX signal to the process named by name

        @param string name    Name of the process to signal (or 'group:name')
        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return boolean
        
## supervisor.signalProcessGroup
	 Send a signal to all processes in the group named 'name'

        @param string name    The group name
        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return array
        
## supervisor.startAllProcesses
	 Start all processes listed in the configuration file

        @param boolean wait    Wait for each process to be fully started
        @return array result   An array of process status info structs
        
## supervisor.startProcess
	 Start a process

        @param string name Process name (or ``group:name``, or ``group:*``)
        @param boolean wait Wait for process to be fully started
        @return boolean result     Always true unless error

        
## supervisor.startProcessGroup
	 Start all processes in the group named 'name'

        @param string name     The group name
        @param boolean wait    Wait for each process to be fully started
        @return array result   An array of process status info structs
        
## supervisor.stopAllProcesses
	 Stop all processes in the process list

        @param  boolean wait   Wait for each process to be fully stopped
        @return array result   An array of process status info structs
        
## supervisor.stopProcess
	 Stop a process named by name

        @param string name  The name of the process to stop (or 'group:name')
        @param boolean wait        Wait for the process to be fully stopped
        @return boolean result     Always return True unless error
        
## supervisor.stopProcessGroup
	 Stop all processes in the process group named 'name'

        @param string name     The group name
        @param boolean wait    Wait for each process to be fully stopped
        @return array result   An array of process status info structs
        
## supervisor.tailProcessLog
	
        Provides a more efficient way to tail the (stdout) log than
        readProcessStdoutLog().  Use readProcessStdoutLog() to read
        chunks and tailProcessStdoutLog() to tail.

        Requests (length) bytes from the (name)'s log, starting at
        (offset).  If the total log size is greater than (offset +
        length), the overflow flag is set and the (offset) is
        automatically increased to position the buffer at the end of
        the log.  If less than (length) bytes are available, the
        maximum number of available bytes will be returned.  (offset)
        returned is always the last offset in the log +1.

        @param string name         the name of the process (or 'group:name')
        @param int offset          offset to start reading from
        @param int length          maximum number of bytes to return
        @return array result       [string bytes, int offset, bool overflow]
        
## supervisor.tailProcessStderrLog
	
        Provides a more efficient way to tail the (stderr) log than
        readProcessStderrLog().  Use readProcessStderrLog() to read
        chunks and tailProcessStderrLog() to tail.

        Requests (length) bytes from the (name)'s log, starting at
        (offset).  If the total log size is greater than (offset +
        length), the overflow flag is set and the (offset) is
        automatically increased to position the buffer at the end of
        the log.  If less than (length) bytes are available, the
        maximum number of available bytes will be returned.  (offset)
        returned is always the last offset in the log +1.

        @param string name         the name of the process (or 'group:name')
        @param int offset          offset to start reading from
        @param int length          maximum number of bytes to return
        @return array result       [string bytes, int offset, bool overflow]
        
## supervisor.tailProcessStdoutLog
	
        Provides a more efficient way to tail the (stdout) log than
        readProcessStdoutLog().  Use readProcessStdoutLog() to read
        chunks and tailProcessStdoutLog() to tail.

        Requests (length) bytes from the (name)'s log, starting at
        (offset).  If the total log size is greater than (offset +
        length), the overflow flag is set and the (offset) is
        automatically increased to position the buffer at the end of
        the log.  If less than (length) bytes are available, the
        maximum number of available bytes will be returned.  (offset)
        returned is always the last offset in the log +1.

        @param string name         the name of the process (or 'group:name')
        @param int offset          offset to start reading from
        @param int length          maximum number of bytes to return
        @return array result       [string bytes, int offset, bool overflow]
        
## system.listMethods
	 Return an array listing the available method names

        @return array result  An array of method names available (strings).
        
## system.methodHelp
	 Return a string showing the method's documentation

        @param string name   The name of the method.
        @return string result The documentation for the method name.
        
## system.methodSignature
	 Return an array describing the method signature in the
        form [rtype, ptype, ptype...] where rtype is the return data type
        of the method, and ptypes are the parameter data types that the
        method accepts in method argument order.

        @param string name  The name of the method.
        @return array result  The result.
        
## system.multicall
	Process an array of calls, and return an array of
        results. Calls should be structs of the form {'methodName':
        string, 'params': array}. Each result will either be a
        single-item array containing the result value, or a struct of
        the form {'faultCode': int, 'faultString': string}. This is
        useful when you need to make lots of small calls without lots
        of round trips.

        @param array calls  An array of call requests
        @return array result  An array of results
        
[Finished in 0.1s]