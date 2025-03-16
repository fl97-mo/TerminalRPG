import os
import re
import textwrap

ANSI_ESCAPE_PATTERN = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_framed(title: str) -> None:
    border_len = max(40, len(title) + 6)
    print("┌" + "─" * (border_len - 2) + "┐")
    margin = (border_len - 2 - len(title)) // 2
    print("│" + " " * margin + title + " " * (border_len - 2 - margin - len(title)) + "│")
    print("└" + "─" * (border_len - 2) + "┘")

def visible_length(text: str) -> int:
    return len(ANSI_ESCAPE_PATTERN.sub('', text))

def pad_ansi_text(text: str, width: int) -> str:
    current_len = visible_length(text)
    return text + " " * max(0, width - current_len)

def print_two_column_screen(left_lines, right_lines, left_title="Left", right_title="Right") -> None:
    left_width = 50
    right_width = 50
    header_left = f" {left_title} ".center(left_width, "─")
    header_right = f" {right_title} ".center(right_width, "─")
    
    print("┌" + header_left + "┬" + header_right + "┐")
    
    wrapped_left = [textwrap.wrap(line, width=left_width) if line else [""] for line in left_lines]
    wrapped_right = [textwrap.wrap(line, width=right_width) if line else [""] for line in right_lines]
    
    num_rows = max(len(wrapped_left), len(wrapped_right))
    if len(wrapped_left) < num_rows:
        wrapped_left.extend([[""]]*(num_rows - len(wrapped_left)))
    if len(wrapped_right) < num_rows:
        wrapped_right.extend([[""]]*(num_rows - len(wrapped_right)))
    
    for i in range(num_rows):
        cell_left = wrapped_left[i]
        cell_right = wrapped_right[i]
        row_height = max(len(cell_left), len(cell_right))
        while len(cell_left) < row_height:
            cell_left.append("")
        while len(cell_right) < row_height:
            cell_right.append("")
        for j in range(row_height):
            l_text = cell_left[j].ljust(left_width)
            r_text = cell_right[j].ljust(right_width)
            print("│" + l_text + "│" + r_text + "│")
    
    print("└" + "─"*left_width + "┴" + "─"*right_width + "┘")

def print_three_column_screen(left_lines, middle_lines, right_lines,
left_title="Left", middle_title="Middle", right_title="Right") -> None:
    width_left = 30
    width_middle = 40
    width_right = 34

    top_left   = pad_ansi_text(f" {left_title} ", width_left)
    top_middle = pad_ansi_text(f" {middle_title} ", width_middle)
    top_right  = pad_ansi_text(f" {right_title} ", width_right)

    print("┌" + top_left.replace(" ", "─") +
        "┬" + top_middle.replace(" ", "─") +
        "┬" + top_right.replace(" ", "─") + "┐")

    max_lines = max(len(left_lines), len(middle_lines), len(right_lines))

    for i in range(max_lines):
        l_text = left_lines[i] if i < len(left_lines) else ""
        m_text = middle_lines[i] if i < len(middle_lines) else ""
        r_text = right_lines[i] if i < len(right_lines) else ""

        l_text = pad_ansi_text(l_text, width_left)
        m_text = pad_ansi_text(m_text, width_middle)
        r_text = pad_ansi_text(r_text, width_right)

        print(f"│{l_text}│{m_text}│{r_text}│")

    print("└" + ("─" * width_left) +
          "┴" + ("─" * width_middle) +
          "┴" + ("─" * width_right) + "┘")
