import os
import string

folder = "Data/Bases"
for root, dirs, files in os.walk(folder):
    for file in files:
        with open(folder + "/" + file, "r+") as f:
            content = f.read()
            new_content = "".join([(x if x.isalnum()
                                         or x == "\n" or x.isspace()
                                         or x in string.punctuation
                                    else "") for x in content])
            print("différence :", not content == new_content)
            f.seek(0)
            f.write(new_content)
