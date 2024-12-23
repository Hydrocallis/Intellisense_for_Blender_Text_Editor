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
    "author": "Mackraken, tintwotin, Jose Conseco, Hydrocallis",
    "version": (0, 4, 1),
    "blender": (3, 6, 0),
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
                        IntProperty,                        )

######MODULE IMPORT START######

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

######MODULE IMPORT END########

from .utils.send_console import send_console
from .utils.send_text import send_text
from .utils.complete import complete
from .utils.text_selection import text_selection
from .utils.get_select_text import get_select_text
from .utils.make_enumlists import make_enumlists
# from . import addon_updater_ops

addon_intellisense_keymaps = []

def category_initialization():
    try:
        bpy.utils.unregister_class(TEXT_PT_intellisense_panel)

    except:
        pass
    addon_prefs = bpy.context.preferences.addons[__name__].preferences

    TEXT_PT_intellisense_panel.bl_category = addon_prefs.code_category
    bpy.utils.register_class(TEXT_PT_intellisense_panel)

class UpdaterProps:
    
    auto_check_update : bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False) # type: ignore

    updater_interval_months : bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)# type: ignore

    updater_interval_days : bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)# type: ignore

    updater_interval_hours : bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)# type: ignore

    updater_interval_minutes : bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)# type: ignore

class TEXT_AP_intellisense_AddonPreferences(AddonPreferences,UpdaterProps):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    def update_category(self, _):
        try:
            bpy.utils.unregister_class(TEXT_PT_intellisense_panel)
        except:
            pass

        TEXT_PT_intellisense_panel.bl_category = self.code_category
        bpy.utils.register_class(TEXT_PT_intellisense_panel)

    # Custom panel category
    code_category: StringProperty(
        name="Category",
        description="Category to show Import Any panel",
        default="Text",
        update=update_category,
    ) # type: ignore

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    ) # type: ignore

    show_autocomplete_Status: BoolProperty(
        name="show autocomplete Status",
        default=True,
    ) # type: ignore
    use_send_console_line_break_bool: BoolProperty(
        name="Use send console line break",
        default=True,
    ) # type: ignore

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "use_send_console_line_break_bool")
        layout.prop(self, "show_autocomplete_Status")
        layout.label(text="Addon Intellisense Keymaps")
        layout.prop(self, "code_category")
        mainrow = layout.row()
        col = mainrow.column()

		# Updater draw function, could also pass in col as third arg.
        # addon_updater_ops.update_settings_ui(self, context)
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
                ) # type: ignore

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
            if not sel.strip():  # 空文字列またはスペースのみの場合はスキップ
                continue
            send_text(context, sel)
        send_text(context, "\n")
    
        return {'FINISHED'}




class TEXT_OT_intellisense_send_text_options(Operator):


    item = [('LEN', "len()", "Get the length of an object",0),
        ('TYPE', "type()", "Get the type of an object",1),
        ('LIST_COMPREHENSION', "List Comprehension", "An example of list comprehension",2),
        ('NONE', "None", "",3)
       ]

    #'''Tooltip'''
    bl_idname = "text.intellioptions_send_text_options"
    bl_label = "line send text options"
    len_type_list_comprehension: bpy.props.EnumProperty(name="Options", description="", items=item) # type: ignore
    comprehension_option: bpy.props.StringProperty(name="comprehension option", description="", default="i") # type: ignore


    @classmethod
    def poll(cls, context):
        if len(bpy.data.texts) != 0:
            return True 
    def invoke(self, context, event):   
        return context.window_manager.invoke_props_dialog(self)

    def draw(self,context):
        row = self.layout.row(align=True)
        row.prop(self, 'len_type_list_comprehension', expand=True)  
        if self.len_type_list_comprehension == "LIST_COMPREHENSION":
            row =  self.layout.row(align=True)
            row.prop(self,"comprehension_option")

    def execute(self, context):

        start_text, select_text, end_text = get_select_text()
        if self.len_type_list_comprehension == "LEN":
            add_select_text = "len(" + select_text + ")"
        elif self.len_type_list_comprehension == "TYPE":
            add_select_text = "type(" + select_text + ")"
        elif self.len_type_list_comprehension == "LIST_COMPREHENSION":
            add_select_text = f"[{self.comprehension_option} for i in " + select_text + "]"
        elif self.len_type_list_comprehension == "NONE":
            add_select_text = select_text
        else:
            add_select_text = select_text

        send_text(context, add_select_text)

    
        return {'FINISHED'}
        
class TEXT_OT_intellisense_send_console(Operator):
    bl_idname = "text.intellioptions_send_console"
    bl_label = "line send console"


    @classmethod
    def poll(cls, context):
        if len(bpy.data.texts) != 0:
            return True 


    def execute(self, context):
    
        send_console(context)
        addon_prefs = context.preferences.addons[__name__].preferences

        if addon_prefs.use_send_console_line_break_bool == True:
            bpy.ops.text.line_break()

        return {'FINISHED'}
    
class TEXT_OT_intellisense_insert(Operator):
    bl_idname = "text.intellisense_insert"
    bl_label = "intellisense insert "

    @classmethod
    def poll(cls, context):
        if len(bpy.data.texts) != 0:
            return True 
        
    # cmd: StringProperty(default="", options={'HIDDEN'}) # type: ignore
    snippet: StringProperty(default="", options={'HIDDEN'}) # type: ignore

    def execute(self, context):
        bpy.ops.text.insert(text=self.snippet)
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


        
    iputtext:bpy.props.EnumProperty(name="test", items=make_enumlists) # type: ignore

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

class TEXT_PT_intellisense_Open_AddonPreferences(bpy.types.Operator):
    bl_idname = "text_pt_intellisense.open_addonpreferences"
    bl_label = "Open Addon Preferences"

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore


    def execute(self, context):


        preferences = bpy.context.preferences
        addon_prefs = preferences.addons["Intellisense_for_Blender_Text_Editor"].preferences

        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        addon_prefs.active_section = 'ADDONS'
        bpy.ops.preferences.addon_expand(module = "Intellisense_for_Blender_Text_Editor")
        bpy.ops.preferences.addon_show(module = "Intellisense_for_Blender_Text_Editor")



        return {'FINISHED'}
    
class TEXT_PT_intellisense_panel(Panel):
    bl_label = "Intellisense"
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "Text"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='VIEWZOOM')


    def is_len_supported(self, obj):
            # オブジェクトの型を取得
            obj_type = type(obj)
            
            # 型がlen関数をサポートしているかどうかを確認
            if hasattr(obj_type, '__len__'):
                return True,obj_type
            else:
                return False,obj_type

        # テスト用のオブジェクト
        # test_objects = ["Hello", [1, 2, 3], (1, 2, 3), {1: 'a', 2: 'b'}, {1, 2, 3}, b"bytes", bytearray(b"bytes")]

        # # テスト用のオブジェクトに対して実行可能かどうかを確認
        # for obj in test_objects:
        #     if is_len_supported(obj):
        #         print(f"オブジェクト {obj} はlen関数をサポートしています。len={len(obj)}")
        #     else:
        #         print(f"オブジェクト {obj} はlen関数をサポートしていません。")



    def draw(self, context):
        props = context.scene.intellisense_propertygroup
        addon_prefs = context.preferences.addons[__name__].preferences

        layout = self.layout


        col = layout.column()

        col.operator('text_pt_intellisense.open_addonpreferences',text="Setting",  icon="TOOL_SETTINGS")
        col.label(text="")
        col.operator("text.intellisense_search")
        col.operator("text.intellioptions_send_text")
        col.operator("text.intellioptions_send_text_options")
        sendconsolebox = col.box()
        sendconsolebox.operator("text.intellioptions_send_console")
        sendconsolebox.prop(addon_prefs,"use_send_console_line_break_bool")

        autocomplete_Status = col.box()
        autocomplete_Status.label(text="Autocomplete Status")
        autocomplete_Status.prop(addon_prefs, "show_autocomplete_Status")


        # start_text,select_text,end_text = get_select_text()
        # code=exec(select_text)

        # result,obj_type = self.is_len_supported(code)
        # autocomplete_Status.label(text=f"type: {obj_type}")
        # if result:
        #     autocomplete_Status.label(text=f"len: {len(obj_type)}")


        if addon_prefs.show_autocomplete_Status:


            items=make_enumlists(self,context)
            # autocomplete_Status.operator("text.intellisense_insert", text = items[0][2],icon="WORDWRAP_ON").snippet = items[0][2]

            for item in items:

                sele_item=item[0]

                autocomplete_Status.operator("text.intellisense_insert", text = sele_item, icon="WORDWRAP_ON").snippet = sele_item

classes = [
    TEXT_PT_intellisense_Open_AddonPreferences,
    TEXT_OT_intellisense_send_text_options,
    TEXT_OT_intellisense_send_text,
    TEXT_OT_intellisense_insert,
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

        km = wm.keyconfigs.addon.keymaps.new(
            name='Text', space_type='TEXT_EDITOR')
        kmi = km.keymap_items.new(
            "text.intellioptions_send_text_options",
            type='D',
            value='PRESS',
            ctrl=True,
            shift=True,
            alt=False)

        addon_intellisense_keymaps.append((km, kmi))

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

def register():
    # addon_updater_ops.register(bl_info)

    for c in classes:
        bpy.utils.register_class(c)

    register_keymaps()
    bpy.types.Scene.intellisense_propertygroup = bpy.props.PointerProperty(type=TEXT_PG_intellisense_PropertyGroup)
    category_initialization()

def unregister():
    # addon_updater_ops.unregister()
    for c in classes:
        bpy.utils.unregister_class(c)

    unregister_keymaps()

    del bpy.types.Scene.intellisense_propertygroup

if __name__ == "__main__":
    register()

