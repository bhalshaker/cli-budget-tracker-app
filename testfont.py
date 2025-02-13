import pyfiglet

text = "Budget Tracker App"

# List of available fonts
#fonts = pyfiglet.FigletFont.getFonts()

# Print the text with each font
#for font in fonts:
#print(f"\nUsing font: {font}")
print(pyfiglet.figlet_format(text, font='small'))