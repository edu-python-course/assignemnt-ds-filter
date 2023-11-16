# Solution

## Objective decomposition

> Your task is to create a function, that performs a dataset filtering by
> unique values. Only values in a given set of keys should be applied for
> filtering.
> The `DataSet` is the only required argument, if case there is no `Keys` to
> filter provided - all available keys will be used.

### Handling empty `dataset`

If an empty dataset is passed to the function call - an empty list should be
returned. Empty sequences are considered `False`.

```python
def filter_by_values(dataset, keys):
    if not dataset:
        return []
```

### Handling `no keys` case

There are two scenarios require implementation:

- `keys` has not been passed to the function call
- empty `keys` list has been passed to the function call

According to [instructions document](./instructions.md) `keys` is a list
of `str` instances, which are valid dictionaries' keys. The parameter is
described as an optional parameter, and it defaults to all available keys.
To make it optional the default value should be provided in the function's
definition. An empty list (`[]`) cannot be used as default value, since it
is a mutable data type. The solution is to use `None` as default value.
Both `None` and an empty list are considered `False` values.

```python
def filter_by_values(dataset, keys=None):
    if not dataset:
        return []
    keys = keys or dataset[0].keys()
```

### Obtain values in specified keys

The [instructions document](./instructions.md) says, that all the values of
specified keys are to be checked being unique. No other values should affect
this check. There is a need to get pairs of dictionary keys and values. List
comprehension syntax can be used to collect only the required values, like:

```python
sample = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
keys = ["a", "c", "d"]
values = [value for key, value in sample.items() if key in keys]
```

`dict.items()` method provides a functionality to get `(key, value)` pairs.
If the `key` is listed in **specified keys** its value will be gathered.

### Filtering values

To check unique values there is a need in some container to collect values,
that have been seen already. If the set of values is met for the first time -
add it to the container.

```python
sample = [{"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3}]
keys = ["a", "c"]
filtered_values = []
for entry in sample:
    entry_values = [value for key, value in entry.items() if key in keys]
    if entry_values in filtered_values:
        continue
    filtered_values.append(entry_values)
```

### Filtering dataset

Use the [Filtering values](#filtering-values) logic. If a set of values is met
for the first time, update filtered dataset entries container as well.

```python
sample = [...]
filtered_values = []
filtered_dataset = []
for entry in sample:
    entry_values = ...
    filtered_values.append(entry_values)
    filtered_dataset.append(entry)
```

### Return filtered dataset

Simply return filtered dataset.

## Code optimization

### Obtain values

`dict.get` method can be used to gather the value in the requested key. While
`keys` is an iterable object, it may be used alongside with `DataEntry` within
a `map` function.

```python
sample = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
keys = ["a", "c", "d"]
values_map = map(sample.get, keys)
```

This will create a generator to gather values in the future.

### Filtering objects

[Instruction](./instructions.md) says, that **all** dictionaries' values are of
`Hashable` type. This means, that the **hash** value can be calculated for each
of these values.

```python
sample = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
keys = ["a", "c", "d"]
values_map = map(sample.get, keys)
values_hash = hash(tuple(values_map))
```

Converting to a `tuple` required to initialize map and actually obtain the
collection the dictionary's values.

Since built-in `hash` function provides a `Hashable` value as well, it can be
stored inside a `set` instance to increase the performance of unique values
check operation.

```python
sample = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
keys = ["a", "c", "d"]
filtered_values = set()
values_map = map(sample.get, keys)
values_hash = hash(tuple(values_map))
if values_hash in filtered_values:
    ...  # skip, and move to the next one data entry
```

## Solution

```python
from typing import Dict, Hashable, List, Optional, Set

DataEntry = Dict[str, Hashable]
DataSet = List[DataEntry]
Keys = List[str]


def filter_by_values(dataset: DataSet, keys: Optional[Keys] = None) -> DataSet:
    """
    Return a dataset filtered by unique values in a list of given keys
    """

    # check empty dataset base case
    if not dataset:
        return []
    
    # obtain default keys if not provided
    keys = keys or dataset[0].keys()
    
    filtered_dataset: DataSet = []
    filtered_values: Set[int] = set()

    for data_entry in dataset:
        values_map = map(data_entry.get, keys)
        values_hash = hash(tuple(values_map))
        
        if values_hash in filtered_values:
            continue
            
        filtered_values.add(values_hash)
        filtered_dataset.append(data_entry)

    return filtered_dataset
```
