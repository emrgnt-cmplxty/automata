1. The ``AutomataTaskRegistry`` is designed to manage tasks, not create
   or delete them. The tasks should be created and potentially deleted
   outside of the registry, and then registered and managed within it.
   However, adding a deletion functionality could be useful if a task is
   no longer needed. Creation could be kept separate to maintain
   separation of responsibilities, but you also could combine the
   functionality if this better suits your use-case.

2. In general, having non-unique ``session_id``\ s is not a good
   practice as it can cause confusion and potential errors down the
   line. However, there might be very specific use cases where this
   could be beneficial. For example, there might be tasks which are
   identical and need to be performed periodically and you would like to
   easily group them together. In this case having the same
   ``session_id`` could be a way to achieve this. Nonetheless, it would
   be more common to have a separate identifier for the group or type of
   task, and keep the ``session_id`` unique.

3. The error handling could definitely be refined as the system gets
   more complex. Rather than just throwing a generic exception, we could
   have custom exceptions that specify the exact reason for the failure,
   like ``TaskAlreadyRegistered``, ``TaskNotInCreatedState``,
   ``NonUniqueSessionID``, etc. Depending on the exact use-case you
   might want to fail loudly or try to recover. In general, it might be
   a good idea to fail loudly during development to notice and fix
   errors early. In a production system, on the other hand, a more
   sophisticated error handling system that attempts recovery while
   alerting the system administrators about the issue might be
   preferable.
