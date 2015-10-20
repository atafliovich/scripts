#David Szeto

import os

for root, dirs, files in os.walk(os.getcwd()):
    if root[-2:] == "a2": #we only care about a2
        utorid = root.split("\\")[-2]
        filename = utorid + ".comments.david"        
        
        if filename not in files: #don't overwrite previous comments
            f = open(root + "\\" + filename, "w")
            
            if "cover.txt" not in files:
                f.write("Cover sheet not submitted. Not graded.")        
            else:
                #question 3
                f.write("Question 3)\n"
                        + "Pass.java:\n"
                        + "Grade: _/9\n"
                        + "Comments:\n"
                        + "\n"
                        )
                if "pass.py" not in files:
                    f.write("pass.py:\n"
                        + "Grade: 0/6\n"
                        + "Comments: pass.py not submitted\n"
                        + "\n"
                        )
                else:
                    f.write("pass.py:\n"
                        + "Grade: _/6\n"
                        + "Comments:\n"
                        + "\n"
                        )
                #question 4
                if "MakeId.java" not in files:
                    f.write("Question 4)\n"
                            + "Grade: 0/15\n"
                            + "Comments: MakeId.java not submitted.\n"
                            )
                else:
                    f.write("Question 4)\n"
                            + "Grade: _/15\n"
                            + "Comments: \n"
                            + "\n"
                            )
            f.close()
