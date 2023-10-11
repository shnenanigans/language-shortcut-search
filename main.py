from utils import *

print("Enter the items you would like to search for. When you are done, type \"done\"\n\nGROUP 1\n")
item_dict = {}
count = 1 #group count

def get_items(group):
    lst = []
    while True:
        item = input()
        if item == "done":
            item_dict[f"Group {group}"] = lst
            return
        else:
            try:
                x = check_item(item)
                lst.append(x) #x will be in the item in minecraft terms now, like "block.minecraft.white_bed"
            except Exception as e:
                print("invalid item. Make sure it is spelled correctly. Caps do not matter. No apostrophes.\n")
                print(e)
                pass


try:
    while True:
        get_items(count) #items[1] is group one, items[2] is group 2 etc...
        print("\nto search, type \"search\". To add another group, type \"add\"")
        user = input()
        if user == "search":
            search(item_dict)
            print("\n\nEnter the items you would like to search for. When you are done, type \"done\"\n\nGROUP 1\n")
            item_dict = {}
            count = 1 #group count
        if user == "add":
            count += 1
            print(f"\nGROUP {count}\n")
except Exception as e:
    print(e)


