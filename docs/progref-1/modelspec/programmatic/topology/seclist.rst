.. _seclist:

    .. tab:: Python

        
        SectionList
        -----------
        
        
        

    .. tab:: HOC

        SectionList
        -----------
----

.. class:: SectionList

    .. tab:: Python
    
    
        Syntax:
            ``sl = n.SectionList()``

            ``sl = n.SectionList(python_iterable_of_sections)``


        Description:
            Class for creating and managing a list of sections. Unlike a regular Python list, a ``SectionList`` allows including sections
            based on neuronal morphology (e.g. subtrees).

            If ``sl`` is a :class:`SectionList`, then to turn that into a Python list, use ``py_list = list(sl)``; note
            that iterating over a SectionList is supported, so it may not be neccessary to create a Python list.

            The second syntax creates a SectionList from the Python iterable and is equivalent
            to:

            .. code-block::
                python

                sl = n.SectionList()
                for sec in python_iterable_of_sections:
                    sl.append(sec)

            ``len(sl)`` returns the number of sections in the SectionList.

            ``list(sl)`` and ``[s for s in sl]`` generate equivalent lists.

        .. seealso::
            :class:`SectionBrowser`, :class:`Shape`, :meth:`RangeVarPlot.list`

         

    .. tab:: HOC


        Syntax:
            ``sl = new SectionList()``
        
        
        Description:
            Class for creating and managing a list of sections 
        
        
        .. seealso::
            :class:`SectionBrowser`, :class:`Shape`, :ref:`forsec <hoc_keyword_forsec>`, :meth:`RangeVarPlot.list`
        
----



.. method:: SectionList.append

    .. tab:: Python
    
    
        Syntax:
            ``sl.append(section)``
        
            ``sl.append(sec=section)``


        Description:
            append ``section`` to the list 

         

    .. tab:: HOC


        Syntax:
            ``sl.append()``
        
        
        Description:
            append the currently accessed section to the list 
        
----



.. method:: SectionList.remove

    .. tab:: Python
    
    
        Syntax:
            ``n = sl.remove(sec=section)``

            ``n = sl.remove(sectionlist)``


        Description:
            Remove ``section`` from the list.

            If ``sectionlist`` is present then all the sections in sectionlist are 
            removed from sl. 

            Returns the number of sections removed. 

         

    .. tab:: HOC


        Syntax:
            ``n = sl.remove()``
        
        
            ``n = sl.remove(sectionlist)``
        
        
        Description:
            remove the currently accessed section from the list 
            If the argument is present then all the sections in sectionlist are 
            removed from sl. 
            Returns the number of sections removed. 
        
----



.. method:: SectionList.children

    .. tab:: Python
    
    
        Syntax:
            ``sl.children(section)``

            ``sl.children(sec=section)``


        Description:
            Appends the sections connected to ``section``. 
            Note that this includes children connected at position 0 of 
            parent. 
    
        .. note::

            To get a (Python) list of a section's children, use the section's
            ``children`` method. For example:

            .. code::
                python

                >>> from neuron import n
                >>> s = n.Section('s')
                >>> t = n.Section('t')
                >>> u = n.Section('u')
                >>> t.connect(s)
                t
                >>> u.connect(s)
                u
                >>> t.children()
                []
                >>> s.children()
                [u, t]

         

    .. tab:: HOC


        Syntax:
            ``sl.children()``
        
        
        Description:
            Appends the sections connected to the currently accessed section. 
            Note that this includes children connected at position 0 of 
            parent. 
        
----



.. method:: SectionList.subtree

    .. tab:: Python
    
    
        Syntax:

            ``sl.subtree(section)``
    
            ``sl.subtree(sec=section)``


        Description:
            Appends the subtree of the ``section``. (including that one). 

        .. note::

            To get a (Python) list of a section's subtree, use the section's
            ``subtree`` method.         

        .. seealso::
            :meth:`Section.subtree`

    .. tab:: HOC


        Syntax:
            ``sl.subtree()``
        
        
        Description:
            Appends the subtree of the currently accessed section (including that one). 
        
----



.. method:: SectionList.wholetree

    .. tab:: Python
    
    
        Syntax:

            ``sl.wholetree(section)``

            ``sl.wholetree(sec=section)``


        Description:
            Appends all sections which have a path to the ``section``. 
            (including the specified section). The section list has the 
            important property that the sections are in root to leaf order. 

        .. note::

            To get a (Python) list of a section's wholetree, use the section's
            ``wholetree`` method. 

        .. seealso::
            :meth:`Section.wholetree`
         

    .. tab:: HOC


        Syntax:
            ``sl.wholetree()``
        
        
        Description:
            Appends all sections which have a path to the currently accessed section 
            (including the currently accessed section). The section list has the 
            important property that the sections are in root to leaf order. 
        
----



.. method:: SectionList.allroots

    .. tab:: Python
    
    
        Syntax:
            ``sl.allroots()``


        Description:
            Appends all the root sections. Root sections have no parent section. 
            The number of root sections is the number 
            of real cells in the simulation. 

         

    .. tab:: HOC


        Syntax:
            ``sl.allroots()``
        
        
        Description:
            Appends all the root sections. Root sections have no parent section. 
            The number of root sections is the number 
            of real cells in the simulation. 
        
----



.. method:: SectionList.unique

    .. tab:: Python
    
    
        Syntax:
            ``n = sl.unique()``


        Description:
            Removes all duplicates of sections in the SectionList. I.e. ensures that 
            no section appears more than once. Returns the number of sections references 
            that were removed. 

         

    .. tab:: HOC


        Syntax:
            ``n = sl.unique()``
        
        
        Description:
            Removes all duplicates of sections in the SectionList. I.e. ensures that 
            no section appears more than once. Returns the number of sections references 
            that were removed. 
        
----



.. method:: SectionList.printnames

    .. tab:: Python
    
    
        Syntax:
            ``.printnames()``


        Description:
            print the names of the sections in the list. 

            ``sl.printnames()`` is approximately equivalent to:

            .. code::
                python

                for sec in sl:
                    print(sec)
         

    .. tab:: HOC


        Syntax:
            ``.printnames()``
        
        
        Description:
            print the names of the sections in the list. 
        
        
            The normal usage of a section list involves efficiently iterating 
            over all the sections in the list with 
            ``forsec sectionlist {statement}``
        
