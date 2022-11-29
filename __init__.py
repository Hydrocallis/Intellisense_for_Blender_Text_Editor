# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Intellisense",
    "author": "Mackraken, tintwotin, Hydrocallis",
    "version": (0, 3, 3),
    "blender": (3, 3, 1),
    "location": " Text Editor in Scripting tab> Ctrl + Shift + Space, Edit and Context menus,Ctrl + Shift + ENTER, send console",
    "description": "Adds intellisense to the Text Editor",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development",
}

import bpy,pprint

from bpy.types import (
                        Panel,
                        Menu,
                        Operator,
                        PropertyGroup,
                        AddonPreferences,
                        )
from bpy.props import (
                        BoolProperty,
                        StringProperty,
                        IntProperty,
                        )

# The folder location has changed since Blender 3.3, 
# so switch the module folder location when an error occurs

try:
    from console import intellisense

except ModuleNotFoundError:
    from bl_console_utils.autocomplete import intellisense
    
from console_python import get_console


def complete(context):

    sc = context.space_data
    try:
        text = sc.text

        region = context.region
        for area in context.screen.areas:
            if area.type == "CONSOLE":
                region = area.regions[1]
                break

        console = get_console(hash(region))[0]

        line = text.current_line.body
        cursor = text.current_character

        result = intellisense.expand(line, cursor, console.locals)
    except AttributeError:
        result=""

    return result


def make_enumlists(self,context):
    inte_lists=[]
    options = complete(bpy.context)
    options = options[2].split("\n")

    while("" in options) :
        options.remove("")

    att = False

    for op in enumerate(options):
        if op[1].find("attribute")>-1:
            att = True
        if not att:
            op1 = op[1].lstrip()
        # print('###op',op)
        inte_lists.append((op1,op1,"","",op[0]))
        
    return inte_lists
        

def ShowMessageBox(message = "", title = "Sendc Console Message", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


def send_console(context, all=0):
    
    sc = context.space_data
    text = sc.text
    
    console = None
    override = None
    for area in bpy.context.screen.areas:
        if area.type=="CONSOLE":
            override = {'area': area, 'region': area.regions} #override context
            console = get_console(hash(area.regions[1]))[0]
            
    if console==None:
        return {'FINISHED'}
    
    lines = []
    
    if all:
        lines = text.lines
    else:
        lines = [text.current_line]
    
    space = " "
    tab = "	"	
    
    for l in lines:
        line = l.body
        if "=" in line:
            var = line.split("=")
            if not "." in var[0] and var[1]!="":
                # print("push "+line)
                while line[0]==space or line[0]==tab:
                    line = line[1::]
            
                console.push(line)
                
            else:
                # print("not processed")
                text ="not processed"
                ShowMessageBox(text) 

        elif "import" in line:
            console.push(line)

        else:

            # print("not processed")
            text ="not processed"
            ShowMessageBox(text) 


def current_text(context):
    if context.area.type == "TEXT_EDITOR":
        return context.area.spaces.active.text


def text_selection(context):
    txt = current_text(context)
    sel = ""


    if txt:

        sline = txt.current_line
        endline = txt.select_end_line
        endlineincex= txt.select_end_line_index
        # If only one line is selected
        if sline == endline: return txt.lines[endlineincex].body
        print('###1',txt.lines[endlineincex].body)
        rec = 0
        for i, l in enumerate(txt.lines):
            i=i+1
            line = l.body + "\n"
            if l == sline or l==endline:
                if rec == 0:
                    rec = 1
                    sel += line
                    continue
            if rec:
                sel += line
                if l == sline or l==endline:
                    break
    return sel


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


addon_intellisense_keymaps = []


class TEXT_AP_intellisense_AddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Addon Intellisense Keymaps")
        # layout.prop(self, "filepath")
        # layout.prop(self, "number")
        # layout.prop(self, "boolean")
        # print('###', )
        # pprint.pprint(addon_intellisense_keymaps)

    
        import rna_keymap_ui 
        layout = self.layout
        wm = context.window_manager
        kc = wm.keyconfigs.user
        old_km_name = "" 
        old_id_l = [] 
        for km_add, kmi_add in addon_intellisense_keymaps: 
            km = kc.keymaps[km_add.name] 
            # print('###km',km)     

            for kmi_con in km.keymap_items: 
                # print('###kmi_con',kmi_con)  # key map all set     
                if kmi_add.idname == kmi_con.idname:
                    # print('###kmi_add.idname',kmi_add.idname)  # The "keymap name of the corresponding add-on" will be displayed.   

                    if not kmi_con.id in old_id_l:
                        kmi = kmi_con 
                        old_id_l.append(kmi_con.id) 
                        # print('###old_id_l',old_id_l)  # keymaps di number   
                        break 
            try:
                if kmi:
                    if not km.name == old_km_name: 
                        layout.label(text=km.name,icon="DOT") 
                    layout.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)
                    layout.separator()
                    old_km_name = km.name
                    kmi = None
            except UnboundLocalError:
                print('###error',)


class TEXT_PG_intellisense_PropertyGroup(PropertyGroup):

    use_send_console_line_break_bool : BoolProperty(
                name = "use send console line break",
                default = True,
                description="",
                )


class TEXT_OT_intellisense_send_text(Operator):
    #'''Tooltip'''
    bl_idname = "text.intellioptions_search_send_text"
    bl_label = "line send text"

    @classmethod
    def poll(cls, context):
        if len(bpy.data.texts) != 0:
            return True 


    def execute(self, context):

        sel=text_selection(context)
        splitlines=str.splitlines(sel)
        for sel in splitlines:
            send_text(context,sel)
    
        return {'FINISHED'}
        

class TEXT_OT_intellisense_send_console(Operator):
    #'''Tooltip'''
    bl_idname = "text.intellioptions_search_send_console"
    bl_label = "line send console"


    @classmethod
    def poll(cls, context):
        if len(bpy.data.texts) != 0:
            return True 


    def execute(self, context):
    
        send_console(context)
        props = context.scene.intellisense_propertygroup
        if props.use_send_console_line_break_bool == True:
            bpy.ops.text.line_break()

        return {'FINISHED'}

    
class TEXT_OT_intellisense_options(Operator):
    '''Options'''
    bl_idname = "text.intellioptions"
    bl_label = "Intellisense Options"

    text: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        sc = context.space_data
        text = sc.text

        comp = self.text
        line = text.current_line.body

        lline = len(line)
        lcomp = len(comp)

        #intersect text
        intersect = [-1, -1]

        for i in range(lcomp):
            val1 = comp[0:i + 1]

            for j in range(lline):
                val2 = line[lline - j - 1::]
                #print("	",j, val2)

                if val1 == val2:
                    intersect = [i, j]
                    break

        comp = comp.strip()
        if intersect[0] > -1:
            newline = line[0:lline - intersect[1] - 1] + comp
        else:
            newline = line + comp
        #print(newline)
        text.current_line.body = newline

        bpy.ops.text.move(type='LINE_END')

        return {'FINISHED'}


class TEXT_OT_intellisense_options_search(Operator):
    '''Options'''
    bl_idname = "text.intellioptions_search"
    bl_label = "Intellisense Options"
    bl_property = 'iputtext'

        
    iputtext:bpy.props.EnumProperty(name="test", items=make_enumlists)

    # text: bpy.props.StringProperty()
    def invoke(self, context, event):   
        # return context.window_manager.invoke_props_dialog(self)
        sc = context.space_data
        text = sc.text
        # If there is nothing on the text screen
        if text == None:
            pass
        # If it is in the text, the process is executed   
        elif text.current_character > 0:
            result = complete(context)
            text.current_line.body = result[0]
            bpy.ops.text.move(type='LINE_END')
            if result[2] != '':
                wm = context.window_manager
                wm.invoke_search_popup(self)
        

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        
        return context.active_object is not None

    def execute(self, context):
        sc = context.space_data
        text = sc.text

        comp = self.iputtext
        line = text.current_line.body

        lline = len(line)
        lcomp = len(comp)

        #intersect text
        intersect = [-1, -1]

        for i in range(lcomp):
            val1 = comp[0:i + 1]

            for j in range(lline):
                val2 = line[lline - j - 1::]
                #print("	",j, val2)

                if val1 == val2:
                    intersect = [i, j]
                    break

        comp = comp.strip()
        if intersect[0] > -1:
            newline = line[0:lline - intersect[1] - 1] + comp
        else:
            newline = line + comp
        #print(newline)
        text.current_line.body = newline

        bpy.ops.text.move(type='LINE_END')

        return {'FINISHED'}


class TEXT_OT_Intellisense(Operator):
    '''Text Editor Intellisense'''
    bl_idname = "text.intellisense"
    bl_label = "Text Editor Intellisense"

    text = ""

    #   @classmethod
    #   def poll(cls, context):
    #	   return context.active_object is not None

    def execute(self, context):
        sc = context.space_data
        text = sc.text

        if text.current_character > 0:
            result = complete(context)

            if result[2] == "":
                text.current_line.body = result[0]
                bpy.ops.text.move(type='LINE_END')
            else:
                bpy.ops.wm.call_menu(name=TEXT_MT_intellisense_menu.bl_idname)

        return {'FINISHED'}


class TEXT_PT_intellisense_panel(Panel):
    bl_label = "Intellisense"
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "Text"


    def draw(self, context):
        props = context.scene.intellisense_propertygroup
        layout = self.layout

        col = layout.column()

        col.operator("text.intellisense", text="Intellisense")
        col.menu("TEXT_MT_intellisense_menu", text="Options")
        col.prop(props,"use_send_console_line_break_bool")


class TEXT_MT_intellisense_menu(Menu):
    '''Intellisense Menu'''

    bl_label = "Intellisense"
    bl_idname = "TEXT_MT_intellisense_menu"

    text = ""

    def draw(self, context):

        # print(make_enumlists(context))

        layout = self.layout
        options = complete(context)
        options = options[2].split("\n")

        while("" in options) :
            options.remove("")

        att = False
        # pprint.pprint(options)

        for op in options:
            if op.find("attribute")>-1:
                att = True
            if not att:
                op = op.lstrip()
            # print('###op',op)
            layout.operator("text.intellioptions", text=op).text = op



classes = [
    TEXT_OT_intellisense_send_text,
    TEXT_OT_intellisense_send_console,
    TEXT_OT_Intellisense,
    TEXT_OT_intellisense_options,
    TEXT_MT_intellisense_menu,
    TEXT_PT_intellisense_panel,
    TEXT_OT_intellisense_options_search,
    TEXT_PG_intellisense_PropertyGroup,
    TEXT_AP_intellisense_AddonPreferences,
    ]


def panel_append(self, context):
    self.layout.separator()
    self.layout.menu("TEXT_MT_intellisense_menu")


def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:

        km = wm.keyconfigs.addon.keymaps.new(
            name='Text', space_type='TEXT_EDITOR')
        kmi = km.keymap_items.new(
            "text.intellioptions_search", #　Only search name is Text Generic. key map disappears when reloading.
            type='SPACE',
            value='PRESS',
            ctrl=False,
            shift=True)

        addon_intellisense_keymaps.append((km, kmi))


        km= wm.keyconfigs.addon.keymaps.new(
            name='Text', space_type='TEXT_EDITOR')
        kmi = km.keymap_items.new(
            "text.intellioptions_search_send_console",
            type='RET',
            value='PRESS',
            ctrl=True,
            shift=True)
        km = wm.keyconfigs.addon.keymaps.new(
            name='Text', space_type='TEXT_EDITOR')
        addon_intellisense_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(
            name='Text', space_type='TEXT_EDITOR')
        kmi = km.keymap_items.new(
            "text.intellioptions_search_send_text",
            type='RET',
            value='PRESS',
            ctrl=True,
            shift=True,
            alt=True)

        addon_intellisense_keymaps.append((km, kmi))


def register():

    for c in classes:
        bpy.utils.register_class(c)

    register_keymaps()


    bpy.types.TEXT_MT_edit.append(panel_append)
    bpy.types.TEXT_MT_context_menu.append(panel_append)
    bpy.types.Scene.intellisense_propertygroup = bpy.props.PointerProperty(type=TEXT_PG_intellisense_PropertyGroup)


def unregister_keymaps():

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_intellisense_keymaps:
            km.keymap_items.remove(kmi)
    addon_intellisense_keymaps.clear()


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    unregister_keymaps()

    bpy.types.TEXT_MT_edit.remove(panel_append)
    bpy.types.TEXT_MT_context_menu.remove(panel_append)

    del bpy.types.Scene.intellisense_propertygroup


if __name__ == "__main__":
    register()

