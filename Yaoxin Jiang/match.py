def match(fullname, initialname):
    full = fullname.split()
    initial = initialname.split()
    if initial[0] == full[0] and initial[1] == full[1][0]:
        return True
    return False


if match(fullProfName, initialProfName):
    name = fullProfName