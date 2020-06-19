#------------------------------------------------------------------------------
# Name:        File Actions Library
# Purpose:     A set of tools for better working with files & directories
#
# Author:      Hadi
#
# Created:     29/05/2020
# Copyright:   (c) Hadi 2020
# Licence:     <MIT>
#------------------------------------------------------------------------------
import os


class PowerDirectory(object):
      ''' A set of tools which makes working with files in a directory easier'''
      def __init__(self,address):
          assert os.path.exists(address)
          self.CURRENT_DIR=address
          self.file_subdir_list=os.scandir(address)


      def __str__(self):
          return self.CURRENT_DIR

      def __call__(self):
          self.CURRENT_DIR=address

      def full_address_file_list(self,directory):
        '''Makes a file list along with path of each file'''
        if directory in ('', None):
           directory = self.file_subdir_list
        file_list = []

        for entry in directory:
            if entry.is_file():
                print(entry.scandir_path)
                file_list.append(entry.path)

        print(file_list[-1])
        return file_list


      def full_address_dir_list(self,directory):
        '''Makes a file list along with path of each file'''
        dir_list = []

        for entry in self.file_subdir_list:
            if entry.is_dir():
                print(entry.path)
                dir_list.append(entry.path)

        print(dir_list[-1])
        return dir_list


      def apply_extension_filter(self, extension, directory):
        '''Returns a list of files. filters a given list of files based on the
           specified extension'''
        if directory in ('', None):
           directory = self.file_subdir_list
        filtered_file_list = []

        for item in self.full_address_file_list(directory):
            print(item)
            if os.path.isfile(item) and item[-4:] == extension:
               filtered_file_list.append(item)

        return filtered_file_list


      def apply_size_filter(self,
                            min_size,
                            max_size,
                            list_of_files
                            ):
        '''Returns a list files filtered by the min & max size given.
           The size must be in bytes format.'''

        if list_of_files in ([], None):
            directory = self.file_subdir_list
        filtered_list = []

        for item in self.file_subdir_list:
           if min_size < item.stat()[6] < max_size:
                filtered_list.append(item)

        return filtered_list



