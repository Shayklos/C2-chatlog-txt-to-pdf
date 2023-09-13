# Cultris II chatlog .txt to .pdf converter
Small tool for transforming Cultris 2 chatlogs from a `.txt` to a more readable `.pdf`.

Also a *decent* educative example on how to use `PyFPDF`.

By default it transforms all chatlogs in the same folder as the .py (or .exe if you compile it), but that can be easily changed.

Results are not deterministic in the sense that colors of usernames are random every time, for no real design reason.

Assumes that a font (by default `ggsans.ttf`) is on the main.py directory. This can be changed on the settings file (maybe change FONT_DIRECTORY to `r"c:\WINDOWS\Fonts\somefont.ttf"`) or simply remove the line of code and change the uses of the font to Arial or some other default font.