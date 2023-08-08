DotPathMap
==========

Overview
--------

``DotPathMap`` is a class that creates a mapping from module dot paths
to module file paths. The aim of this class is to facilitate the
efficient retrieval and manipulation of files within a project or module
hierarchy structure. This is achieved by creating a dictionary where the
keys are module dot paths and the values are corresponding file paths.

The class initializes with a provided file path and project name,
converting the project name into a prefix replacing path separators with
dots. It then builds two dictionaries to store dot path to file path
mapping and vice versa.

There are also methods to add (``put_module``) or remove
(``delete_module``) module information into/from these dictionaries.

Related Symbols
---------------

-  ‘automata.code_parsers.py.dotpath_map.DotPathMap.get_module_fpath_by_dotpath’
-  ‘automata.code_parsers.py.dotpath_map.DotPathMap.items’
-  ‘automata.code_parsers.py.dotpath_map.DotPathMap.contains_dotpath’
-  ‘automata.code_parsers.py.dotpath_map.DotPathMap.contains_fpath’
-  ‘automata.code_parsers.py.dotpath_map.DotPathMap.get_module_dotpath_by_fpath’
-  ‘automata.code_parsers.py.dotpath_map.convert_fpath_to_module_dotpath’

Example
-------

The following is an example demonstrating the usage of ``DotPathMap``.
Assume a project structure as follows:

::

   my_project
   │   main.py
   │
   └───core
   │   │   calculator.py
   │   │   calculator2.py
   │   │
   │   └───extended
   │       │   calculator3.py
   │   
   └───utils
       │   util1.py

Now, to create a ``DotPathMap`` instance for this project structure, and
perform some operations:

.. code:: python

   from automata.code_parsers.py.dotpath_map import DotPathMap

   # Create an instance of DotPathMap
   dotpath_map = DotPathMap(path='/path/to/my_project', project_name='my_project')

   # Fetch file path of a module using dot path
   file_path = dotpath_map.get_module_fpath_by_dotpath('my_project.core.calculator')
   print(file_path)  # Output: /path/to/my_project/core/calculator.py

   # Check if a dot path exists in the map
   exists = dotpath_map.contains_dotpath('my_project.core.calculator')
   print(exists)  # Output: True

   # Remove a module using dot path
   dotpath_map.delete_module('my_project.core.calculator')

   # Add a module using dot path
   dotpath_map.put_module('my_project.new_module.new_file')

Limitations
-----------

The ``DotPathMap`` class assumes all files in the project are Python
files (‘.py’). It can’t map other file types.

Follow-up Questions:
--------------------

-  Will the design allow for other file types besides ‘.py’?
-  What happens if identical module names exist in different
   directories?
-  Is there a way to reload the DotPathMap in the event of changes to
   the filesystem?
