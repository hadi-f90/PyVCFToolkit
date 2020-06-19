#-------------------------------------------------------------------------------
# Name:        VcardPaserLib
# Purpose:     A set of tools in a for of a python library to read and manipulate vcard sotred in vcf files
#
# Author:      Hadi
#
# Created:     29/05/2020
# Changed:                Optimized VCFile Class- now works far more faster in a few lines of code
# Changed:     19/06/2020 Changed data gathering and storage system by fully mplementing an rx_dict object
#                         Changed VCFile class to use regex for searching vcf data
# Copyright:   (c) Hadi 2020
# Licence:     <MIT>
#-------------------------------------------------------------------------------

import re

from os.path import getsize

from sys import getsizeof

import datetime

import qrcode

import Deeper

import time


class VCFile(object):
    def __init__(self, file):
        '''determine the type of vcard for further analysis.'''
        self.file = open(file,'rt')
        self.vcard_list = []
        self.vcard_counter = 0
        self.read_vcards_in_file()

    def read_vcards_in_file(self):
        '''stores a contacts data in a form que of lists containing lines of vcard data.'''
        self.vcard_list = re.findall(r"BEGIN:VCARD\n(?P<vcard>(.|\n)*?)\nEND:VCARD\n?", self.file.read(), re.MULTILINE |re.VERBOSE)
        self.vcard_counter = len(self.vcard_list)


class VCard(VCFile):
    def __init__(self, _vcard_string):
        self.vcard_string = _vcard_string
        self.fields = { #TODO: CHANGE TO ADAPT THE SPECIFIED FORMAT or create a new format for saving in memory
        # header data
        'VERSION':re.compile(r"VERSION:(?P<version>[2-4].[0-1])", re.MULTILINE |re.VERBOSE),
        'REV':datetime.datetime.now(),# A timestamp for the last time the vCard was updated
        'SOURCE':re.compile(r"SOURCE:(?P<source>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", re.MULTILINE |re.VERBOSE),# A URL that can be used to get the latest version of this vCard.
##        'CLASS':re.compile(r""),# Describes the sensitivity of the information in the vCard.
##        'KEY':re.compile(r""), #The public encryption key associated with the vCard object. It may point to an external URL, may be plain text, or may be embedded in the vCard as a Base64 encoded block of text.
        'PRODID':'Edited in VCFParserLib',# The identifier for the product that created the vCard object.

        #personal info
        'N':re.compile(r"^N(;CHARSET=(?P<encoding>.*);.*)*?:;(?P<name>).*", re.MULTILINE |re.VERBOSE), #name field
        'FN':re.compile(r"FN(;CHARSET=(?P<encoding>.*);.*)*?:(?P<formated_name>.*)", re.MULTILINE |re.VERBOSE), #The formatted name string associated with the vCard object.
        'TITLE':re.compile(r"TITLE(;CHARSET=(?P<encoding>.*);.*)*?:(?P<title>.*)", re.MULTILINE |re.VERBOSE),
##        'SOUND':re.compile(r""),# By default, if this property is not grouped with other properties it specifies the pronunciation of the FN property of the vCard object
##        'GENDER':re.compile(r""),
        'NICKNAME':re.compile(r"NICKNAME(;CHARSET=(?P<encoding>.*);.*)*?:(?P<nickname>.*)", re.MULTILINE |re.VERBOSE), # One or more descriptive/familiar names for the object represented by this vCard.
        'NAME':re.compile(r"NAME(;CHARSET=(?P<encoding>.*);.*)*?:(?P<source_name>.*)", re.MULTILINE |re.VERBOSE), #Provides a textual representation of the SOURCE property
##        'KIND':re.compile(r""),# Defines the type of entity that this vCard represents: 'application', 'individual', 'group', 'location' or 'organization'; 'x-*' values may be used for experimental purposes The KIND property must be set to "group" in order to use this property.
##        'CATEGORIES':[],# A list of "tags" that can be used to describe the object represented by this vCard.
##        'LANG':re.compile(r""),# Defines a language that the person speaks

           #gfx
        'LOGO':re.compile(r"LOGO;ENCODING=(?P<encoding>.*);(?P<logo_format>.*):(?P<logo>[a-zA-Z0-9/=+\n\s]*$)", re.MULTILINE |re.VERBOSE),# An image or graphic of the logo of the organization that is associated with the individual to which the vCard belongs.
        'PHOTO':re.compile(r"PHOTO;ENCODING=(?P<encoding>.*);(?P<photo_format>.*):(?P<photo>[a-zA-Z0-9/=+\n\s]*$)", re.MULTILINE |re.VERBOSE),# An image or photograph of the individual associated with the vCard.

           #organization & physical address
        'ORG':re.compile(r"ORG(;CHARSET=(?P<encoding>.*);.*)*?:(?P<organization>.*)", re.MULTILINE |re.VERBOSE),# the name and optionally the unit(s) of the organization associated with the vCard object.
        'ROLE':re.compile(r"ROLE(;CHARSET=(?P<encoding>.*);.*)*?:(?P<role>.*)", re.MULTILINE |re.VERBOSE),# The role, occupation, or business category of the vCard object within an organization.

##        'ADR':re.compile(r"", re.MULTILINE |re.VERBOSE), #A structured representation of the physical delivery address for the vCard object.
##        'AGENT':re.compile(r"", string, re.MULTILINE |re.VERBOSE), #Information about another person who will act on behalf of the vCard object. Typically this would be an area administrator, assistant, or secretary for the individual. Can be either a URL or an embedded vCard.
        'GEO':re.compile(r"GEO:(?P<geo>-?\d{2,}\.\d{2,};-?\d{2,}\.\d{2,})", re.MULTILINE |re.VERBOSE),# Specifies a latitude and longitude. 2.1, 3.0: GEO:39.95;-75.1667
##                       LABEL Represents the actual text that should be put on the mailing label when delivering a physical package to the person/object associated with the vCard (related to the ADR property).

           #telephone data
        'TEL':re.compile(r"TEL;(?P<type>.*):(?P<number>[0-9-+]{3,17})", re.MULTILINE |re.VERBOSE),

           #email, IM & website
##        'IMPP':re.compile(r""),# Defines an instant messenger handle. This property was introduced in a separate RFC when the latest vCard version was 3.0. Therefore, 3.0 vCards might use this property without otherwise declaring it.
        'EMAIL':re.compile(r"EMAIL:(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.MULTILINE |re.VERBOSE),# The address for electronic mail communication with the vCard object.
##                       MAILER Type of email program used.
        'URL':re.compile(r"URL:(?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", re.MULTILINE |re.VERBOSE),# A URL pointing to a website that represents the person in some way.

           #calandar data
        'ANNIVERSARY': re.compile(r"ANNIVERSARY:(?P<anniversary>(\d{2,4}/\d{2,4}/\d{2,4}))", re.MULTILINE |re.VERBOSE), #Defines the person's anniversary.
        'BDAY': re.compile(r"BDAY:(?P<birthday>(\d{2,4}/\d{2,4}/\d{2,4}))", re.MULTILINE |re.VERBOSE), # Date of birth of the individual associated with the vCard.
        'CALADRURI':re.compile(r"CALADRURI:(?P<calander_url1>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", re.MULTILINE |re.VERBOSE),# A URL to use for sending a scheduling request to the person's calendar.
        'CALURI':re.compile(r"CALURI:(?P<calander_url2>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", re.MULTILINE |re.VERBOSE),# A URL to the person's calendar.
##          'TZ':re.compile(r""),# The time zone of the vCard object.
           ##FBURL Defines a URL that shows when the person is "free" or "busy" on their calendar
        'NOTE':re.compile(r"NOTE:(?P<note>.*)", re.MULTILINE |re.VERBOSE),
##                       'CLIENTPIDMAP':re.compile(r""), # Used for synchronizing different revisions of the same vCard.
##                         MEMBER '''Defines a member that is part of the group that this vCard represents. Acceptable values include:
##                                  a "mailto:" URL containing an email address
##                                a UID which references the member's own vCard''

##                       RELATED '''Another entity that the person is related to. Acceptable values include:
##                              a "mailto:" URL containing an email address
##                              a UID which references the person's own vCard'''
##                       SORT-STRING Defines a string that should be used when an application sorts this vCard in some way.
##                       UID Specifies a value that represents a persistent, globally unique identifier associated with the object.
##                       XML Any XML data that is attached to the vCard. This is used if the vCard was encoded in XML
##                         The KIND property must be set to "group" in order to use this property.
                       }


    def __str__(self):
        '''Concatenates and returns name fields.'''
        return

    def __eq__(self, other):
        return self.is_duplicate(other)

    def __add__(self, other):
        pass


    def is_duplicate(self, other):
        '''Finds if this vcard entry is similar or indetical to another one or not.'''
         #TO BE IMPLEMENTED:
        pass

    def is_null(self):
        '''Specifies whether a vcard entry lacks vcard data e.g. TEL, EMAIL, etc'''
        #Todo: Asserts that all fields are filled : email, phone number, address, except name data
        pass

    def version(self):
        '''Returns the version of vcf.'''
        return self.fields['VERSION'].search(self.vcard_string).group('version')

    def qr_code(self):
        '''Generates the QR code of the the Vcard.'''
        qrcode.make(self, self.vcard_string)

    def phone_numbers(self):
        '''
        Returns a list of tuples of phone numbers fields in vcf data.
        The first item in each tuple is phone type e.g. mobile, work
        The latter is the number.'''

        return self.fields['TEL'].findall(self.vcard_string)


    def name_data(self):
        '''Returns a tuple of namefields of the vcard in this order:
                   title,
                   name,
                   source name,
                   formatted name, and
                   nickname.'''

        return (self.fields['TITLE'].search(self.vcard_string).group('title'),
                self.fields['N'].search(self.vcard_string).group('name'),
                self.fields['NAME'].search(self.vcard_string).group('source_name'),
                self.fields['FN'].search(self.vcard_string).group('formated_name'),
                self.fields['NICKNAME'].search(self.vcard_string).group('nickname'))

    def photo(self):
        '''
        Returns a tuple cantaining photo and logo data.'''
        return (self.fields['PHOTO'].search(self.vcard_string).group('photo'),
               self.fields['LOGO'].search(self.vcard_string).group('logo'))


class VCard2(VCard):
      #Todo: VCard2 specific fields go here
    pass

class VCard3(VCard):
    #Todo: VCard3 specific fields go here
    pass

class VCard4(VCard):
      #Todo: VCard4 specific fields go here
    pass

