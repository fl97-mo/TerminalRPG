# added temporarly, asni colors and formatting tool in order to make "painting" and formatting in the terminal easier. most will be removed after
# i finished designing
class Colors:
    text_colors = {
        "Black": "\033[30m",
        "Red": "\033[31m",
        "Green": "\033[32m",
        "Yellow": "\033[33m",
        "Blue": "\033[34m",
        "Magenta": "\033[35m",
        "Cyan": "\033[36m",
        "White": "\033[37m",
        "Bright Black": "\033[90m",
        "Bright Red": "\033[91m",
        "Bright Green": "\033[92m",
        "Bright Yellow": "\033[93m",
        "Bright Blue": "\033[94m",
        "Bright Magenta": "\033[95m",
        "Bright Cyan": "\033[96m",
        "Bright White": "\033[97m",
        "Maroon": "\033[38;5;52m",
        "Olive": "\033[38;5;64m",
        "Forest Green": "\033[38;5;22m",
        "Teal": "\033[38;5;30m",
        "Navy": "\033[38;5;19m",
        "Purple": "\033[38;5;90m",
        "Indigo": "\033[38;5;54m",
        "Violet": "\033[38;5;57m",
        "Pink": "\033[38;5;13m",
        "Orange": "\033[38;5;208m",
        "Gold": "\033[38;5;220m",
        "Khaki": "\033[38;5;228m",
        "Chocolate": "\033[38;5;94m",
        "Coral": "\033[38;5;203m",
        "Crimson": "\033[38;5;161m",
        "Salmon": "\033[38;5;209m",
        "Orchid": "\033[38;5;170m",
        "Plum": "\033[38;5;135m",
        "Turquoise": "\033[38;5;80m",
        "Aquamarine": "\033[38;5;86m",
        "Sky Blue": "\033[38;5;117m",
        "Slate Gray": "\033[38;5;102m",
        "Gray": "\033[38;5;8m",
        "Dark Gray": "\033[38;5;59m",
        "Light Gray": "\033[38;5;250m",
        "Beige": "\033[38;5;230m",
        "Ivory": "\033[38;5;230m",
        "Mint": "\033[38;5;121m",
        "Rose": "\033[38;5;218m",
        "Lavender": "\033[38;5;183m",
        "Deep Pink": "\033[38;5;198m",
        "Sienna": "\033[38;5;130m",
        "Peru": "\033[38;5;173m",
        "Chartreuse": "\033[38;5;118m",
    }

    background_colors = {
        "Black BG": "\033[40m",
        "Red BG": "\033[41m",
        "Green BG": "\033[42m",
        "Yellow BG": "\033[43m",
        "Blue BG": "\033[44m",
        "Magenta BG": "\033[45m",
        "Cyan BG": "\033[46m",
        "White BG": "\033[47m",
        "Bright Black BG": "\033[100m",
        "Bright Red BG": "\033[101m",
        "Bright Green BG": "\033[102m",
        "Bright Yellow BG": "\033[103m",
        "Bright Blue BG": "\033[104m",
        "Bright Magenta BG": "\033[105m",
        "Bright Cyan BG": "\033[106m",
        "Bright White BG": "\033[107m",
        "Maroon BG": "\033[48;5;52m",
        "Olive BG": "\033[48;5;64m",
        "Forest Green BG": "\033[48;5;22m",
        "Teal BG": "\033[48;5;30m",
        "Navy BG": "\033[48;5;19m",
        "Purple BG": "\033[48;5;90m",
        "Indigo BG": "\033[48;5;54m",
        "Violet BG": "\033[48;5;57m",
        "Pink BG": "\033[48;5;13m",
        "Orange BG": "\033[48;5;208m",
        "Gold BG": "\033[48;5;220m",
        "Khaki BG": "\033[48;5;228m",
        "Chocolate BG": "\033[48;5;94m",
        "Coral BG": "\033[48;5;203m",
        "Crimson BG": "\033[48;5;161m",
        "Salmon BG": "\033[48;5;209m",
        "Orchid BG": "\033[48;5;170m",
        "Plum BG": "\033[48;5;135m",
        "Turquoise BG": "\033[48;5;80m",
        "Aquamarine BG": "\033[48;5;86m",
        "Sky Blue BG": "\033[48;5;117m",
        "Slate Gray BG": "\033[48;5;102m",
        "Gray BG": "\033[48;5;8m",
        "Dark Gray BG": "\033[48;5;59m",
        "Light Gray BG": "\033[48;5;250m",
        "Beige BG": "\033[48;5;230m",
        "Ivory BG": "\033[48;5;230m",
        "Mint BG": "\033[48;5;121m",
        "Rose BG": "\033[48;5;218m",
        "Lavender BG": "\033[48;5;183m",
        "Deep Pink BG": "\033[48;5;198m",
        "Sienna BG": "\033[48;5;130m",
        "Peru BG": "\033[48;5;173m",
        "Chartreuse BG": "\033[48;5;118m",
    }

    text_styles = {
        "Reset": "\033[0m",
        "Bold": "\033[1m",
        "Underline": "\033[4m",
        "Blink": "\033[5m",
        "Inverted": "\033[7m",
    }

    @staticmethod
    def color_text(text, color_name=None, bg_color_name=None, style_names=None):
        formatted = ""
        if style_names:
            if isinstance(style_names, list):
                for style in style_names:
                    formatted += Colors.text_styles.get(style, "")
            else:
                formatted += Colors.text_styles.get(style_names, "")
        if color_name:
            formatted += Colors.text_colors.get(color_name, "")
        if bg_color_name:
            formatted += Colors.background_colors.get(bg_color_name, "")
        formatted += text
        formatted += Colors.text_styles["Reset"]
        return formatted

    @staticmethod
    def show_all():
        print("=== Textcolors ===")
        for name, code in Colors.text_colors.items():
            sample = f"{code}{name}{Colors.text_styles['Reset']}"
            print(f"{name:15} {sample}")
        print("\n=== Background colors ===")
        for name, code in Colors.background_colors.items():
            sample = f"{code}  {Colors.text_styles['Reset']}"
            print(f"{name:15} {sample}")
        print("\n=== Textstyles ===")
        for name, code in Colors.text_styles.items():
            sample = f"{code}{name}{Colors.text_styles['Reset']}"
            print(f"{name:15} {sample}")

if __name__ == "__main__":
    Colors.show_all()
