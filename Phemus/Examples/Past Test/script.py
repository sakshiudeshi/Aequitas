infile = open("Employee_Retraining_Dataset.csv", "r")
outfile = open("Employee_Retraining_Dataset_modified.csv", "w")
for i, line in enumerate(infile.readlines()):
  if i == 0: continue
  lineSplit = line.split(",")
  lineSplit[-1] = "-1"
  modline = ",".join(lineSplit)
  outfile.write(modline + "\n")

  