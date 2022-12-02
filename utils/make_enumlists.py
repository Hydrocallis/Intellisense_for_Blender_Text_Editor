import bpy
from ..utils.complete import complete
def make_enumlists(self,context):
    
    inte_lists=[]
    # options   は検索結果の候補の中身
    options = complete(bpy.context)
    # print('###option',options)
    if options != "":
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