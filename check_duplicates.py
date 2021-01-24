import os

list_of_songs = []
numbers_of_duplicates = 0

folder = ''
for _, dirs, _ in os.walk(folder):
    for dir_name in dirs:
        if dir_name[0:2].isdigit():
            for name in os.listdir(os.path.join(folder, dir_name)):
                if name not in list_of_songs:
                    list_of_songs.append(name)
                elif name in list_of_songs:
                    path_of_del_file = os.path.join(folder, dir_name, name)
                    print(os.path.abspath(path_of_del_file))
                    os.remove(path_of_del_file)
                    numbers_of_duplicates += 1


print(len(list_of_songs), list_of_songs)
print('number of duplicates: ', numbers_of_duplicates)
