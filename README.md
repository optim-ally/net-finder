# net-finder

Python scripts to search for common nets of boxes

### Running

There are two approaches available: exhaustive search and random search.

Both programs take one or more boxes as an input and use the first box to generate candidate nets. These nets are then checked against all other boxes (if any are provided) to find nets that are common to all of them.

Both programs send their results to stdout and append them to `results.txt`.

#### Exhaustive Search

This is designed to systematically check every possible common net of the given box or boxes and find all matches. It should only be used for small boxes since search spaces are usually too large.

```
python find_all.py [-b | --box] <length> <height> <depth> ...
```

The "box" argument can be supplied multiple times to provide the dimensions of more boxes.

Only distinct nets are returned, meaning reflections and rotations of the same net are not included.

#### Random Search

Better for most cases. This will instead search semi-randomly in the space of possible common nets until it finds just one the matches every box, then it terminates. The program uses several tricks to _hopefully_ produce a single solution faster than exhaustive search. It may run indefinitely and will never produce a solution for certain inputs.

```
python find_one.py [-b | --box] <length> <height> <depth> ...
```

It scores candidate nets by the sum of their distances to each target box, where "distance" is defined as the minimum number of unit squares on the box not covered by the net. Scoring a net is an expensive operation as all positions and orientations of the net must be tried to find the best one, but doing this helps identify promising areas of the search space.

As the program runs, it outputs each new best-scoring net it finds.

#### Examples

Find all nets of a unit cube (there are 11):

```
python find_all.py --box 1 1 1
```

or

```
python find_all.py -b 1 1 1
```

The following program gives the same result but adds needless checks:

```
python find_all.py --box 1 1 1 --box 1 1 1
```

Find all nets of a `2 x 1 x 1` cuboid (there are 723):

```
python find_all.py --box 2 1 1
```

Find all common nets of `5 x 1 x 1` and `1 x 2 x 3` cuboids (there are 2263, but the set of candidates to check is much larger):

```
python find_all.py --box 5 1 1 --box 1 2 3
```

Find all common nets of `1 x 1 x 11`, `1 x 2 x 7` and `1 x 3 x 5` cuboids (this may take years to run):

```
python find_all.py --box 1 1 11 --box 1 2 7 --box 1 3 5
```

Search for any common net of `1 x 1 x 11`, `1 x 2 x 7` and `1 x 3 x 5` cuboids (it is not known whether a solution exists):

```
python find_one.py --box 1 1 11 --box 1 2 7 --box 1 3 5
```
