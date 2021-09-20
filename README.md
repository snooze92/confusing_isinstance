# Confusing `isinstance`

## Goal

This repository helps reproduce a confusing issue we had with Python's `isinstance` and import system.

As it turns out, Python is behaving exactly as expected; there still are a few interesting conclusions to notice! ;)

## Reproduce

Checking out the repository and running `PYTHONPATH="${PYTHONPATH}:$(pwd)" python confusing_isinstance` gives this output:

> ```
> Created <confusing_isinstance.example.ExampleClass object at 0x7ffb98353e90>...
> ... is not instance of <class 'example.ExampleClass'>
> ... is instance of <class 'confusing_isinstance.example.ExampleClass'>
> Created <example.ExampleClass object at 0x7ffb8801c350>...
> ... is instance of <class 'example.ExampleClass'>
> ... is not instance of <class 'confusing_isinstance.example.ExampleClass'>
> ```

## Conclusions

### What happens

The module is imported twice under two names.
We have two copies of the module and instances of one copy of the class are not instances of the other copy of the class.

The easiest way is to see the difference between the two imports of the same class is to compare `AbsoluteClass.__module__` and `RelativeClass.__module__`.
We find `confusing_isinstance.example` and `example` respectively.

We can also see that both modules with different names exist in `sys.modules`, from the same file:
```
{
  'sys': <module 'sys' (built-in)>,
  ...
  'confusing_isinstance.example': <module 'confusing_isinstance.example' from '/Users/jlehuen/Code/school-august-2021/confusing_isinstance/confusing_isinstance/example.py'>,
  'example': <module 'example' from '/Users/jlehuen/Code/school-august-2021/confusing_isinstance/confusing_isinstance/example.py'>
}
```

### What is recommended

The best description of the problem I've found online is [Nick Coghlan's _double import trap_](http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html#the-double-import-trap).

That gives the general guideline _“Never add a package directory, or any directory inside a package, directly to the Python path”_.

And indeed, if I don't set the Python path, absolute imports stop working:
```
$ python confusing_isinstance
Traceback (most recent call last):
  File "/usr/local/Caskroom/miniconda/base/lib/python3.7/runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "/usr/local/Caskroom/miniconda/base/lib/python3.7/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "confusing_isinstance/__main__.py", line 1, in <module>
    from confusing_isinstance.example import is_example_class as is_example_absolute
ModuleNotFoundError: No module named 'confusing_isinstance'
```

Or if I try to run as a module, relative imports stop working (whether I set Python path or not):
```
$ python -m confusing_isinstance.main
Traceback (most recent call last):
  File "/usr/local/Caskroom/miniconda/base/lib/python3.7/runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "/usr/local/Caskroom/miniconda/base/lib/python3.7/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/Users/jlehuen/Code/school-august-2021/confusing_isinstance/confusing_isinstance/__main__.py", line 3, in <module>
    from example import ExampleClass as RelativeClass
ModuleNotFoundError: No module named 'example'
```

Based on all of this, I think the best approach is to **prefer running with `python -m` and use absolute imports consistently**.

Note that JetBrains' PyCharm will sometimes run a file directly and set `PYTHONPATH`, which could hide such issues.

## Links

- [Similar question on SO](https://stackoverflow.com/questions/46708659/isinstance-fails-for-a-type-imported-via-package-and-from-the-same-module-direct), that mentions:
  - [Import system documentation](https://docs.python.org/3/reference/import.html);
  - [Nick Coghlan's _double import trap_](http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html#the-double-import-trap);
- [Another related SO question](https://stackoverflow.com/questions/9006740/isinstance-and-type-equivelence-failure-due-to-import-mechanism-python-djan);
- [One last SO question](https://stackoverflow.com/questions/53658252/why-do-circular-imports-cause-problems-with-object-identity-using-isinstance), this is a slightly different issue coming from the `__main__` module name when running a file...
