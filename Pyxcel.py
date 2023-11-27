import re
# creating Pyxcel!

class Table: # our class for table!
    def __init__(self, a, b):
        self.matrix = [['None'] * int(a) for _ in range(int(b))]
        self.sig = int()
    def tableAssignment(self, str1, str2):
        str2 = fullEval(str2, self.matrix)
        x, y = bracketOrNot(str1, self.matrix)
        if str2 == 'unsupported operand':
            return 0
        if 0 <= x <= len(self.matrix) and 0 <= y <= len(self.matrix[0]):
            self.matrix[x][y] = str2
        else:
            return -1
    def variableAssignment(self, str1, str2):
        str2 = fullEval(str2, self.matrix)
        if str2 == 'unsupported operand':
            return 0
        var[str1] = str2
    def bracketAssignment(self, str1, str2, str3):
        str1 = fullEval(str1, self.matrix)
        str2 = fullEval(str2, self.matrix)
        str3 = fullEval(str3, self.matrix)
        if str3 == 'unsupported operand' or str3 == 'unsupported operand' or str3 == 'unsupported operand':
            return 0
        self.matrix[str2 - 1][cells(str1)] = str3
    def formula(self, str1, str2):
        a, b = bracketOrNot(str1, self.matrix)
        str2 = variableSweeper(str2, list(var.keys()), var)
        self.matrix[a][b] = str2
    def display(self):
        self.matrix2 = int2string(self.matrix)
        self.matrix2 = setFunc(self.matrix2)
        self.matrix2 = int2string(self.matrix2)
        for i in range(1, len(self.matrix2) + 1):
            self.matrix2[i - 1] = [str(i)] + self.matrix2[i - 1]
        lst = [str(0)]
        for i in range(len(self.matrix2[0])):
            lst.append(cells(str(i)))
        self.matrix2 = [lst] + self.matrix2
        lens = [max(map(len, col)) for col in zip(*self.matrix2)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in self.matrix2]
        print('\n'.join(table))
        # arr = self.matrix and we'll try to display it!
    def print(self, string): 
        self.matrix3 = int2string(self.matrix)
        self.matrix3 = setFunc(self.matrix3)
        self.matrix3 = int2string(self.matrix3)
        string = fullEval(string, self.matrix3)
        if string == 'unsupported operand':
            return 0
        print('out:' + str(string))
    def comparison(self, string):
        self.matrix2 = int2string(self.matrix)
        self.matrix2 = setFunc(self.matrix2)
        self.matrix2 = int2string(self.matrix2)
        return fullBoolEval(string, self.matrix2)
    
def fullBoolEval(boolean, matrix): # the main function for boolean eval!
    booleanSplit = re.split("\s*and\s*|\s*or\s*", boolean)
    booleanSigns = re.findall("or|and", boolean)
    lst = []
    ans = boolean1(lst, booleanSplit, booleanSigns, matrix)
    return ans

def setFunc(matrix): # function for setFunc order!
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if '+' in str(matrix[i][j]) or '-' in str(matrix[i][j]) or '*' in str(matrix[i][j]) or '/' in str(matrix[i][j]):
                matrix[i][j] = fullEval(str(matrix[i][j]), matrix)
    return matrix

def int2string(matrix): # used for converting the table elements to strings!
    arr = []
    temp = []
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix[0])):
            temp.append(str(matrix[i][j]))
        arr.append(temp)    
    return arr

def bracketOrNot(string, matrix): # used for bracket and alternative cell eval!
    a = re.findall("\[(.*)\]\[(.*)\]", string)
    b = re.findall("([A-Z]*)([0-9]*)", string) 
    if a:
        c = fullEval(a[0][0], matrix)
        d = fullEval(a[0][1], matrix)
        if c == 'unsupported operand' or d == 'unsupported operand':
            return 0
        c = cells(c)
        return d - 1, c
    else:
        a = cells(b[0][0])
        c = int(b[0][1])
    return c - 1, a

def analyseInput(string, our_dict, cntxt, arr): # the main function of the whole business!
    a = re.findall("create\((.*),(.*),(.*)\)", string)
    b = re.findall("context\((.*)\)", string)
    c = re.findall("([A-Z]+[0-9]+)\s*(=)\s*(.*)", string)
    d = re.findall("([a-z][^\s]*)\s*(=)\s*(.*)", string)
    e = re.findall("\[(.*)\]\[(.*)\]\s*(=)\s*(.*)", string)
    f = re.findall("setFunc\((.*),(.*)\)", string)
    g = re.findall("display\((.*)\)", string)
    h = re.findall("print\((.*)\)", string)
    i = re.findall("while\((.*)\){", string)
    k = re.findall("if\((.*)\){", string)
    if a:
        our_dict[a[0][0]] = Table(a[0][1], a[0][2])
    elif b:
        cntxt = b[0] 
    elif c:
        if cntxt not in our_dict.keys():
            return -1, 0 # error
        s = our_dict[cntxt].tableAssignment(c[0][0], c[0][2])
        if s == 0 or s == -1:
            return s, 0
    elif e:
        if cntxt not in our_dict.keys():
            return -1, 0 # error
        s = our_dict[cntxt].bracketAssignment(e[0][0], e[0][1], e[0][3])
        if s == 0 or s == -1:
            return s, 0
    elif f:
        if cntxt not in our_dict.keys():
            return -1, 0 # error
        s = our_dict[cntxt].formula(f[0][0], f[0][1])
        if s == 0 or s == -1:
            return s, 0
    elif g:
        s = our_dict[g[0]].display()
        if s == 0 or s == -1:
            return s, 0
    elif h:
        a = re.findall("[A-Z]+[0-9]+", h[0])
        b = re.findall("\[.*\]\[.*\]", h[0])
        if a or b:
            if cntxt not in our_dict.keys():
                return -1, 0 # error
            s = our_dict[cntxt].print(h[0])
            if s == 0 or s == -1:
                return s, 0
        else:
            s = fullEval(h[0], [])
            if s == 0 or s == -1:
                return s, 0
            print('out:' + str(s))
    elif i:
        lst = arr[0]
        x = 1
        my_arr = []
        while bracketBalance(lst) == -1:
            lst += arr[x]
            my_arr.append(arr[x])
            x += 1
        while fullBoolEval(i[0], our_dict[cntxt].matrix) == 1:
            z = 0
            while z < len(my_arr) - 1:
                string4 = re.sub("^\s*", '', my_arr[z])
                cntxt , k = analyseInput(string4, our_dict, cntxt, my_arr[z::])
                z += 1
                z += k
        return cntxt, len(my_arr)
    elif k:
        lst = arr[0]
        x = 1
        my_arr = []
        while bracketBalance(lst) == -1:
            lst += arr[x]
            my_arr.append(arr[x])
            x += 1
        if fullBoolEval(k[0], our_dict[cntxt].matrix) == 1:
            z = 0
            while z < len(my_arr) - 1:
                string4 = re.sub("^\s*", '', my_arr[z])
                cntxt , k = analyseInput(string4, our_dict, cntxt, my_arr[z::])
                z += 1
                z += k
        return cntxt, len(my_arr)
    elif d:
        if cntxt not in our_dict.keys():
            return -1, 0 # error
        s = our_dict[cntxt].variableAssignment(d[0][0], d[0][2])
        if s == 0 or s == -1:
            return s, 0

    return cntxt, 0

def lineByLine(n, our_dict = {}, cntxt = str(), i = 0): # used right before analyseInput()
    arr = []
    for _ in range(n):
        s = input()
        s = re.sub('\s*\$.*', '', s)
        arr.append(s)
    i = 0
    while i < n:
        cntxt, j = analyseInput(arr[i], our_dict, cntxt, arr[i::])
        i += 1
        i += j
        if cntxt == -1:
            print('Error')
            break
        elif cntxt == 0:
            print('unsupported operand')
            break

def bracketBalance(para): # used for finding the appropriate slices of arr
    a = 0                 # for while and if orders ! 
    b = 0
    x = 0
    y = 0
    ans = ""
    for i in range(len(para)):
        if para[i] == '{':
            x += 1
        elif para[i] == '}':
            y += 1
    if x == y:        
        for i in range(len(para)):
            if para[i] == '{':
                a += 1
            elif para[i] == '}':
                b += 1
            if b > a:
                ans = -1
                break
            else:
                ans = 1  
        return ans       
    else:
        return -1
        
def fullEval(string, matrix): # the main function for arithmetic eval!
    string = alternativeMatrixSweeper(string, matrix)
    string = variableSweeper(string, list(var.keys()), var)
    string = bracketEval(string, matrix)
    if 'None' in string:
        return 'None'
    if string == 1:
        return 'unsupported operand'
    else:
        string = multidivide([string] + [0], 0)
        error, string = calculation(string)
        if error == 1:
            return "unsupported operand"
        else:
            if type(string) == float:
                return int(string)
            elif type(string) == int:
                return int(string)
            else:
                return string

altCellPattern = re.compile(r"([A-Z]+)([0-9]+)")
def cells(our_string): # functon for interpretation of matrix columns! 
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    our_string = str(our_string)
    our_string = re.findall("[\w]+", our_string)
    our_string = our_string[0]
    sum = 0
    our_stringReverse = our_string[::-1]

    if our_string[0] in letters:
        for i in range(len(our_string)):
            if i == 0:
                sum += letters.index(our_stringReverse[i])
            else:
                sum += (letters.index(our_stringReverse[i]) + 1) * (26 ** i)
        return sum 

    else:
        num = int(float(our_string))
        remainder = []
        answer = str()

        if num > 0:
            while num >= 0:
                remainder.append(num % 26)
                num = num // 26 - 1
            for reverse in remainder[::-1]:
                answer = answer + letters[reverse]
        else:
            answer = 'A'
        return answer    

def variableSweeper(string, keys, dict): # gets rid of those nasty variables!
    stringSplit = re.split("\s*\+\s*|\s*\-\s*", string)
    signs = re.findall("[+-]", string) 
    for i in range(len(stringSplit)):
        for j in range(len(keys)):
            a = re.findall("[*/\[\]]", stringSplit[i])
            b = re.findall("\"", stringSplit[i])
            if a or not b:
                stringSplit[i] = re.sub(keys[j], str(dict[keys[j]]), stringSplit[i])
            else:
                pass
    string = str()        
    for i in range(len(signs)):
        string += stringSplit[i] + signs[i]
    string += stringSplit[-1]
    return string     

def alternativeMatrixSweeper(string, matrix): # just like variableSweeper() but for A1, A2, ...
    stringSplit = re.split("\s*\+\s*|\s*\-\s*", string)
    signs = re.findall("[+-]", string) 
    for i in range(len(stringSplit)):
        alt = altCellPattern.finditer(stringSplit[i])
        for pattern in alt:
            a = re.findall("[*/\[\]]", stringSplit[i])
            b = re.findall("\"", stringSplit[i])
            if a or not b:
                stringSplit[i] = re.sub(str(pattern.group()), str(matrixAccess(pattern.group(1), pattern.group(2), matrix)), str(stringSplit[i]))   
            else:
                pass
    string = str()        
    for i in range(len(signs)):
        string += stringSplit[i] + signs[i]
    string += stringSplit[-1]
    return string
    
def matrixAccess(a, b, matrix): # function for accessing matrix cells.
    a = str(a)
    a = cells(a)
    b = str(b)
    b = re.sub("[\"]", "", b)
    b = int(float(b))
    if b - 1 >= len(matrix):
        b -= 1
    if a >= len(matrix[0]):
        a -= 1
    return matrix[b - 1][a]

def bracketEval(string, matrix): # function for doing the tedious calculations inside the brackets.
    a = re.findall("\[[^\[\]]*\]\[[^\[\]]*\]", string)
    for i in range(len(a)):
        a[i] = re.sub("^\[", "", a[i])
        a[i] = re.sub("\]$", "", a[i])
        a_split = re.split("\]\[", a[i])
        new1 = multidivide(a_split, 0)
        new2 = multidivide(a_split, 1)
        new1 = calculation(new1)
        new2 = calculation(new2)
        if new1[0] == 1 or new2[0]:
            return 1 
        string = re.sub("\[[^\[\]]*\]\[[^\[\]]*\]", str(matrixAccess(new1[1], new2[1], matrix)), string, 1)
    return string

def multidivide(arr, i): # function used for calculating multipication and division.
    a = arr[i]
    if '/' not in a and '*' not in a:
        return a
    stringSplit = re.split("\s*\+\s*|\s*\-\s*", a)
    signs = re.findall("[+-]", a) 
    ans = []   
    for i in range(len(stringSplit)):
        if '*' not in stringSplit[i] and '/' not in stringSplit[i]:
            if type2(stringSplit[i]) == 4:
                ans.append(str(float(stringSplit[i])))
            else:
                ans.append(str(stringSplit[i]))    
        else:
            multsigns = re.findall("[*/]", stringSplit[i])
            multsplit = re.split("\s*[*/]\s*", stringSplit[i])
            for j in range(len(multsigns)):
                if multsigns[j] == '*':
                    multsplit[0] = float(multsplit[0]) 
                    multsplit[0] *= float(multsplit[1])
                    multsplit[0] = str(multsplit[0])
                    multsplit.pop(1)
                else:
                    multsplit[0] = float(multsplit[0]) 
                    multsplit[0] /= float(multsplit[1])
                    multsplit[0] = str(multsplit[0])
                    multsplit.pop(1)
            ans.append(multsplit[0])
        
    string = str()   
    for i in range(len(signs)):
        string += ans[i] + signs[i]   
    string += ans[-1]
    return string

def type2(string): # function for identifying the type of string: 1.Number 2.string 3.column name
    string = str(string)
    if string == "":
        return 10
    x = "\"" in string
    string = re.sub("[\"]", "", string)
    a = re.findall("[0-9|-]", string)
    b = re.findall("[^0-9\s*-/]", string)
    c = re.findall("[A-Z]", string)   
    d = re.findall("[^A-Z\s*/-]", string)
    if a and not b and not x:
        return 4
    elif c and not d:

        return 1
    else:
        return 0 

def calculation(string): # main function for doing the summation and subtraction of the strings.
    error = 0
    stringSplit = re.split("\s*\+\s*|\s*\-\s*", string) 
    signs = re.findall("[-+]", string)
    for i in range(len(signs)):
        if type2(stringSplit[0]) == 4 and type2(stringSplit[1]) == 4:
            if signs[i] == "+":
                stringSplit[0] = float(stringSplit[0]) + float(stringSplit[1])
            else:
                stringSplit[0] = float(stringSplit[0]) - float(stringSplit[1])

        elif type2(stringSplit[0]) == 4 and type2(stringSplit[1]) == 1:
            stringSplit[1] = re.sub("[\"]", "", stringSplit[1])
            if signs[i] == "+":
                stringSplit[0] = float(stringSplit[0]) + float(cells(stringSplit[1]))
            else:
                stringSplit[0] = float(stringSplit[0]) - float(cells(stringSplit[1]))

        elif type2(stringSplit[0]) == 1 and type2(stringSplit[1]) == 4:
            stringSplit[0] = re.sub("[\"]", "", stringSplit[0])
            if signs[i] == "+":
                stringSplit[0] = cells(cells(stringSplit[0]) + float(stringSplit[1]))
                stringSplit[0] = '"' + stringSplit[0] + '"' 
            else:
                stringSplit[0] = cells(cells(stringSplit[0]) - float(stringSplit[1]))
                stringSplit[0] = '"' + stringSplit[0] + '"' 

        elif type2(stringSplit[0]) == 1 and type2(stringSplit[1]) == 1:
            stringSplit[0] = re.sub("[\"]", "", stringSplit[0])
            stringSplit[1] = re.sub("[\"]", "", stringSplit[1])
            if signs[i] == "+":
                stringSplit[0] = stringSplit[0] + stringSplit[1]
                stringSplit[0] = '"' + stringSplit[0] + '"' 
            else:
                error = 1
                return error, stringSplit

        elif type2(stringSplit[0]) == 4 and type2(stringSplit[1]) == 0:
            stringSplit[1] = re.sub("[\"]", "", stringSplit[1])
            if signs[i] == "+":
                error = 1
                return error, stringSplit
            else:
                error = 1
                return error, stringSplit

        elif type2(stringSplit[0]) == 0 and type2(stringSplit[1]) == 4:
            stringSplit[0] = re.sub("[\"]", "", stringSplit[0])
            if signs[i] == "+":
                error = 1
                return error, stringSplit
            else:
                error = 1
                return error, stringSplit
            
        elif type2(stringSplit[0]) == 0 and type2(stringSplit[1]) == 0:
            stringSplit[0] = re.sub("[\"]", "", stringSplit[0])
            stringSplit[1] = re.sub("[\"]", "", stringSplit[1])
            if signs[i] == "+":
                stringSplit[0] = stringSplit[0] + stringSplit[1]
                stringSplit[0] = '"' + stringSplit[0] + '"' 
            else:
                error = 1
                return error, stringSplit
            
        elif type2(stringSplit[0]) == 0 and type2(stringSplit[1]) == 1:
            stringSplit[0] = re.sub("[\"]", "", stringSplit[0])
            stringSplit[1] = re.sub("[\"]", "", stringSplit[1])
            if signs[i] == "+":
                stringSplit[0] = stringSplit[0] + stringSplit[1]
                stringSplit[0] = '"' + stringSplit[0] + '"' 
            else:
                error = 1
                return error, stringSplit
          
        elif type2(stringSplit[0]) == 1 and type2(stringSplit[1]) == 0:
            stringSplit[0] = re.sub("[\"]", "", stringSplit[0])
            stringSplit[1] = re.sub("[\"]", "", stringSplit[1])
            if signs[i] == "+":
                stringSplit[0] = stringSplit[0] + stringSplit[1]
                stringSplit[0] = '"' + stringSplit[0] + '"' 
            else:
                error = 1
                return error, stringSplit
        stringSplit.pop(1)   
    else:
        if type2(stringSplit[0]) == 4:
            stringSplit[0] = float(stringSplit[0])
    return error, stringSplit[0]  

def comparison(string, matrix): # part of bool eval!
    stringSplit = re.split("\s*==\s*|\s*>\s*|\s*<\s*", string)
    comparisonSign = re.findall("==|>|<", string)
    if comparisonSign[0] == '==':
        error, s = comparison2(stringSplit,matrix)
        if error == 1:
            return -1
        elif error == 2:
            return -2 
        if s == 2:
            return 1           
        else: 
            return 0                
    elif comparisonSign[0] == '>':
        error, s = comparison2(stringSplit, matrix)
        if error == 1:
            return -1
        elif error == 2:
            return -2 
        if s == 1:
            return 1           
        else: 
            return 0                
    elif comparisonSign[0] == '<':
        error, s = comparison2(stringSplit, matrix)
        if error == 1:
            return -1
        elif error == 2:
            return -2
        if s == 3:
            return 1 
        else: 
            return 0                

def comparison2(arr, matrix): # part of bool eval!
    a = arr[0]
    b = arr[1]
    a = alternativeMatrixSweeper(a, matrix)
    a = variableSweeper(a, list(var.keys()), var)
    a = bracketEval(a, matrix)
    a = multidivide([a] + [0], 0)
    error1, a = calculation(a)
    b = alternativeMatrixSweeper(b, matrix)
    b = variableSweeper(b, list(var.keys()), var)
    b = bracketEval(b, matrix)
    b = multidivide([b] + [0], 0)
    error2, b = calculation(b)
    if error1 == 1 or error2 == 1:
        return 1
    if type2(a) == 4 or type2(b) == 4:
        if type2(a) == 4 and type2(b) == 4:
            if a == b:
                return 0, 2
            elif a > b:
                return 0, 1
            elif a < b:
                return 0, 3
        else:
            return 2, None
    else:
        if a == b:
            return 0, 2
        elif a > b:
            return 0, 1
        elif a < b:
            return 0, 3

def boolean1(lst, booleanSplit, booleanSigns, matrix): # part of the eval of bools!  
    for i in range(len(booleanSplit)):
        if booleanSplit[i] == 'true':
            lst.append(1)
        elif booleanSplit[i] == 'false':
            lst.append(0)
        else:
            ans = comparison(booleanSplit[i], matrix)
            if ans == -1:
                return -1
            elif ans == -2:
                return -2    
            lst.append(ans)
    for i in range(len(booleanSigns)):
        if booleanSigns[i] == 'or':
            if lst[0] == 1 or lst[1] == 1:
                lst[0] = 1
                lst.pop(1)
            else:
                lst[0] = 0
                lst.pop(1)              
        else: 
            if lst[0] == 1 and lst[1] == 1:
                lst[0] = 1
                lst.pop(1)
            else:
                lst[0] = 0
                lst.pop(1)     
    return lst[0]     

n = int(input())
our_dict = {}
cntxt = str()
var = {}
i = 0
lineByLine(n)

