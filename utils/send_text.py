
import bpy

def send_text(context,sel):

    override=None
    
    
    for area in bpy.context.screen.areas:
        if area.type=="CONSOLE":
            override = {'area': area, 'region': area.regions} #override context

    # Exit if there is no console screen
    if override==None:
        return {'FINISHED'}
    
    bpy.ops.console.clear_line(override)
    bpy.ops.console.insert(override,text=sel)
    bpy.ops.console.execute(override)
