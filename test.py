def normalise(string):
    string = string.lower()
    string = string.replace(" ", "")
    string = string.replace("\t", "")
    return string

string = "asdfjkJKFLDSJ sajkj JKDFSJKF"
print(normalise(string))
