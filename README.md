# net-finder
Python scripts to search for common nets of boxes

### Running

Set the constants at the top of `dimensions.py`. The first box will have dimensions `LENGTH * HEIGHT * DEPTH` and candidate nets will be generated from this one. `target_boxes` has tuples containing the dimensions of the other boxes you want the nets to match. Each candidate net will be checked against all of these boxes.

To start the script run

```python
python find_nets.py
```

It will continue until it finds a net that is common to every box. Partial matches, i.e. nets common to more than one but not all of the boxes will be written to `results.txt`.
