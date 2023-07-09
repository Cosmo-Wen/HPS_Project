# HPS 2023 Team 10 Style Guide

## 1. Relevant Settintg

### 1.1. Vim Setup

Install vim by doing:

```bash
sudo apt-get install vim
```

Apply the recommended setting from Google by:

1. Acqure the `google_python_style.vim` file from:
   https://google.github.io/styleguide/pyguide.html#s1-background.
2. Navigate to `.vim` directory. Create one if it doesn't exist.
3. Move the `google_python_style.vim` file to the `indent` directory under the current directory. Create one if it doesn't exist.

### 1.2. VSCode SSH setup

The following guide takes you through the steps: \
https://code.visualstudio.com/docs/remote/ssh

## 2. Python Linter

Pylint should already come with the OS from the imager. Use `pip install pylint` if it is not available. \
Acquire the pylintrc file from https://google.github.io/styleguide/pyguide.html#21-lint. To use this configuration file:

- Move it to `/etc/pylintrc` for default global configuration
- Move it to `~/.pylintrc` for default user configuration
- Move it to `'project'/pylintrc` for default project configuration (used when you'll run `pylint 'project'`)
- Use `pylint --rcfile='file_path'` if you want to specify a path

## 3. Language Rules

### 3.1. Imports

- Modules and packages: `import x`
- Modules (y) from packages (x): `from x import y`
- Only change module name when conflict: `from x import y as z`
- For standard abbreviations: `import numpy as np`
- Use full path names for packages: `import absl.flags` or `from doctor.who import jodie`
-

### 3.2. Exceptions

- Use built-in exception classes, e.g. `ValueError`, `ConnectionError`, etc.
- Use assert to ensure internal correctness.
- Use raise to ensure external (arguement) correctness.

### 3.3. Mutable Global State

Avoid mutable global state. For example:

```Python
### This should be avoided unless absolutely necessary.
count = 0

def counter_inc():
    global count
    count += 1

count_inc
print(count) # counter is now 1
```

### 3.4. Comprehensions and Generators

Allowed for simple cases:

- One line per portion, for example:
  ```Python
  descriptive_name = [
    transform({'key': key, 'value': value}, color='black')
    for key, value in generate_iterable(some_input)
    if complicated_condition_is_met(key, value)
  ]
  ```
- Limited to one `for` clause

### 3.5. Default Iterators

Use default iterators over iterating over containers.

```Python
for key in adict:           # Yes
for key in adict.keys():    # No
```

### 3.6. Lambda Functions

Allowed for one-liners.\
If function exists in the `operator` module, use it over defining a new one.

### 3.7. Conditional Expressions/Ternary Operators

Allowed for simple cases.\
 Limited to one line per portion, for example:

```Python
the_longest_ternary_style_that_can_be_done = (
    'yes, true, affirmative, confirmed, correct'
    if predicate(value)
    else 'no, false, negative, nay')
```

### 3.8. Default Argument Values

Allowed if arguments are immutable.

### 3.9 True/False Evaluations

- Use the “implicit” false if possible, e.g., if foo: rather than if foo != []:.
- To check for `None` use `if foo is (not) None:`
- To compare `False`, use `if not foo`
- Empty sequences are `False`. Use `if (not) seq` for sequences.
- Use the integer 0 when handling integers
- Note that `'0'` (i.e., 0 as string) evaluates to true.
- Use .size for Numpy Arrays (e.g. if not users.size).

### 3.10. Type Annotated Code

Type annotations (or “type hints”) are highly encouraged, for example:

```Python
def func(a: int) -> list[int]:
```

Note that type-hinting doesn't prohibit the execution even if the types are incorrect.

## 4. Style Rules

### 4.1. Semicolonos

Not allowed.

### 4.2. Line Length

80 characters. \
Exceptions:

- Long imports
- URLs
- Long strings that might require search function accessability.

Do not use backslashes `\` to continue a line. Break inside parantheses at the highest syntatic level, for example:

```Python
bridgekeeper.answer(
    name="Arthur", quest=questlib.find(owner="Arthur", perilous=True))

# Continued lines are aligned at the starting paranthesis.
answer = (a_long_line().of_chained_methods()
          .that_eventually_provides().an_answer())

if (
    config is None
    or 'editor.language' not in config
    or config['editor.language'].use_spaces is False
):
    use_tabs()

# Join strings with an extra pair of paranthesis.
x = ('This will build a very long long '
     'long long long long long long string')
```

### 4.3. Paranthesis

Minimum, tuples are fine.

### 4.4. Indentation

4 spaces.

### 4.5. Comments and Docstrings

A docstring should be organized as a summary line (one physical line not exceeding 80 characters) terminated by a period, question mark, or exclamation point. When writing more (encouraged), this must be followed by a blank line, followed by the rest of the docstring starting at the same cursor position as the first quote of the first line. There are more formatting guidelines for docstrings below.

1.  Modules: \
    Files should start with a docstring describing the contents and usage of the module.

    ```Python
    """A one-line summary of the module or program, terminated by a period.

    Leave one blank line.  The rest of this docstring should contain an
    overall description of the module or program.  Optionally, it may also
    contain a brief description of exported classes and functions and/or usage
    examples.

    Typical usage example:
        foo = ClassFoo()
        bar = foo.FunctionBar()
    """
    ```

2.  Functions and Methods \
    A docstring is mandatory for every function that has one or more of the following properties:

    - being part of the public API
    - nontrivial size
    - non-obvious logic

    Certain aspects of a function should be documented in special sections, listed below. Each section begins with a heading line, which ends with a colon. All sections other than the heading should maintain a hanging indent of two or four spaces (be consistent within a file). These sections can be omitted in cases where the function’s name and signature are informative enough that it can be aptly described using a one-line docstring.

    Args:\
    List each parameter by name. A description should follow the name, and be separated by a colon followed by either a space or newline. If the description is too long to fit on a single 80-character line, use a hanging indent of 2 or 4 spaces more than the parameter name (be consistent with the rest of the docstrings in the file). The description should include required type(s) if the code does not contain a corresponding type annotation. \

    Returns: (or Yields: for generators) \
    Describe the semantics of the return value, including any type information that the type annotation does not provide. If the function only returns None, this section is not required. It may also be omitted if the docstring starts with Returns or Yields (e.g. """Returns row from Bigtable as a tuple of strings.""") and the opening sentence is sufficient to describe the return value. \

    Raises: \
    List all exceptions that are relevant to the interface followed by a description. Use a similar exception name + colon + space or newline and hanging indent style as described in Args:.

    Example:

    ```Python
    def fetch_smalltable_rows(
        table_handle: smalltable.Table,
        keys: Sequence[bytes | str],
        require_all_keys: bool = False,
    ) -> Mapping[bytes, tuple[str, ...]]:
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.
            keys: A sequence of strings representing the key of each table
            row to fetch.  String keys will be UTF-8 encoded.
            require_all_keys: If True only rows with values set for all keys will be
            returned.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

            {b'Serak': ('Rigel VII', 'Preparer'),
            b'Zim': ('Irk', 'Invader'),
            b'Lrrr': ('Omicron Persei 8', 'Emperor')}

            Returned keys are always bytes.  If a key from the keys argument is
            missing from the dictionary, then that row was not found in the
            table (and require_all_keys must have been False).

        Raises:
            IOError: An error occurred accessing the smalltable.
        """
    ```

3.  Classes \
    Classes should have a docstring below the class definition describing the class. If your class has public attributes, they should be documented here in an Attributes section and follow the same formatting as a function’s Args section.

    Example:

    ```Python
    class SampleClass:
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam: bool = False):
        """Initializes the instance based on spam preference.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""
    ```

4.  Block and Inline Comments
    The final place to have comments is in tricky parts of the code.

    To improve legibility, these comments should start at least 2 spaces away from the code with the comment character #, followed by at least one space before the text of the comment itself.

    On the other hand, never describe the code. Assume the person reading the code knows Python (though not what you’re trying to do) better than you do.

5.  Punctuation, Spelling, and Grammar \
    Pay attention to punctuation, spelling, and grammar; it is easier to read well-written comments than badly written ones.

    Comments should be as readable as narrative text, with proper capitalization and punctuation. In many cases, complete sentences are more readable than sentence fragments. Shorter comments, such as comments at the end of a line of code, can sometimes be less formal, but you should be consistent with your style.

    Although it can be frustrating to have a code reviewer point out that you are using a comma when you should be using a semicolon, it is very important that source code maintain a high level of clarity and readability. Proper punctuation, spelling, and grammar help with that goal.

### 4.6. Strings

Use f-strings. Simple joining with `+` are fine but do not format with it.

### 4.7. Files

Use `with` statements. Use contextlib.closing() if `with` is not supported.

### 4.8. TODO Comments

Use TODO comments for code that is temporary, a short-term solution, or good-enough but not perfect. The TODO is followed by an explanation of what there is to do. \
FMI: https://google.github.io/styleguide/pyguide.html#312-todo-comments

### 4.9. Imports formatting

Imports should be on separate lines, with the order of:

1. Python future import statement
   Python future import statements. For example:

```Python
from __future__ import annotations
```

2. Python standard library imports. For example:

```Python
import sys
```

3. Third-party module or package imports. For example:

```Python
import tensorflow as tf
```

4. Code repository sub-package imports. For example:

```Python
from otherproject.ai import mind
```

Within each grouping, imports should be sorted lexicographically, ignoring case, according to each module’s full package path (the path in from path import ...). Code may optionally place a blank line between import sections. \
For example:

```Python
import collections
import queue
import sys

from absl import app
from absl import flags
import bs4
import cryptography
import tensorflow as tf

from book.genres import scifi
from myproject.backend import huxley
from myproject.backend.hgwells import time_machine
from myproject.backend.state_machine import main_loop
from otherproject.ai import body
from otherproject.ai import mind
from otherproject.ai import soul
```

### 4.10. Statements

One statement per line unless a short `if` with no `else`.

### 4.11. Naming

| Type                       | Public               | Internal                          |
| -------------------------- | -------------------- | --------------------------------- |
| Packages                   | `lower_with_under`   |                                   |
| Modules                    | `lower_with_under`   | `_lower_with_under`               |
| Classes                    | `CapWords`           | `_CapWords`                       |
| Exceptions                 | `CapWords`           |                                   |
| Functions                  | `lower_with_under()` | `_lower_with_under()`             |
| Global/Class Constants     | `CAPS_WITH_UNDER`    | `_CAPS_WITH_UNDER`                |
| Global/Class Variables     | `lower_with_under`   | `_lower_with_under`               |
| Instance Variables         | `lower_with_under`   | `_lower_with_under` (protected)   |
| Method Names               | `lower_with_under()` | `_lower_with_under()` (protected) |
| Function/Method Parameters | `lower_with_under`   |                                   |
| Local Variables            | `lower_with_under`   |                                   |

Extra Rules:

- Namings should be descriptive; avoid abbreviations.
- Always use a .py filename extension.
- Never use dashes.
- Avoid single character names except:
  - counters or iterators (e.g. i, j, k, v, et al.)
  - e as an exception identifier in try/except statements.
  - f as a file handle in with statements
  - private type variables with no constraints (e.g. \_T = TypeVar("\_T"), \_P = ParamSpec("\_P"))

### 4.12. Main

If a file is meant to be used as an executable, its main functionality should be in a main() function, and your code should always check `if __name__ == '__main__'` before executing your main program, so that it is not executed when the module is imported.
When using `absl`, use `app.run`:

```Python
from absl import app
...

def main(argv: Sequence[str]):
    # process non-flag arguments
    ...

if __name__ == '__main__':
    app.run(main)
```

Otherwise, use:

```Python
def main():
    ...

if __name__ == '__main__':
    main()
```

### 4.13. Function Lengths

Prefer small and focused functions. If a function exceeds about 40 lines, think about whether it can be broken up without harming the structure of the program.

## 5. Conclusion

**BE CONSISTENT.**

If you’re editing code, take a few minutes to look at the code around you and determine its style. If they use \_idx suffixes in index variable names, you should too. If their comments have little boxes of hash marks around them, make your comments have little boxes of hash marks around them too.

The point of having style guidelines is to have a common vocabulary of coding so people can concentrate on what you’re saying rather than on how you’re saying it. We present global style rules here so people know the vocabulary, but local style is also important. If code you add to a file looks drastically different from the existing code around it, it throws readers out of their rhythm when they go to read it.

However, there are limits to consistency. It applies more heavily locally and on choices unspecified by the global style. Consistency should not generally be used as a justification to do things in an old style without considering the benefits of the new style, or the tendency of the codebase to converge on newer styles over time.
