from confusing_isinstance.example import is_example_class as is_example_absolute
from confusing_isinstance.example import ExampleClass as AbsoluteClass
from example import ExampleClass as RelativeClass
from example import is_example_class as is_example_relative

if __name__ == "__main__":
	a = AbsoluteClass()
	print(f"Created {a}...")
	is_example_relative(a)
	is_example_absolute(a)

	r = RelativeClass()
	print(f"Created {r}...")
	is_example_relative(r)
	is_example_absolute(r)