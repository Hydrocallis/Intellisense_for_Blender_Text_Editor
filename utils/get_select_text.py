import bpy
# https://blender.stackexchange.com/a/218189/89484
def get_select_text():
    text = bpy.context.space_data.text

    fschar = text.current_character
    fsline = text.current_line_index
    fechar = text.select_end_character
    feline = text.select_end_line_index

    # The end and start lines and characters can be switched
    # depending on the direction in which the text was selected
    schar = min(fschar,fechar)
    echar = max(fschar,fechar)
    sline = min(fsline,feline)
    eline = max(fsline,feline)

    original_text = text.as_string()
    lines = original_text.split("\n")

    for line in range(sline, eline + 1):
        cur_line = lines[line]
        
        start_char = 0
        end_char = len(cur_line)
        
        if line == sline:
            start_char = schar
            
        if line == eline:
            end_char = echar
        
        # Uppercase the selected part of this line
        oldline = "".join((cur_line[:start_char], cur_line[start_char:end_char], cur_line[end_char:]))
        # # Uppercase the selected part of this line
        # new_line = "".join((cur_line[:start_char], cur_line[start_char:end_char].upper(), cur_line[end_char:]))
        # lines[line] = new_line
    start_text,select_text,end_text=(cur_line[:start_char], cur_line[start_char:end_char], cur_line[end_char:])
    
    return start_text,select_text,end_text
