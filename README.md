# net-finder
Python scripts to search for common nets of boxes

### Running

Set the constants at the top of `dimensions.py`. The first box will have dimensions `LENGTH * HEIGHT * DEPTH` and candidate nets will be generated from this one. `target_boxes` has tuples containing the dimensions of the other boxes you want the nets to match. Each candidate net will be checked against all of these boxes.

To start the script run

```python
python find_nets.py
```

It will continue until it finds a net that is common to every box. Partial matches, i.e. nets common to more than one but not all of the boxes will be written to `results.txt`.

The C++ implementation is basically identical (at the time of writing) and was written to check whether it gave significantly faster results. The conclusion was that 
it didn't. This is most likely due to the author's (my) implementation being quite Pythonic and not translating well to efficient C++. Improvements for either language are very welcome.
