import bpy

try:
    from console import intellisense # type: ignore

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
        try:
            if "[" == line[-1]:
                cursor-=1
        except IndexError:
            pass
        result = intellisense.expand(line, cursor, console.locals)
        # print('###result', )
        # pprint.pprint(result)
    except AttributeError:
        result=""
        
    return result
