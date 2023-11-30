#!/usr/bin/env python3
import re
import string

# import an extended letter list (so that affiliation can exceed alphabet letters)
alphabet_letters = list(string.ascii_lowercase)
alphabet_letters.extend(['a'+l for l in alphabet_letters])

# Open the text file copied from ENUBET internal wiki and import its contend in "lines"
with open('author_list.txt') as fp:
    lines = fp.readlines()


# Create the "author" list of dictionaries for the authors
author_list = lines[0].replace("),", "),;").split(";")
authors = []
for a in author_list:
    name = ' '.join(a.replace('.','.$').split('$')[:-1]).strip()
    surname = a.replace('.','.$').split('$')[-1].split("(")[0].strip()
    affiliations = a.replace('.','.$').split('$')[-1].rstrip(",").replace(",",")(").replace("(","$(").split("$")[1:]
    affiliations = [aff.rstrip(",").rstrip(")").rstrip("\n").lstrip("(").rstrip(")")  for aff in affiliations]
    authors.append({'name': name,
                    'surname': surname,
                    'affiliations'  : affiliations})

# Create an affiliation dict (starting from the affiliation list from the text file)
affiliation_list = [l.rstrip("\n") for l in lines[2:]]
affiliation_dict = {l.split(" ")[0].lstrip("(").rstrip(")"): " ".join(l.split(" ")[1:]) for l in affiliation_list}


# Visit the affiliation dict in alphabetical order (names as listed in the wiki)
# When a new aff keys is encountered, assign to a letter and remove it from the keys
all_aff_keys = list(affiliation_dict.keys())
letter_index = 0
num_to_letter_aff_map = {}
for a in authors:
    for aff in a['affiliations']:
        if aff in all_aff_keys:
            num_to_letter_aff_map[aff] = alphabet_letters[letter_index]
            letter_index += 1
            all_aff_keys.remove(aff)
            

#############################
# print out the results (to the stdout)
#############################

# Author list
for a in authors:
    aff_keys = [num_to_letter_aff_map[num] for num in a['affiliations']]
    print(f"\\author[{','.join(aff_keys)}]{{{a['name']} {a['surname']}}}")
print('\n') #  black line
# Affiliation list
for num in num_to_letter_aff_map:
    print(f'\\affiliation[{num_to_letter_aff_map[num]}]{{{affiliation_dict[num]}}}')