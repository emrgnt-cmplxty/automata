class Singleton(abc.ABCMeta, type): ‘:raw-latex:`\n    `Singleton
metaclass for ensuring only one instance of a class.:raw-latex:`\n    `’
\_instances: Dict[(str, Any)] = {}

::

   def __call__(self, *args, **kwargs):
       'Call method for the singleton metaclass.'
       if (self not in self._instances):
           self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
       return self._instances[self]
