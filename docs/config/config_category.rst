-  To add a new category in ``ConfigCategory``, you simply define a new
   attribute in the ``ConfigCategory`` Enum class and assign it a unique
   value. Following is an example of how to do this:

::

   from enum import Enum

   class ConfigCategory(Enum):
       AGENT = 1
       PROMPT = 2
       SYMBOL = 3
       INSTRUCTION = 4
       NEWCATEGORY = 5  # new category

-  As for the situation where there is a need for a sub-category,
   ``ConfigCategory`` does not directly support sub-categories. If there
   is a need for this, it may be an indicator that your code needs to be
   restructured instead. However, you could potentially implement this
   by storing another Enum as the value of a category. This might look
   like this:

::

   from enum import Enum

   class Subcategory(Enum):
       SUBCATEGORY1 = 1
       SUBCATEGORY2 = 2

   class ConfigCategory(Enum):
       AGENT = 1
       PROMPT = 2
       SYMBOL = 3
       INSTRUCTION = 4
       NEWCATEGORY = Subcategory  # new category with sub-categories

Keep in mind though that this would be somewhat unconventional and might
make the code harder to understand. It would be better to consider other
ways to structure your code if sub-categories are necessary.
