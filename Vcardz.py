#------------------------------------------------------------------------------
# Name:        Vcard Mgr
# Purpose:      A tool to edit, manage and deduplicate messy Vcards -
#                This is caused by some rubbish Persian Messengers
#
# Author:      Hadi
#
# Created:     27/05/2020
# Changed:     1399/03/09 Separated file action and vcard parser libs
# Changed:     1399/03/09 debugged foreplay and postplay actions
# Copyright:   (c) Hadi 2020
# Licence:     <MIT>
#------------------------------------------------------------------------------
import os

import threading

import multiprocessing

import VcardParserLib

import FileActionsLib

import Deeper

#===================================Constants==================================
CURRENT_DIR=FileActionsLib.PowerDirectory(os.getcwd()[:])


#===============================Main Course====================================

def main():
    '''main procedures'''
    answer = input(
    'Enter vcard file address(default has set to read first vcard file found \
                 in this directory):')
##    print(answer, type(answer))#log

    if answer != '':
##       print(f'{answer} was not empty.')#log

       try:# It is a good idea to add a feature to search a given directory.
           assert os.path.exists(answer)
##           print(os.path.exists(answer))

           assert os.path.isfile(answer)
##           print(os.path.isfile(answer))

           assert answer[-4:] == '.vcf'
##           print(f'{answer} was  a vcf file.')#log

           main_vcard_file = VcardParserLib.VCFile(answer)
           print(f'{main_vcard_file.file}\n \
                   {main_vcard_file.version}\n \
                   {main_vcard_file.content}'
                   )
           #COURSE OF ACTIONS GO HERE!

       except AssertionError:
              print('Bad address! Try again.')#log
              main()

    else:
        print(f'No file vcard specified.\n Searching {CURRENT_DIR} for .vcf file...')

        try:
            main_vcard_file = CURRENT_DIR.apply_extension_filter(
                              extension = 'vcf' )[0]
            print(f'Found {main_vcard_file} file...')

            print(main_vcard_file.content)

        except FileNotFoundError:
            print('No vcard file found!')

        finally:
            exit_prompt()


#==============================Other Functions=================================
def exit_prompt():
    '''exit routine run at the end.'''
    answer=input('Finished? Shall I exit(Y/N)')
    if answer in ('N','n', 'No', 'no'):
       main()

    elif answer in ('Y', 'y', 'Yes','yes'):
         print('Bye...')
         exit()

    else:
         print('Answer was not understood!')
         exit_prompt()

def vcard_creator(vcard):
    while vcard.vcard_que.not_empty:
          yield VcardParserLib.VCard(vcard.vcard_que.get())


if __name__ == '__main__':
    main()
