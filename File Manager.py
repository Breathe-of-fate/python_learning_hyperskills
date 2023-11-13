import os
import shutil

# run the user's program in our generated folders
os.chdir('module/root_folder')

# put your code here
def pwd():
    print(os.getcwd())
    
def cd(x):
    go, where = x.split()
    try:
        os.chdir(where)
        print(os.path.basename(os.getcwd()))
    except:
        print("Invalid command")
        
def ls(x):
    def the_size(x):
        in_kb, in_mb, in_gb = 1024, 1048576, 107374182
        if x < in_kb:
            in_what = "B"
        elif in_kb <= x < in_mb:
            in_what = "KB"
            x //= in_kb
        elif in_mb <= x < in_gb:
            in_what = "MB"
            x //= in_mb
        elif x >= in_gb:
            in_what = "GB"
            x //= in_gb
        return f"{x}{in_what}"
    
    all_folders = [i for i in os.listdir() if "." not in i]
    all_files = [i for i in os.listdir() if "." in i]
    ls_l = [(i, ) for i in all_folders] + list(zip(all_files, [str(os.stat(i).st_size) + "B" for i in all_files]))
    ls_lh = [(i, ) for i in all_folders] + list(zip(all_files, [the_size(os.stat(i).st_size) for i in all_files]))
    
    if x.startswith("ls"):
        if x.endswith("ls"):
            print(*all_folders + all_files, sep="\n")
        elif x.endswith(" -l"):
            print(*[" ".join(i) for i in ls_l], sep="\n")
        elif x.endswith(" -lh"):
            print(*[" ".join(i) for i in ls_lh], sep="\n")

def rm(x):
    if not x.endswith("rm"):
        command, where = x.split()
        if where.startswith("."):
            all_files = [i for i in os.listdir(os.getcwd()) if where in i]
            [os.remove(i) for i in all_files] if all_files else print(f"File extension {where} not found in this directory")            
        elif os.path.exists(where):
            if os.path.isfile(where):
                os.remove(where)
            else:
                shutil.rmtree(where)
        else:
            print("No such file or directory")
    else:
        print("Specify the file or directory")
        
def mv(x):
  if len(x.split()) == 3:
    what, where = x.split()[1:]
    if what.startswith('.'):
        all_files = [i for i in os.listdir(os.getcwd()) if what in i]
        if all_files:
            for i in all_files:
                if i in os.listdir(where):
                    while True:
                        answer = input(f"{i} already exists in this directory. Replace? (y/n)\n")
                        if answer == "y":
                            os.remove(where+"/"+i)
                            shutil.move(i, where)
                            break
                        elif answer == "n":
                            break
                        else:
                            continue
                else:
                    shutil.move(i, where)
        else:
            print(f"File extension {what} not found in this directory")
    
    elif os.path.isdir(where) and os.path.exists(os.path.normpath(where+"/"+what)):
      print("The file or directory already exists")
    elif not os.path.isdir(where) and os.path.exists(os.path.normpath(where)):
      print("The file or directory already exists")
    else:
      try:
        shutil.move(what, where)
      except FileNotFoundError:
        print("No such file or directory")
  elif len(x.split()) == 2:
      print("Specify the current name of the file or directory and the new name")
  else:
    print("Specify the current name of the file or directory and the new location and/or name")

def mkdir(x):
    if not x.endswith("mkdir"):
        command, where = x.split()
        if os.path.exists(where):
            print("The directory already exists")
        else:
            os.mkdir(where)
    else:
        print("Specify the name of the directory to be made")

def cp(x):
  pathes = x.split()
  if len(pathes) > 3:
    print("Specify the current name of the file or directory and the new name")
  elif len(pathes) < 3:
    print("Specify the file")
  else:
    what, where = pathes[1:]
    main_path, file_name = os.path.split(where)
    
    if what.startswith(".") and os.path.exists(os.path.realpath(main_path)):
        all_files = [i for i in os.listdir(os.getcwd()) if what in i]
        if all_files:
            for i in all_files:
                if i in os.listdir(where):
                    while True:
                        answer = input(f"{i} already exists in this directory. Replace? (y/n)\n")
                        if answer == "y":
                            shutil.copy2(i, where)
                            break
                        elif answer == "n":
                            break
                        else:
                            continue
                else:
                    shutil.copy2(i, where)
        else:
            print(f"File extension {what} not found in this directory")
    elif not os.path.exists(what) or not os.path.exists(os.path.realpath(main_path)):
      print("No such file or directory")
    elif os.path.exists(os.path.join(where, what)):
      print(what, "already exists in this directory")
    else:
      shutil.copy2(what, where)

print("Input the command:")
while True:
    user_choice = input()
    if user_choice == "pwd":
        pwd()
    elif user_choice.startswith("cd "):
        cd(user_choice)
    elif user_choice.startswith("ls"):
        ls(user_choice)
    elif user_choice.startswith("rm"):
        rm(user_choice)
    elif user_choice.startswith("mv"):
        mv(user_choice)
    elif user_choice.startswith("mkdir"):
        mkdir(user_choice)
    elif user_choice.startswith("cp"):
        cp(user_choice)
    elif user_choice == "quit":
        break
    else:
        print("Invalid command")