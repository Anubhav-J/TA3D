Turle Art 3D Prototype
======================

How to run
----------

### Interactive mode

To run the code in interactive mode, simply run the executable ta3d.py
as `python ta3d.py`

### Running a script

To run a script please do the following:
+ `cat examples/helix.3dlogo | ./ta3d.py`
OR
+ `./ta3d.py < examples/circle.3dlogo`

List of Supported Commands
--------------------------

1. `fd <value>` ; Move `<value>` distance forward
1. `rx <value>` ; Rotate the turtle `<value>` degrees about it's x axis.
1. `ry <value>` ; Rotate the turtle `<value>` degrees about it's y ayis.
1. `rz <value>` ; Rotate the turtle `<value>` degrees about it's z azis.
1. `setxyz <xvalue> <yvalue> <zvalue>` ; Set the turtle's co-ordiantes.
1. `pen <value>` ; Change pen state, possible values are 'u' or 'd'.
1. `reset` ; resets the orientation vector to `1i + 0j + 0k`.
1. `repeat <value>` ; starts a repeat block and repeats
    the command preceeeding it `<value>` number of times
1. `end` ; marks the end of a repeat block.
1. `x` ; exit the interactive turtle shell.

Examples
--------

Please find the example files/scripts under the `examples/` subdirectory.


Caveats
-------

+ Script support is a ad-hoc at the moment
+ running a script displays the result for 5 minutes and closes afterwards
+ Nested block statements are not supported at the moment
