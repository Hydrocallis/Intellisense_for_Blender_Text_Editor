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
    "version": (0, 3, 7),
    "blender": (3, 6, 0),
    "location": " Text Editor in Scripting tab> Ctrl + Shift + Space, Edit and Context menus,Ctrl + Shift + ENTER, send console",
    "description": "Adds intellisense to the Text Editor",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development",
}


## チェックリスト
# bpy.context.window_manager.keyconfigs.addon.keymaps['
# bpy.context.selected_objcetで数がでるか
# print(bpy.context)で間がはいるか
# import bpy
# form import ができるか

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


######MODULE IMPORT######

from .utils.send_console import send_console
from .utils.send_text import send_text
from .utils.complete import complete
from .utils.text_selection import text_selection
from .utils.make_enumlists import make_enumlists

def reload_unity_modules(name):
    import os
    import importlib
   
    utils_modules = sorted([name[:-3] for name in os.listdir(os.path.join(__path__[0], "utils")) if name.endswith('.py')])

    for module in utils_modules:
        impline = "from . utils import %s" % (module)

        # print("###hydoro unity reloading one %s" % (".".join([name] + ['utils'] + [module])))

        exec(impline)
        importlib.reload(eval(module))

    modules = []

    for path, module in modules:
        if path:
            impline = "from . %s import %s" % (".".join(path), module)
        else:
            impline = "from . import %s" % (module)

        print("###hydoro unity reloading second %s" % (".".join([name] + path + [module])))

        exec(impline)
        importlib.reload(eval(module))


if 'bpy' in locals():
    reload_unity_modules(bl_info['name'])

########################


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
                    # print('###kmi_add.idname',kmi_add.idname)     

                    if not kmi_con.id in old_id_l:
                        kmi = kmi_con 
                        old_id_l.append(kmi_con.id) 
                        # print('###old_id_l',old_id_l)     
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
    bl_idname = "text.intellioptions_send_text"
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
    bl_idname = "text.intellioptions_send_console"
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

    
class TEXT_OT_intellisense_search(Operator):
    '''Options'''
    bl_idname = "text.intellisense_search"
    bl_label = "Intellisense Search"
    bl_property = 'iputtext'

    @classmethod
    def poll(cls, context):
        if len(bpy.data.texts) != 0:
            return True 


        
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
            leftbodyline=text.current_line.body[:text.current_character]
            righttbodyline=text.current_line.body[text.current_character:]
            # print("###leftbodyline",leftbodyline)
            # print("###righttbodyline",righttbodyline)
            # コンソールに送るために右端を削除してあげないといけない
            text.current_line.body = leftbodyline
            result = complete(context)
            # 右端削除を元に戻す
            if result[0][-1] ==".":
                # print('###a',)
                # .が帰ってきた時
                text.current_line.body = result[0] + righttbodyline

            if result != "":
                # print('###b',result[2].split("\n"))
                if result[2] != "":
                    if result[2].split("\n")[0][-1] =="]":

                        text.current_line.body = result[0]+ righttbodyline

                        text.current_character = len(result[0])
                        text.select_end_character = len(result[0])
                        # print('###bb',)
                    # 候補が２つの場合（.も含む)
                    else:
                        # print('###c',)
                        text.current_line.body = result[0] + righttbodyline
                        text.current_character = len(result[0])
                        text.select_end_character = len(result[0])
                
             # 候補が２つの場合（.も含む)

            else:
                # print('###c',)
                text.current_line.body = leftbodyline + righttbodyline

            if result[2] == '':
                # print('###d',)
                # この場合はドッドになる
                if result[0][-1] ==".":
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                # fromなどの処理
                text.current_line.body = result[0] + righttbodyline
                text.current_character = len(result[0])
                text.select_end_character = len(result[0])
                # print('###result',result)
            
            # リザルトに入ってる場合
            if result[2] != '':
                wm = context.window_manager
                wm.invoke_search_popup(self)
        

        return {'FINISHED'}


    def execute(self, context):
        bpy.ops.ed.undo_push() 

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
        # print('###',intersect)
        if intersect[0] > -1:
            # newline = line[0:lline - intersect[1] - 1] + comp + line[text.current_character:]
            newline = line[:text.current_character] + comp + line[text.current_character:]
            # print('###comp',comp)
            # print('###a',intersect)


        else:
            newline = line[:text.current_character] + comp + line[text.current_character:]
            # print('###b',)
            # print('###comp2',comp)
        #print(newline)
        text.current_line.body = newline

        for textcount in range(len(comp)):
            bpy.ops.text.move(type='NEXT_CHARACTER')
        


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

        col.operator("text.intellisense_search")
        col.operator("text.intellioptions_send_text")
        sendconsolebox = col.box()
        sendconsolebox.operator("text.intellioptions_send_console")
        sendconsolebox.prop(props,"use_send_console_line_break_bool")


classes = [
    TEXT_OT_intellisense_send_text,
    TEXT_OT_intellisense_send_console,
    TEXT_PT_intellisense_panel,
    TEXT_OT_intellisense_search,
    TEXT_PG_intellisense_PropertyGroup,
    TEXT_AP_intellisense_AddonPreferences,
    ]


def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:

        km = wm.keyconfigs.addon.keymaps.new(
            name='Text', space_type='TEXT_EDITOR')
        kmi = km.keymap_items.new(
            "text.intellisense_search", #　Only search name is Text Generic. key map disappears when reloading.
            type='SPACE',
            value='PRESS',
            ctrl=True,
            shift=True)

        addon_intellisense_keymaps.append((km, kmi))

        km= wm.keyconfigs.addon.keymaps.new(
            name='Text', space_type='TEXT_EDITOR')
        kmi = km.keymap_items.new(
            "text.intellioptions_send_console",
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
            "text.intellioptions_send_text",
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

    bpy.types.Scene.intellisense_propertygroup = bpy.props.PointerProperty(type=TEXT_PG_intellisense_PropertyGroup)


def unregister_keymaps():

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for i , j in addon_intellisense_keymaps:
            # print('###i j ',i.keymap_items , j)
            pass
        for km, kmi in addon_intellisense_keymaps:
            try:
                km.keymap_items.remove(kmi)
            except:
                # print('###error',kmi)
                pass
    addon_intellisense_keymaps.clear()


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    unregister_keymaps()

    del bpy.types.Scene.intellisense_propertygroup


if __name__ == "__main__":
    register()

