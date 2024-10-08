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

            if len(beziers) > 0:        
                count = 1
                #saveFile = open(self.filepath + ".csv", "w")
                #saveFile.write("name,px,py,pz,hlx,hly,hlz,hrx,hry,hrz\n");
                #str = '%d,%f,%f,%f,%f,%f,%f,%f,%f,%f\n'
                saveFile = open(self.filepath + ".tres", "w")
                saveFile.write("[gd_resource type=\"Curve3D\" format=3]\n\n[resource]\n_data = {\n\"points\": PackedVector3Array(")
                string = '%f,%f,%f,%f,%f,%f,%f,%f,%f' # renamed from "str" as it is fucking up the "convert to string" function.

                for bezier in beziers:
                    for point in bezier.bezier_points:
                        if count != 1: saveFile.write(","); # Add comma if not the first line so points concatenate
                        line = string % (point.handle_left.x, -point.handle_left.y, point.handle_left.z, point.handle_right.x, -point.handle_right.y, point.handle_right.z, point.co.x, -point.co.y, point.co.z )
                        saveFile.write(line)
                        count = count + 1
                # Loop complete, now add remaining remaining items
                saveFile.write("),\n\"tilts\": PackedFloat32Array(")
                # Loop for tilts here, one per point/count
                tilt = 1
                while tilt <= count:
                    saveFile.write("0")
                    if tilt != count: saveFile.write(", ") # add seperator, unless its the final entry.
                    tilt = tilt + 1

                saveFile.write(")\n}\npoint_count = " + str(count))
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
