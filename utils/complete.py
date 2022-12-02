import bpy

try:
    from console import intellisense

except ModuleNotFoundError:
    from bl_console_utils.autocomplete import intellisense
        
from console_python import get_console


def complete(context):
    # righttsliceline =""

    sc = context.space_data
    try:
        text = sc.text

        region = context.region
        for area in context.screen.areas:
            if area.type == "CONSOLE":
                region = area.regions[1]
                break

        console = get_console(hash(region))[0]
        # print('###',console)

        line = text.current_line.body
        # print('###line body',line)
        cursor = text.current_character
        # 事前処理で[を入れているので検索キャラクターを1段下げる
        if "[" == line[-1]:
            cursor-=1
             # if "[" == line[-1]:
        #     cursor-=1

                # line=line[linefind:]
                # print("###linestlip",line)

            # print("##linerfound",line.rfind('import'))
        # current_position =bpy.context.space_data.text.current_character
        # ここでカーソルより左側のみ抽出する必要がある
        # leftsliceline = line[:current_position]
        # righttsliceline = line[current_position:]
        # print('###line',line)

        result = intellisense.expand(line, cursor, console.locals)
        # print('###result', )
        # pprint.pprint(result)
    except AttributeError:
        result=""
        
    return result
