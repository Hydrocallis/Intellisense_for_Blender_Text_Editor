
import bpy

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
        # print('###1',txt.lines[endlineincex].body)
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
