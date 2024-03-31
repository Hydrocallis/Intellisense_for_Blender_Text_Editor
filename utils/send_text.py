
import bpy
def console_get():
    for area in bpy.context.screen.areas:
        if area.type == 'CONSOLE':
            for space in area.spaces:
                if space.type == 'CONSOLE':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            return area, space, region
    return None, None, None



def send_text(context,sel):


    area, space, region = console_get()
    if space is None:
        return

    context_override = bpy.context.copy()
    context_override.update({
        "space": space,
        "area": area,
        "region": region,
    })
    with bpy.context.temp_override(**context_override):
        bpy.ops.console.clear_line()
        bpy.ops.console.insert(text=sel)
        bpy.ops.console.execute()                    

        