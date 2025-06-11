.. _timer:

Timer
-----



.. class:: Timer

    .. tab:: Python
    
    
        Syntax:
            ``timer = n.Timer(python_func)``


        Description:
            Execute a Python function at the end of each interval specified by timer.seconds(interval). 
            The timer must be started and can be stopped. 
            A Timer is used to implement the :menuselection:`NEURON Main Menu --> Tools --> MovieRun` in 
            :file:`nrn/lib/hoc/movierun.hoc`

        .. warning::
            This code must be run with ``nrniv -python`` and not directly via ```python```.
            The better solution is to `use Python's threading module <https://docs.python.org/3/library/threading.html>`_
            which works regardless of how NEURON is launched.
            


        Example:

            .. code-block::
                python

                from neuron import n

                def foo():
                    print('Hello')

                timer = n.Timer(foo)
                timer.seconds(1)
                timer.start()
                # type timer.end() to end timer


         

    .. tab:: HOC


        Syntax:
            ``timer = new Timer("stmt")``
        
        
        Description:
            Execute "stmt" at the end of each interval specified by timer.seconds(interval). 
            The timer must be started and can be stopped. 
            A Timer is used to implement the :menuselection:`NEURON Main Menu --> Tools --> MovieRun` in 
            :file:`nrn/lib/hoc/movierun.hoc`
        
        
        Example:
        
        
            .. code-block::
                none
        
        
                load_file("nrngui.hoc") 
                objref timer 
                timer = new Timer("p()") 
                invl = .2 
                nstep = 10 
                proc p() {local x 
                    istep += 1 
                    tt = startsw() - t0 
                    print istep, tt 
                    if (istep >= nstep) { 
                            timer.end() 
                    } 
                    doNotify() 
                } 
                proc begin() { 
                    istep = 0 
                    timer.seconds(invl) 
                    t0 = startsw() 
                    tt = 0 
                    timer.start() 
                } 
        
        
                xpanel("Timer Demo") 
                    xbutton("Start", "begin()") 
                    xbutton("Stop", "timer.end()") 
                    xpvalue("Interval", &invl, 1) 
                    xpvalue("#steps", &nstep, 1) 
                    xpvalue("istep", &istep) 
                    xpvalue("t", &tt) 
                xpanel() 
                begin() 
        
----



.. method:: Timer.seconds

    .. tab:: Python
    
    
        Syntax:
            ``interval = timer.seconds()``

            ``interval = timer.seconds(interval)``


        Description:
            Specify the timer interval. Timer resolution is system dependent but is probably 
            around 10 ms. 
            The time it takes to execute the Python function is part of the interval. 

         

    .. tab:: HOC


        Syntax:
            ``interval = timer.seconds()``
        
        
            ``interval = timer.seconds(interval)``
        
        
        Description:
            Specify the timer interval. Timer resolution is system dependent but is probably 
            around 10 ms. 
            The time it takes to execute the "stmt" is a part of the interval. 
        
----



.. method:: Timer.start

    .. tab:: Python
    
    
        Syntax:
            ``timer.start()``


        Description:
            Start the timer. The Python function will be called at the end of each interval defined 
            by the argument to timer.seconds(interval). 

         

    .. tab:: HOC


        Syntax:
            ``timer.start()``
        
        
        Description:
            Start the timer. "stmt" will be called at the end of each interval defined 
            by the argument to timer.seconds(interval). 
        
----



.. method:: Timer.end

    .. tab:: Python
    
    
        Syntax:
            ``timer.end()``


        Description:
            Stop calling the Python function. At least on Linux, this will prevent the calling 
            of the function at the end of the current interval. 

         

    .. tab:: HOC


        Syntax:
            ``timer.end()``
        
        
        Description:
            Stop calling the "stmt". At least on linux, this will prevent the calling 
            of "stmt" at the end of the current interval. 
        
