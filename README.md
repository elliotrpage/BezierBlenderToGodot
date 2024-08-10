# BezierBlenderToGodot
Export a Bezier curve from Blender to Godot Curve3D.

## TODO:
* Confirm python script is working for CSV **YEP**
* Remove UE4 files (Spline stuff)
* Update Python script to spit out a Compliant TRES file instead of a CSV
  * https://docs.godotengine.org/en/stable/classes/class_curve3d.html
  * Working on this, crashed Blender oops!!
  * It created a 1.6GB TRES file??? Okay its nothing but "0, " over and over again, I have a fuckup in my logic. I forgot to increment "tilt" oooops
  * Okay, attempt 5 seems to have worked, file looks to be properly generated.
  * lets try importing to Godot!
* ~~Keep the CSV option, maybe?~~ (nah)


# Original README:
Export Bezier curve from Blender to Unreal Engine 4.

The article is available [here](https://medium.com/@qerrant/export-spline-from-blender-to-unreal-engine-28a4ccdd97c0). 

## List
* **ExportBezierToUE.py** - Blender add-on
* **Spline** - Unreal Engine project
  * **BlueprintVersion** - Blueprint solution
  * **SplinePathComponent** and **PathActor** - Component solution
* **TestSpline.csv** - Test file

## Guide
1. Install add-on in Blender:
  Edit -> Preferences... -> Add-ons -> Install (ExportBezierToUE.py)
2. Export Bezier curve points into CSV:
  Select object and File -> Export -> Export BezierCSV for UE4
3. Import CSV such as DataTable in Unreal Engine
4. Select DataTable in SplineActor
