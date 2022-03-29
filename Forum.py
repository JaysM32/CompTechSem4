import re

php = open("forum.php", "r")

#data processing / seperating
unprosdata = php.read()
#print(unprosdata)
perlinedata = unprosdata.split('\n')


#analysis
phpoptag = "<?php"
phpendtag = "?>"
classtag = "class"
functag = "function"
vartag = "\$"
lineendtag = "\;"
phpendtag = "?>"
mathtimes = "\*"
stringtag = r'"(.*?)"'
brackstart = "\{"
brackend = "\}"
numbers = r"\d+"
assigntag = '='
brackstart2 ="\("
brackend2 ="\)"
concate = "\."
printoutput = "echo"

stringstart = 0
stringend= 0

linecount = 0

for line in perlinedata:
    linecount+=1

    #print('---------------------------')
    #print('---------------------------')
    #print(line)
    #print('---------------------------')


    #php tag
    if line in phpoptag:
        print(f"{linecount},1,php-opening-tag")

    if line in phpendtag:
        print(f"{linecount},1,php-closing-tag")

    #class & function
    if re.search(classtag,line):
        found = re.search(classtag, line)
        print(f"{linecount},{found.start()+1},class")
        perworddata = line.split()
        if perworddata[0] == "class":
            name = re.sub(r'[^a-zA-Z]', '', perworddata[1])
            print(f"{linecount},{found.start() + 7},type-identifier,{name}")

    if re.search(functag,line):
        found = re.search(functag, line)
        print(f"{linecount},{found.start()+1},function")
        perworddata = line.split()
        if perworddata[0] == "function":
            name = re.sub(r'[^a-zA-Z]', '', perworddata[1])
            print(f"{linecount},{found.start() + 7},type-identifier,{name}")

    #brackets n curly
    if re.search(brackstart2, line):
        found = re.search(brackstart2, line)
        print(f"{linecount},{found.start() + 1},bracket-opening")

    if re.search(brackend2, line):
        found = re.search(brackend2, line)
        print(f"{linecount},{found.start() + 1},bracket-closing")

    if re.search(brackstart, line):
        found = re.search(brackstart, line)
        print(f"{linecount},{found.start()+1},curly-bracket-opening")

    if re.search(brackend,line):
        found = re.search(brackend, line)
        print(f"{linecount},{found.start()+1},curly-bracket-closing")

    #semicolon
    if re.search(lineendtag, line):
        found = re.search(lineendtag, line)
        print(f"{linecount},{found.start() + 1},semicolon")

    #concate
    if re.search(concate, line):
        found = re.search(concate, line)
        print(f"{linecount},{found.start() + 1},concate")


    #Strings
    if re.search(stringtag, line):
        found = re.search(stringtag, line)
        stringstart = found.start()
        stringend = found.end()
        print(f"{linecount},{found.start() + 1},String-literal,{re.findall(stringtag,line)}")


    #maths
    if re.search(mathtimes, line):
        found = re.search(mathtimes, line)
        print(f"{linecount},{found.start() + 1},math_times")

    # variables
    if re.finditer(vartag, line):
        for match in re.finditer(vartag, line):
            s = match.start()
            if (stringstart > s ) or (s > stringend):
                print(f"{linecount},{s + 1},variable")
                print(f"{linecount},{s + 2},type-identifier,{line[s + 1]}")

    # assign
    if re.search(assigntag, line):
        found = re.search(assigntag, line)
        if (stringstart > found.start()) or (found.start() > stringend):
            print(f"{linecount},{found.start() + 1},assign")

    #numbers
    if re.finditer(numbers,line):
        for match in re.finditer(numbers, line):
            s = match.start()
            print(f"{linecount},{s+1},number,{line[s]}")

    #echo
    if re.search(printoutput, line):
        found = re.search(printoutput, line)
        print(f"{linecount},{found.start() + 1},print-output")