def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        # Check if adding the new word to the current line would exceed the max width
        size = font.size(current_line + word + ' ')[0]
        if size < max_width:
            current_line += word + ' '
        else:
            lines.append(current_line)  # Add the current line to lines
            current_line = word + ' '  # Start a new line with the current word
    
    lines.append(current_line)  # Add the last line
    return lines