1. Integrating location information onto the Bounding Box could prove
   beneficial in certain use-cases, such as running a specific check in
   a particular portion of the AST or highlighting an error. Instead of
   looking up the location details separately, these could then be
   directly retrieved from the BoundingBox instance.

2. Bounding box intersection or overlap could be implemented by
   extending this class or by creating a new utility class. The most
   suitable approach would depend on the project’s design philosophy. If
   there’s a need for making ``BoundingBox`` instances ‘aware’ of each
   other and capable of making intersection or overlap checks, then
   extending this class would make sense. Conversely, if this added
   functionality does not conceptually belong to the idea of a
   ‘BoundingBox’, a utility class that takes two bounding boxes and
   checks for intersection or overlap would be appropriate.

3. A ``BoundingBox`` is conventionally a rectangle, derived from the
   ‘minimum bounding rectangle’ concept in spatial analysis where it
   represents the smallest rectangle (oriented along the axes) within
   which all points lie. However, depending on the higher-level
   abstraction, a “bounding box” might not always be rectangular, but
   that could complicate the computation of overlap, intersection, etc.
   and would likely involve the creation of a significantly more complex
   class or set of classes to handle these cases.
