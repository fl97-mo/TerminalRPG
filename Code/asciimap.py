from colors import Colors
import logging

logger = logging.getLogger(__name__)

class AsciiMap:
    THEMES = {
        "temperate forest": {
            "T": ("Olive", "Forest Green BG", None),        # trees
            "#": ("Bright Green", "Forest Green BG", None),    # bushes
            "X": ("Red", "Forest Green BG", None),             # tent
            "~": ("Bright Blue", "Bright Cyan BG", None),      # river
            " ": ("Mint", "Forest Green BG", None),            # grass
            ".": ("Slate Gray", "Forest Green BG", None),      # rock
            "═": ("Light Gray", "Forest Green BG", None),      # street w-e
            "╝": ("Light Gray", "Forest Green BG", None),      # street w-n
            "╔": ("Light Gray", "Forest Green BG", None),      # street s-e
            "║": ("Light Gray", "Forest Green BG", None),      # street s-n
            "≡": ("Peru", "Sienna BG", None)                   # bridge w-e
        }
    }
    
    def __init__(self, map_data, theme="temperate forest") -> None:
        self.map_data = map_data
        if theme not in self.THEMES:
            theme = "temperate forest"
        self.char_colors = dict(self.THEMES[theme])

    def set_char_color(self, char: str, color_name: str = None, bg_color_name: str = None, style_names=None) -> None:
        self.char_colors[char] = (color_name, bg_color_name, style_names)

    def draw_map(self) -> str:
        rendered_lines = []
        for row in self.map_data:
            colored_chars = []
            for char in row:
                color_name, bg_color_name, style_names = self.char_colors.get(char, ("White", None, None))
                colored_chars.append(Colors.color_text(char, color_name=color_name, bg_color_name=bg_color_name, style_names=style_names))
            rendered_lines.append("".join(colored_chars))
        return "\n".join(rendered_lines)

    def print_banner_above_map(self, text_line1: str, text_line2: str) -> None:
        max_text_len = max(len(text_line1), len(text_line2))
        width = max_text_len + 4

        top_border = "." + "-" * (width - 2) + "."
        middle_line1 = "|" + " " + text_line1.center(width - 4) + " " + "|"
        middle_line2 = "|" + " " + text_line2.center(width - 4) + " " + "|"
        bottom_border = "'" + "-" * (width - 2) + "'"

        banner_lines = [top_border, middle_line1, middle_line2, bottom_border]

        for line in banner_lines:
            print(Colors.color_text(line, color_name="Bright White", bg_color_name="Sienna BG"))
