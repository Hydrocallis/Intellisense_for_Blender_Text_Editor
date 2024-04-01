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

    for index,op in enumerate(options):
        # 前後の空白を取り除いた文字列を作成
        op_stripped = op.strip()
        # もし最後の2文字が']'であれば、']'を含めたまま、その前の文字列を取得
        if op_stripped[-2:] == "']":
            op_cleaned = op_stripped
        else:
            # "'"と","を取り除いた文字列を作成
            op_cleaned = op_stripped.replace("'", "").replace(",", "")
        # 出力リストに追加
        inte_lists.append((op_cleaned,op_cleaned,"","",index))
        
    # pprint.pprint(inte_lists)

    return inte_lists

