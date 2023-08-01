-  The exact behavioural difference between ``DYNAMIC`` and ``STATIC``
   graph types is not stated explicitly in the current context. However,
   typically, a ``DYNAMIC`` graph is expected to reflect real-time
   changes in the symbols and their relations, while a ``STATIC`` graph
   remains constant over the execution period once built.

-  Applications or functions specifically might require one type over
   the other depending on the usage context. If the application involves
   real-time data monitoring or updating symbol relationships as the
   program runs (like code documentation generation in an IDE or live
   code analyzing), a ``DYNAMIC`` graph may be requested. On the other
   hand, for applications that only require a one-time analysis or
   structure extraction (like static code analyzing tools), a ``STATIC``
   graph would suffice.

-  The ability to switch between ``DYNAMIC`` and ``STATIC`` types for a
   single ``SymbolGraph`` instance in runtime generally lies in the
   functional specification and design of the ``SymbolGraph`` object
   itself. However, there’s no mention of such a feature in the provided
   context. The flexibility to switch between ``DYNAMIC`` and ``STATIC``
   types would need to be incorporated at design time and could involve
   creating separate ``SymbolGraph`` objects or updating the graph’s
   properties. It’s important to consider that switching from STATIC to
   DYNAMIC could possibly demand additional resources for constant
   updates, while switching from DYNAMIC to STATIC may imply that the
   program is no longer interested in subsequent modifications.
