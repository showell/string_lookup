This repo contains code in Python and JS (more or less the same
code in each) that builds a "smart" index on a list of names to
handle prefix searches.

Basically all the code does is create a dictionary of letter ->
index, where each index is recursively either:

- another smart index (w/dictionary of letter -> index)
- a leaf index, which is basically start, end, and offset

I didn't try to conserve memory, but almost all the overhead
is integers and pointers.  (I don't ever create new strings).

## Test data

I got just under 5k names from here:

https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.txt

see my [names.txt](names.txt)

## Results

For whatever reason, Python is slower than JS (node.js) in general
on my box.  Although both languages are pretty fast per search
on a smart index.

Python:

~~~
$ python test_index.py
build naive index
time to build (microseconds): 27.600000000002623

TEST:
# of vals 4945
# of tests 1122
avg cost (microseconds) 1782.4422459893049


build smart index
time to build (microseconds): 5902.300000000693

TEST:
# of vals 4945
# of tests 1122
avg cost (microseconds) 17.006773618538155
~~~

JS:

~~~
$ node test_index.js
build naive 465.101
Testing...
num tests 2983
time per row 58.45873281930942
build smart 500.001
Testing...
num tests 2983
time per row 9.601911163258464

