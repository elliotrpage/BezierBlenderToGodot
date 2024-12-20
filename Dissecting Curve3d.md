# Dissecting Curve3d.md 

Okay, lets dissect the file format. There is also a screenshot from the Godot editor to help with this.

Dec 2024 note: Returning to this after errors with importing into Godot4.4Dev6. Script appears to be busted! Mismatch in number of points and the points "jumped" all over the place.

Thinking about it, I believe the issue is one where Blender has In and Out values for ALL points. Godot does not "see" or record the "in" data for the first Point, nor the "out" data for the last Point.

## Front matter
-----
[gd_resource type="Curve3D" format=3 uid="uid://dt3v76vo6wwjt"]

[resource]
_data = {
-----

format=3 comes from godot 4.2
format=2 was seen in godot 3.6
**For now, lets worry about 4.2**

uid optional? created by the Godot engine itself, I believe. Can be ignored.

## Data Points
-----
"points": PackedVector3Array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.25, 0.5, 0.75, 1, 1, 1, 0, 0, 0, 1, 1, 1),
-----
This is the actual meat of things.
Each Vector is a set of 9 values. Vectors are not seperated into individual points - they are concatenated into a single list. Let's look at a single data point, the "middle" one in this example.

### Single Data Point
-----
0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.25, 0.5, 0.75,
-----
So, cross referencing with the in-engine example, these values break down like so:
`in-x, in-y, in-z, out-x, out-y, out-z, pos-x, pos-y, pos-z`
This is personally surprising as I was expecting them to put position first, but hey. 

Note that for the first/last nodes which do not have an "in" or "out" value this is set to blanket zeros. (0)   
**Dec 2024 note**: It may be this was forgotten about in my version of the script.

To compare to the UE4 script I am basing on, this uses "px,py,pz,hlx,hly,hlz,hrx,hry,hrz"
hl = left (in), hr = right (out)


## Tilts
-----
"tilts": PackedFloat32Array(0, 0, 0)
-----
This relates to the rotation of PathFollow3D objects "on" the path.
For now, lets leave all at 0.

**TODO**: This needs to be handled later, once the line itself is working.
It looks like the conversion from Mesh to Curve does not retain any tilt/facing data - at least, how I did it. 

## Point count
-----
point_count = 3
-----

Integer count of the number of points in the Curve. Could be optional or have a checksum purpose but lets not leave it out!   
Starts at 1 - it is a count, not an ID ref.


# Testing notes:
Dec 2024 - Okay, the output looks weird, like it is "bouncing" all the time.  
My initial thoyght was that this was due to godot treating axes differently - y is z and vice versa. This is something to bear in mind even if not the case.    

However it appears this is not the issue. Looking at the curve object in Godot I can view the points - looking at Point 2 (1 in a zero-based counting) it appears that some positive / negatives are inverted.

## Blender:
  Position:
    X: -15.886  
    Y: 44.343  
    Z: -0.162
  In:
    X: -8.426 
    Y: 32.003
    Z: 0.256
  Out:
    X: -18.356
    Y: -8.427
    Z: -0.3
  Tilt: 0.0
## Godot: 
  Position:
    X: -15.886  OK
    Y: -44.343  INCORRECT - has inverted
    Z: -0.162   OK
  In:
    X: -8.426   OK
    Y: -32.003  INCORRECT - has inverted
    Z: 0.256    OK
  Out:
    X: -18.356  OK
    Y: -48.427  INCORRECT - has inverted
    Z: -0.3     OK

Okay, so its the Y dimension inverting? Did I skip over something in the script / add a typo?
Looks like it was something present in the original script I did not interrorgate. OOPS.
Now fixed, lets test. (v3 file)

**Now it somehow looks WORSE?**

Okay, it might well be the Z / X swap. Lets do that.
Corrected now, lets test again. (v4 file)
Nope, that just rotated it, as initially expected.

Is it how the different engines handle the in/out values? Is one Global while the other is Differential?
Godot indicates that the in/out values are "relative to the vertex". Aha. 
Okay, lets look at Blender docs: "A Bézier curve can be edited by transforming the **locations** of both control points and handles.
Yep, they are "Global", as exported. Blender has the ability to display as local in the viewport, I would presume this is a derived value and not one kept in the "raw data"? The values are "local" as relates to the origin point of the object itself, not the "world"/scene. regardless, these are still not relative to the location.

Okay looks like I need to adjust the script. 
The in/out values are relative to the location - the delta.
So, **In/out.value - location.value = delta, relative to the location**

Adjusted the script to handle this, v6 file.
IT WORKS
THANK CHRIST
Its rotated, so lets fix that - v7 file
Okay, so its still rotated but for now the shape, handles and order work so am leaving it alone.  Phew.
