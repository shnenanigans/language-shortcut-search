import json
import os


def check_item(item): #checks if item exists in minecraft
    item = item.lower()
    with open('mclanguages\en_ca.json', 'r') as j:
        en_ca = json.load(j)

    key_list = list(en_ca.keys())
    val_list = list(map(lambda x:x.lower(), list(en_ca.values()))) #make values lowercase
    position = val_list.index(item)
    return key_list[position]

def del_long_seq(substrings):
    filter = set(item for item in substrings if len(item) <= 2) #can make this 1 for 1 character searches only but uhhh dont
    return filter

#thanks chatgpt
def findseq(strings):
    substrings = set(strings[0][i:j] for i in range(len(strings[0])) for j in range(i + 1, len(strings[0]) + 1))

    for string in strings[1:]:
        current_substrings = set(string[i:j] for i in range(len(string)) for j in range(i + 1, len(string) + 1))
        substrings = substrings.intersection(current_substrings)
    
    return del_long_seq(substrings)


def get_lang_dirs():
    langs = os.listdir('mclanguages/')
    lang_dirs = []
    for i in range(len(langs)):
        lang_dirs.append(f"mclanguages\{langs[i]}") #gets directories of all language files in a list
    return lang_dirs


#thanks again chatgpt (if theres bugs its the AIs fault)
def delete_non_shared_pairs(dictionaries):
    #gets rid of any language which shortcuts for one group but not another
    shared_keys = set.intersection(*[set(d.keys()) for d in dictionaries])

    for d in dictionaries:
        for key in list(d.keys()):
            if key not in shared_keys:
                del d[key] #key is a language

    i = 1
    for group in dictionaries: #group is success dictionary
        print(f"\n\nGroup: {i}\n")
        i += 1
        for key in group:
            good = group[key]
            print(f"{key}: {good}")

def search(item_dict):
    print(f"searching:\n{item_dict}\n")
    lang_dirs = get_lang_dirs()

    lang_dict_list = [] #each group has separate dict, all in this list
    for group in item_dict: #item_dict[group][i] for element of group list
        lang_dict = {} #new dictionary in format "English": ["bed", "wood"], etc
        for file in lang_dirs:
            with open(file, 'r') as j:
                try:
                    data = json.load(j)
                except:
                    pass
                language = data["language.name"]
                item_list = []
                for item in item_dict[group]: #item is a key, not value. eg, "minecraft:white_bed"
                    try:
                        item_list.append(data[item]) #item list will contain the value for that key
                    except: #error occurs when language doesnt have translation and defaults to english
                        with open('mclanguages\en_ca.json', 'r') as j:
                            data = json.load(j)
                            item_list.append(data[item])
                lang_dict[language] = item_list

        lang_dict_list.append(lang_dict)
    
    success_dict_list = []
    for group_dict in lang_dict_list: #group is a dict containing all the items in specified group in each language
        success_dict = {}
        for key in group_dict: #key is a language
            items = group_dict[key] #items will be list from group ["white bed", "respawn anchor"] in each language
            found = findseq(items) #found is a list of things to search for in current language (key)
            found = [elem for elem in found if elem != " "] #remove single spaces from list
            if found != []:
                success_dict[key] = found
        success_dict_list.append(success_dict) #index of list +1 should be group number

    delete_non_shared_pairs(success_dict_list)


"""
item_dict:
{"group 1": ["block:white_bed", "block:respawn_anchor"], "group 2": ["item:iron_ingot", "item:iron_axe"]}

lang_dict: 
{"English": ["white bed", "respawn anchor"], "French": ["blanche bed", "respawnereir anquioire"], "German": etc...}
{"English": ["iron ingot", "iron axe"], "French": ["ironer ingout", "ironer acquex"], "German": etc...}

lang_dict_list:
[{dict for group 1}, {dict for group 2}, etc...]

success_dict:
{"English": ["e"], "French": ["e"], "German": etc...}
{"English": ["substrings in both items"], "French": ["substrings in both items"], "German": etc...}

success_dict_list:
[{success dict for group 1}, {success dict for group 2}, etc...]
"""