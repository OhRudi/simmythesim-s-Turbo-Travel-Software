from glob import iglob

filenames = []
for file in iglob("ClientFullBuilds//*//*.package", recursive=True):
    filename = file.split("\\")[-1]
    filenames.append(filename)

def id(string):
    value = int(string.replace("ClientFullBuild", "").replace(".package", ""))
    number_of_digits = len(str(value))
    if value in range(0, 10):
        number_of_digits = 2
    if value in range(10, 99):
        number_of_digits = 3
    value += 10 **  (number_of_digits - 1)
    print(value, int(string.replace("ClientFullBuild", "").replace(".package", "")))
    print(string)

  #  print((int((str(value)[0])) + 1) + ((int(str(value)[1:])) * 1), value)
    return (int((str(value)[0])) + 1) + ((int(str(value)[1:])) * 1)
sorted_filenames = sorted(filenames, key=id)
print(sorted_filenames)