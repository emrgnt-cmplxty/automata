PyCodeWriterToolkitBuilder
==========================

Overview
--------

``PyCodeWriterToolkitBuilder`` is a class developed for interacting with
the PythonWriter API. The class provides functionality to modify python
code with the help of built-in methods that can create or update
existing python modules. Class’s initialization requires an instance of
``PyCodeWriter`` and a boolean variable ``do_write`` deciding whether to
write these changes to disk.

Important methods contained in this class include ``build``,
``_update_existing_module``, and ``_create_new_module``. The ``build``
method generates a toolkit that includes two functionalities: updating
existing python code and creating a new python module. If a required
object doesn’t exist in the module being modified, it is created
automatically. If it already exists, the existing code is modified. To
create a new module, the complete code is provided as a parameter.

Related Symbols
---------------

-  ``automata.tools.builders.AgentToolkitBuilder``
-  ``automata.tools.builder.PyCodeWriter``

Example
-------

The following examples demonstrate how to use
``PyCodeWriterToolkitBuilder`` for modifying an existing python module
and creating a new python module.

.. code:: python

   from automata.tools.builders.py_writer_builder import PyCodeWriterToolkitBuilder
   from automata.tools.writer import PyCodeWriter

   py_writer = PyCodeWriter()
   py_writer_builder_toolkit = PyCodeWriterToolkitBuilder(py_writer)

   update_module_tool = py_writer_builder_toolkit.build()[0]
   result = update_module_tool.function('my_folder.my_file.MyClass', 'def my_method():\n   "My Method"\n    print("hello world")\n')

   create_module_tool = py_writer_builder_toolkit.build()[1]
   result = create_module_tool.function('my_folder.my_new_file', 'import math\ndef my_method():\n   "My Method"\n    print(math.sqrt(4))\n')

Limitations
-----------

The primary limitation is that ``PyCodeWriterToolkitBuilder`` can only
modify the python code of an existing module or create a new module with
provided complete code. This toolkit has no context outside of the
passed arguments. Any additional statements, especially any import
statements that the code block may depend upon, should be included
within the code block itself.

Also, Error handling within the toolkit can return generic exceptions
which might not provide a clear understanding of the exact issue
limiting the ease of debugging.

Follow-up Questions:
--------------------

-  Could we provide a way to have better error handling or return more
   specific exceptions? Would that help usability in large projects?
-  Can we provide the ability to read and write the changes on the go as
   per user requirements?
-  Is there a possibility to add a feature that can directly modify code
   within the actual Project’s structure itself?
