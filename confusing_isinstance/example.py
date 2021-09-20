class ExampleClass:
    pass

def is_example_class(o):
	result = isinstance(o, ExampleClass)
	print(f"... {'is' if result else 'is not'} instance of {ExampleClass}")
	return result
