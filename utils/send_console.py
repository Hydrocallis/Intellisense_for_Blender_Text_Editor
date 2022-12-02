
import bpy

        
from console_python import get_console


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
        # elif "if" in line:
        #     console.push(line)

        else:

            # print("not processed")
            text ="not processed"
            ShowMessageBox(text) 
   