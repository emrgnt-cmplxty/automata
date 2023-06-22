ToolkitBuilder
==============

``ToolkitBuilder`` is a class for building toolkits of various types. It
provides an interface to create toolkits containing different tools for
specific purposes such as symbol search, code retrieval, code writing,
and context oracle. The class works with closely related symbols like
``Toolkit``, ``ToolkitType``, ``UnknownToolError``, and
``AgentToolFactory`` to help in creating and customizing toolkits.

Overview
--------

``ToolkitBuilder`` takes a toolkit type as input and creates a
corresponding toolkit of tools. It uses the ``AgentToolFactory`` to
create an agent tool of the provided toolkit type which is then built
into a toolkit. A toolkit can contain a number of tools for various
purposes such as code retrieval, code writing, symbol search, and
context oracle.

Related Symbols
---------------

-  ``automata.core.base.tool.Toolkit``
-  ``automata.core.base.tool.ToolkitType``
-  ``automata.core.agent.tools.tool_utils.UnknownToolError``
-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``automata.core.agent.tools.tool_utils.AgentToolFactory``

Example
-------

The following example demonstrates how to create and build a toolkit
using the ``ToolkitBuilder`` class.

.. code:: python

   from automata.core.agent.tools.tool_utils import ToolkitBuilder
   from automata.core.base.tool import ToolkitType

   # Create a ToolkitBuilder instance
   builder = ToolkitBuilder()

   # Build a toolkit of type SYMBOL_SEARCHER
   toolkit = builder.build_toolkit(ToolkitType.SYMBOL_SEARCHER)

Limitations
-----------

The primary limitation of ``ToolkitBuilder`` is that it relies on the
predefined available toolkits specified in ``ToolkitType``. It cannot
create custom toolkits or tools that are not defined within the scope of
the predefined toolkit types. Additionally, ``ToolkitBuilder`` assumes
that all the necessary arguments required for creating the agent tool
are provided in the ``kwargs`` argument during the initialization of the
class; otherwise, it may raise a ``ToolCreationError``.

Follow-up Questions:
--------------------

-  How can we extend ``ToolkitBuilder`` to support custom toolkits or
   tools that are not predefined within the existing toolkit types?
-  How can we improve the error handling mechanism for
   ``ToolkitBuilder`` when the provided arguments are not sufficient for
   creating the required agent tool?
