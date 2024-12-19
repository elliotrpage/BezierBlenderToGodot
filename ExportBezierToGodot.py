# Blender Plugin
# Later on, switch from CSV to a TRES File
bl_info = {
    "name": "Export BezierCSV for Godot",
    "blender": (2, 80, 0),
    "author": "Elliot Page, Alex Z.",
    "location": "File > Export > BezierCSV For Godot (.tres)",
    "category": "Import-Export",
}

import sys, getopt
import os
import bpy
from bpy_extras.io_utils import ImportHelper


class ObjectExportPoints(bpy.types.Operator, ImportHelper):
    bl_idname = "me.export_bezier_points" 
    bl_label = "Export BezierCSV to Godot"   
    bl_options = {'REGISTER'} 
    
    def execute(self, context):
        obj = bpy.context.active_object
        objType = bpy.context.object.type
        
        if objType == 'CURVE':
            beziers = []
                        
            for subcurve in obj.data.splines:
                if subcurve.type == 'BEZIER':
                    beziers.append(subcurve)

            #DEBUG
            print(beziers)

            # Actual loop
            if len(beziers) > 0:        
                count = 1
                saveFile = open(self.filepath + ".tres", "w")
                saveFile.write("[gd_resource type=\"Curve3D\" format=3]\n\n[resource]\n_data = {\n\"points\": PackedVector3Array(") # Writes front matter and opens the array
                string = '%f,%f,%f,%f,%f,%f,%f,%f,%f' # Each point on the curve is a series of 9 floats

                for bezier in beziers:
                    pointtotal = len(bezier.bezier_points) # how many points are there in the curve? We will need this later.
                    for point in bezier.bezier_points:
                        if count != 1: saveFile.write(", "); # Add a comma if not the first point so the list is concatenated properly.
                        # If this is the first point in the curve, the "in" vector must be zeroed out.
                        if count == 1: 
                            line = string % (0.0, 0.0, 0.0, point.handle_right.x, -point.handle_right.y, point.handle_right.z, point.co.x, -point.co.y, point.co.z)
                        # If this is the last point in the curve, the "out" vector must be zeroed out
                        elif count == pointtotal:
                            line = string % (point.handle_left.x, -point.handle_left.y, point.handle_left.z, 0.0, 0.0, 0.0, point.co.x, -point.co.y, point.co.z)
                        # All the rest are "Main sequence" points, with both "In" and "Out" vectors
                        else:
                            line = string % (point.handle_left.x, -point.handle_left.y, point.handle_left.z, point.handle_right.x, -point.handle_right.y, point.handle_right.z, point.co.x, -point.co.y, point.co.z)
                        # write the point to the list
                        saveFile.write(line)
                        count = count + 1 
                # Loop complete, now add remaining remaining items
                saveFile.write("),\n\"tilts\": PackedFloat32Array(")
                # Loop for tilts here, one per point/count
                tilt = 1
                while tilt <= pointtotal: # This initially used "count" which was 1 point too many.
                    saveFile.write("0")
                    if tilt != pointtotal: saveFile.write(", ") # add seperator, unless its the final entry.
                    tilt = tilt + 1

                saveFile.write(")\n}\npoint_count = " + str(pointtotal)) # This initially used "count" which was 1 point too many.
                # Generation complete, close file
                saveFile.close()
                self.report({"INFO"}, "The curve was exported")
                return {'FINISHED'}
            else:
                self.report({"WARNING"}, "Selected object isn't a Bezier curve")
                return {'CANCELLED'}                
                
        else:
            self.report({"WARNING"}, "Selected object isn't a curve")
            return {'CANCELLED'}

def menu_func(self, context):
    self.layout.operator(ObjectExportPoints.bl_idname,text="Export BezierCSV For Godot (.tres)")

def register():
    bpy.utils.register_class(ObjectExportPoints)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ObjectExportPoints)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
