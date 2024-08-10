# Dissecting Curve3d.md 

Okay, lets dissect the file format. There is also a screenshot from the Godot editor to help with this.

## Front matter
-----
[gd_resource type="Curve3D" format=3 uid="uid://dt3v76vo6wwjt"]

[resource]
_data = {
-----

format=3 comes from godot 4.2
format=2 was seen in godot 3.6
**For now, lets worry about 4.2**

uid optional? created by the Godot engine itself, I believe. Leave out for now.

## Data Points
-----
"points": PackedVector3Array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.25, 0.5, 0.75, 1, 1, 1, 0, 0, 0, 1, 1, 1),
-----
This is the actual meat of things.
Each Vector is a set of 9 values. Vectors are not seperated into individual points - they are concatenated into a single list. Lets look at a single data point, the "middle" one in this example.

### Single Data Point
-----
0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.25, 0.5, 0.75,
-----
So, cross referencing with the in-engine example, these values break down like so:
`in-x, in-y, in-z, out-x, out-y, out-z, pos-x, pos-y, pos-z`
This is personally surprising as I was expecting them to put position first, but hey. 

Note that for the first/last nodes which do not have an "in" or "out" value this is set to blanket zeros. (0)

To compare to the UE4 script I am basing on, this uses "px,py,pz,hlx,hly,hlz,hrx,hry,hrz"
hl = left (in), hr = right (out)


## Tilts
-----
"tilts": PackedFloat32Array(0, 0, 0)
-----
This relates to the rotation of PathFollow3D objects "on" the path.
For now, lets leave all at 0.


## Point count
-----
point_count = 3
-----

Integer count of the number of points in the Curve. Could be optional or have a checksum purpose but lets not leave it out!