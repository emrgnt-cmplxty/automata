1. ``Node`` provides a template that all derived classes must adhere to.
   By defining required attributes and methods in the ``Node`` abstract
   base class, it ensures any derived classes will have the necessary
   functionality to be used as a node in the file tree. However,
   concrete methods in the derived classes can be varied as per the
   unique requirement of these classes, provided they do not violate the
   structure outlined by ``Node``.

2. The parent-child relationship between nodes is typically maintained
   through references. Each ``Node`` has a ``parent`` attribute which
   holds a reference to its parent node. When a ``Node`` is created, it
   is assigned a ``parent``, and it may also add itself to the parent’s
   list of children (if such functionality is implemented in the child
   class). This creates a two-way link between the parent and child
   nodes. When a ``Node`` is deleted, these links are typically also
   removed to ensure the integrity of the tree.

   However, as the ``Node`` class is an abstract base class, it does not
   directly handle these relationships - this would be the
   responsibility of the concrete classes that inherit from ``Node``,
   such as ``Directory`` or ``File``.
