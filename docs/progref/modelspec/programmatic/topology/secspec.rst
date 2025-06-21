.. _secspec:

.. _CurrentlyAccessedSection:

Section and Segment Selection
=============================

Dot notation for properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. tab:: Python

        Since sections share property names eg. a length called :data:`L` 
        it is always necessary to specify *which* section is being discussed;
        this is done using dot notation, e.g.

        .. code-block::
            python

            dendrite[2].L = dendrite[1].L + dendrite[0].L 
            axon.v = soma.v 
            print(soma.gnabar)
            axon.nseg *= 3

        This notation is necessary when one needs to refer to more than 
        one section within a single statement. 

    .. tab:: HOC

        This takes precedence over the other methods and 
        is described by the syntax :samp:`{sectionname}.varname`. Examples 
        are 

        .. code-block::
            none

            dendrite[2].L = dendrite[1].L + dendrite[0].L 
            axon.v = soma.v 
            print soma.gnabar 
            axon.nseg = 3*axon.nseg 

        This notation is necessary when one needs to refer to more than 
        one section within a single statement. 

Stack of sections
~~~~~~~~~~~~~~~~~

    .. tab:: HOC

        The syntax is 

        .. code-block::
            none

            sectionname {stmt} 

        and means that the currently selected section during the 
        execution of *stmt* 
        is *sectionname*. This method is the most useful for 
        programming since the user has explicit control over 
        the scope of the section and can set several range variables. 
        Notice that after the *stmt* is executed the currently selected 
        section reverts 
        to the name (if any) it had before *sectionname* was seen. The 
        programmer is allowed to 
        nest these statements to any level. 
        Avoid the error: 

        .. code-block::
            none

                    soma L=10 diam=10 

        which sets ``soma.L``, then pops the section stack and sets :hoc:data:`diam`
        for whatever section is then on the stack. 
        
        It is important that control flow reach the end of *stmt* in order to 
        automatically pop the section stack. Therefore, one cannot use 
        the :ref:`continue <hoc_keyword_continue>`, :ref:`break <hoc_keyword_break>`, or :ref:`return <hoc_keyword_return>` statements in *stmt*.
        
        There is no explicit notion of a section variable in NEURON but the same 
        effect can be obtained with the :hoc:class:`SectionRef` class. The use of :hoc:func:`push_section`
        for this purpose is not recommended except as a last resort. 
        
        Looping over sets of sections is done most often with the :ref:`forall <hoc_keyword_forall>` and :ref:`forsec <hoc_keyword_forsec>`
        commands. 
        

Default section
~~~~~~~~~~~~~~~

    .. tab:: HOC
        
        The syntax 

        .. code-block::
            none

            access sectionname 

        defines a default section name to be the currently selected section when the 
        first two methods are not in effect. There is often a conceptually 
        privileged section which gets most of the use and it is useful to 
        declare that as the default section. e.g. 

        .. code-block::
            none

            access soma 

        With this, one can, with a minimum of typing, get values of voltage, etc 
        at 
        the command line level. 
        
        In general, this statement should only be used once to give default access 
        to a privileged section. It's bad programming practice to change the 
        default access within anything other than an initialization procedure. 
        The "``sec { stmt }``" form is almost always the right way to 
        use the section stack. 

                
                

        ----


        .. index::  access (keyword)


        .. _hoc_keyword_access:

        **access**


            Syntax:
                ``access section``



            Description:
                Makes *section* the default currently accessed section. 
                More precisely, it replaces the top of the section stack with the 
                indicated section and so will be the permanent default section only if 
                the section stack is empty or has only one section in it. 
                This is lesser 
                precedence than 
                ``section stmt`` 
                which is lesser precedence than 
                ``section.var`` 
                
                Note: 
                
                The access statement should not be used within a procedure or function. In 
                fact the best style is to execute it only once in a program to refer to 
                a priviledged section such as "soma". It can be very confusing when a 
                procedure has the side effect of permanently changing the default section. 

            Example:

                .. code-block::
                    none

                    create a, b, c, d 
                    access a  
                    print secname()  
                    b {  
                            print secname()  
                            access c        // not recommended. The "go_to" of sections. 
                            print secname()  
                            d {print secname()} 
                            print secname() 
                    } // because the stack has more than one section, c is popped off 
                    print secname()	// and the second "access" was not permanent! 


                

        ----


        .. index::  forall (keyword)


        .. _hoc_keyword_forall:

        **forall**

            Syntax:
                ``forall stmt``



            Description:
                Loops over all sections, successively making each section the currently 
                accessed section. 
                
                Within an object, ``forall`` refers to all the sections 
                declared in the object. This is generally the right thing to do when a template 
                creates sections but is inconvenient when a template is constructed which 
                needs to compute using sections external to it. In this case, one can pass a collection 
                of sections into a template function as a :hoc:class:`SectionList` object argument.
                
                The ``forall`` is relatively slow, 
                especially when used in conjunction with :hoc:func:`issection`
                and :hoc:func:`ismembrane` selectors. If you are often iterating over the same
                sets it is much faster to keep the sets in :hoc:class:`SectionList` objects and use
                the much faster :ref:`forsec <hoc_keyword_forsec>` command.
                
                The iteration sequence order is undefined but will remain the same for 
                a given sequence of :ref:`create <hoc_keyword_create>` statements.
                

            Example:

                .. code-block::
                    none

                    create soma, axon, dend[3] 
                    forall { 
                        print secname() 
                    } 

                prints the names of all the sections which have been created. 

                .. code-block::
                    none

                    soma 
                    axon 
                    dend[0] 
                    dend[1] 
                    dend[2] 

            .. seealso::
                :ref:`forsec <hoc_keyword_forsec>`, :ref:`ifsec <hoc_keyword_ifsec>`, :hoc:func:`issection`, :hoc:func:`SectionList`, :hoc:func:`ismembrane`

                

        ----



        .. index::  ifsec (keyword)


        .. _hoc_keyword_ifsec:

        **ifsec**

            Syntax:
                ``ifsec string stmt``

                ``ifsec sectionlist stmt``


            Description:


                ifsec string stmt 
                    Executes stmt if string is contained in the name of the currently 
                    accessed section.  equivalent to :samp:`if(issection({string}))` stmt 
                    Note that the regular expression semantics is not the same as that 
                    used by issection. To get an exact match use 
                    ifsec ^string$ 

                ifsec sectionlist stmt 
                    Executes stmt if the currently accessed section is in the sectionlist. 


            .. seealso::
                :ref:`forsec <hoc_keyword_forsec>`, :hoc:class:`SectionList`, :hoc:func:`issection`

                

        ----



        .. index::  forsec (keyword)


        .. _hoc_keyword_forsec:

        **forsec**
            Syntax:
                ``forsec string stmt``

                ``forsec sectionlist stmt``



            Description:


                forsec string stmt 
                    equivalent to ``forall ifsec string stmt`` but faster. 
                    Note that forsec string is equivalent to 
                    :samp:`forall if (issection({string})) stmt` 

                forsec sectionlist 
                    equivalent to ``forall ifsec sectionlist stmt`` but very fast. 

                These provide a very efficient iteration over the list of sections. 

            Example:

                .. code-block::
                    none

                    create soma, dend[3], axon 
                    forsec "a" print secname() 


                .. code-block::
                    none

                    create soma, dend[3], axon 
                    objref sl 
                    sl = new SectionList() 
                    for (i = 2; i >= 0; i = i - 1) dend[i] sl.append() 
                    forsec sl print secname() 



sec= for functions
~~~~~~~~~~~~~~~~~~

    .. tab:: Python

        Many NEURON functions refer to a specific Section. In recent versions of NEURON,
        most of these either are available as section methods or take a section or segment
        directly. For older code or for the remaining exceptions, the active section may
        be specified using a ``sec=`` keyword argument.

        For example:

        .. code-block::
            python

            my_iclamp = n.IClamp(0.25, sec=soma)   # better to use n.IClamp(soma(0.25)) though
            num_pts_3d = n.n3d(sec=apical)         # could get the same value as an int via apical.n3d()

Default section
~~~~~~~~~~~~~~~

If no ``sec=`` keyword argument is specified, the functions will use NEURON's
default Section (sometimes called the *currently accessed section*),
which can be identified via ``n.cas()``.
The default Section is controlled by a stack; it is initially
the first Section created but entries may be pushed onto or popped off of the
stack by the following commands. *Use this only as a last resort.*


.. function:: pop_section

    .. tab:: Python
    
    
        Syntax:
            ``n.pop_section()``


        Description:
            Take the currently accessed section off the section stack. This can only be used after 
            a function which pushes a section on the section stack such as 
            ``point_process.getloc()``. 

        Example:

            .. code-block::
                python

                from neuron import n
            
                soma = n.Section('soma')
                apical = n.Section('apical')
                stims = [n.IClamp(soma(i / 4.)) for i in range(5)] + [n.IClamp(apical(0.5))]
                for stim in stims: 
                    x = stim.get_loc() 
                    print(f"location of {stim} is {n.secname()}({x})")
                    n.pop_section() 
            
            (Note: in this example as ``nseg=1``, the current clamps will either be at position 0, 0.5, or 1.)

            (Note: a more Pythonic way to get the location of the point-process ``stim`` is to use ``seg = stim.get_segment()``,
            but this is shown as an example of using ``n.pop_section()``.)


         

    .. tab:: HOC


        Syntax:
            ``pop_section()``
        
        
        Description:
            Take the currently accessed section off the section stack. This can only be used after 
            a function which pushes a section on the section stack such as 
            ``point_process.getloc()``. 
        
        
        Example:
        
        
            .. code-block::
                none
        
        
                create soma[5] 
                objref stim[5] 
                for i=0,4 soma[i] stim[i] = new IClamp(i/4) 
                for i=0,4 { 
                    x = stim[i].get_loc() 
                    printf("location of %s is %s(%g)\n", stim[i], secname(), x) 
                    pop_section() 
                } 
        
----



.. function:: push_section

    .. tab:: Python
    
    
        Syntax:
            ``n.push_section(number)``

            ``n.push_section(section_name)``


        Description:
            This function, along with ``n.pop_section()`` should only be used as a last resort. 
            It will place a specified section on the top of the section stack, 
            becoming the current section to which all operations apply. It is 
            probably always better to use :class:`SectionRef` 
            or :class:`SectionList` . 


            :samp:`push_section({number})` 
                Push the section identified by the number returned by 
                ``n.this_section()``, etc. which you desire to be the currently accessed 
                section. Any section pushed must have a corresponding ``n.pop_section()``
                later or else the section stack will be corrupted. The number is 
                not guaranteed to be the same across separate invocations of NEURON. 

            :samp:`push_section({section_name})`
                Push the section identified by the name obtained 
                from sectionname(*strdef*). Note: at this time the implementation 
                iterates over all sections to find the proper one; so do not use 
                in loops. 


        Example:

            .. code-block::
                python

                from neuron import n

                soma = n.Section('soma')
                apical = n.Section('apical')

                # get a number to allow pushing by number
                soma_id = n.this_section(sec=soma)

                # push by name
                n.push_section('apical')

                # push by number
                n.push_section(soma_id)

                # RuntimeError -- no such section
                n.push_section('basal')


        .. seealso::
            :class:`SectionRef`

         
         

    .. tab:: HOC


        Syntax:
            ``push_section(number)``
        
        
            ``push_section(section_name)``
        
        
        Description:
            This function, along with ``pop_section()`` should only be used as a last resort. 
            It will place a specified section on the top of the section stack, 
            becoming the current section to which all operations apply. It is 
            probably always better to use :class:`SectionRef`
            or :class:`SectionList` .
        
        
            :samp:`push_section({number})` 
                Push the section identified by the number returned by 
                this_section, etc. which you desire to be the currently accessed 
                section. Any section pushed must have a corresponding pop_section() 
                later or else the section stack will be corrupted. The number is 
                not guaranteed to be the same across separate invocations of NEURON. 
        
        
            :samp:`push_section({section_name})`
                Push the section identified by the name obtained 
                from sectionname(*strdef*). Note: at this time the implementation 
                iterates over all sections to find the proper one; so do not use 
                in loops. 
        
        
        .. seealso::
            :class:`SectionRef`
        
