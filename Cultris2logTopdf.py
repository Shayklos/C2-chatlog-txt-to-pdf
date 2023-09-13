from fpdf import FPDF
from os import listdir
from os.path import isfile, join, dirname, abspath
import sys
from random import shuffle
from colors import *


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
            pdf.add_font('Lucida', '',  r"c:\WINDOWS\Fonts\l_10646.ttf", uni = True)

            names = list(set([line.split(':')[0] for line in text if not (line[0] == line[-2] == '-')]))
            if len(names) <= len(high_contrast_color_list):
                name_colors = high_contrast_color_list
            else:
                name_colors = long_colors_list

            shuffle(name_colors)
            counter = 0
            for line in text:
                if line[0] == line[-2] == '-':
                    if "warned" in line or "kicked" in line or "banned" in line:
                        pdf.set_text_color(*dark_grey)
                        pdf.set_font('Arial', style= 'B', size = 11)
                    else:
                        pdf.set_font('Lucida', size = 9)
                        pdf.set_text_color(*light_grey)

                    pdf.multi_cell(190,5, txt = line)
                else:
                    double_colon_index = line.find(':')
                    splitted_line = {'name': line[:double_colon_index], 'msg': line[double_colon_index:]}
                    pdf.set_text_color(*name_colors[names.index(splitted_line['name'])%len(name_colors)])
                    # pdf.set_text_color(*name_colors[counter%len(name_colors)]) #for testing colors
                    counter+=1
                    pdf.set_font('Arial', style= 'B', size = 11)
                    pdf.cell(20,5, txt = splitted_line['name'], ln=0)
                    pdf.set_font('Lucida', size = 11)
                    pdf.set_text_color(*black)
                    pdf.multi_cell(160,5, txt = splitted_line['msg'])


            pdf.output(directory + "\\" + log[:-4] + '.pdf')


if __name__ == "__main__":
    # x = [1,2,3,4,5,6,7]
    # shuffle(x)
    # print(x)
    main()