# Serialization

This quick guide shows how to serialize full indicator's state including the input and output values and how to restore it later on. This can come handy e.g. if indicator calculated non-trivial number of items and we do not want to calculate them again next time.

The solution is based on [jsonpickle](https://pypi.org/project/jsonpickle) library which can encode/decode objects into string form.

```python
import jsonpickle
from talipp.indicators import BB

bb = BB(5, 1, list(range(0, 100, 2)))
bb_serialized = jsonpickle.encode(bb, unpicklable = True)

# write bb_serialized e.g. to a file...

bb_deserialized = jsonpickle.decode(bb_serialized)

# use the deserialized indicator as usual
bb_deserialized.add(5)
```
