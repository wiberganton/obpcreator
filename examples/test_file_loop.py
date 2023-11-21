import os
myPath = r"C:\Users\antwi87\Downloads\ref_design2024_AMHY"
outfile = ""
for f in os.listdir(myPath):
    file1 = open(myPath + "\\" + f, "r")
    content = file1.read()
    file1.close()
    outfile = outfile + "," + " \n " + content

out_file_path = myPath + r"\references.txt"
file1 = open(out_file_path, "w")
file1.write(outfile)
file1.close()

