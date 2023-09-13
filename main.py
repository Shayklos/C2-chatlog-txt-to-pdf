from fpdf import FPDF
from os import listdir
from os.path import isfile, join, dirname, abspath
import sys
from random import shuffle
from colors import *
from settings import * 

def main():
    if getattr(sys, 'frozen', False):
        directory = dirname(sys.executable) #directory when using .exe
    else:
        directory = dirname(abspath(__file__)) #directory when using .py

    #List with all the logs
    CultrisLogs = [file for file in listdir(directory) if file[-4:].lower() == ".txt" and "Cultris" in file and isfile(join(directory, file))]
    print(CultrisLogs)

    for log in CultrisLogs:
        with open(log) as file:
            text = file.readlines()
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font('ggsans', '',  r"ggsans.ttf", uni = True)

            names = list(set([line.split(':')[0] for line in text if not (line[0] == line[-2] == '-')]))
            if align:
                _width_constant = NAME_WIDTH_CONSTANT + NAME_WIDTH_CONSTANT*max([len(name) for name in names])
            #Use high contrast colors if there are not many players. Otherwise use a longer list of colors
            if len(names) <= len(high_contrast_color_list):
                name_colors = high_contrast_color_list
            else:
                name_colors = long_colors_list

            shuffle(name_colors) #Remove this to consistently have the same username colors
            for line in text:

                #Mod actions look different
                if line[0] == line[-2] == '-':
                    if "warned" in line or "kicked" in line or "banned" in line:
                        pdf.set_text_color(*dark_grey)
                        pdf.set_font('Arial', style= 'B', size = FONT_SIZE)
                    else:
                        pdf.set_font('ggsans', size = FONT_SIZE-2)
                        pdf.set_text_color(*light_grey)

                    pdf.multi_cell(190, HEIGHT, txt = line)
                else:

                    #Set color and font to only name of the user
                    double_colon_index = line.find(':')
                    splitted_line = {'name': line[:double_colon_index], 'msg': line[double_colon_index:]}
                    pdf.set_text_color(*name_colors[names.index(splitted_line['name'])%len(name_colors)])
                    pdf.set_font('Arial', style= 'B', size = FONT_SIZE)
                    if align:
                        pdf.cell(_width_constant, HEIGHT, txt = splitted_line['name'])
                    else:
                        pdf.cell(NAME_WIDTH_CONSTANT + NAME_WIDTH_CONSTANT*len(splitted_line['name']), HEIGHT, txt = splitted_line['name'])

                    #Rest of the line
                    pdf.set_font('ggsans', size = FONT_SIZE)
                    pdf.set_text_color(*black)
                    if align:
                        pdf.multi_cell(180-_width_constant, HEIGHT, txt = splitted_line['msg']) #Multicell for longer messages
                    else:
                        pdf.multi_cell(180-NAME_WIDTH_CONSTANT - NAME_WIDTH_CONSTANT*len(splitted_line['name']), HEIGHT, txt = splitted_line['msg']) #Multicell for longer messages

            #Save resulting .pdf
            pdf.output(directory + "\\" + log[:-4] + '.pdf')


if __name__ == "__main__":
    main()