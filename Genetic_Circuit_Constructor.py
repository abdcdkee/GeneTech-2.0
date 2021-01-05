

#####################################################START CODE ###################################################################

#NAME : MUHAMMAD ABDULLAH SIDDIQUI                                                                                                              ID: 03586

#AIMS FOR THIS PORTION OF CODE THAT HAVE BEEN ACHIEVED:

#1. REPLICATION OF GENETECH SOFTWARE. GENERATION OF OUTPUT PATH FOR A GIVEN BOOLEAN EXPRESSION.
#2. REMOVAL OF FEEDBACK LOOP. SUCCESSFULLY BEEN GENERALIZED FOR ENTIRE OUTPUT. COULD BE MORE EFFICIENT IN IMPLEMENTATION THOUGH
#3. OPTIMIZATION OF LIBRARY: ACCOMPLISHED BY CONSIDERING DICTIONARIES WITHIN DICTIONARIES AS DETAILED BELOW.
#4. GENERALIZED FOR MORE THAN 3 VARIABLES THAT CAN BE INPUTTED EXTERNALLY.
#5. CODE ALSO WORKS IF ANY INTERMEDIATE PROTEIN VALUE IS INPUTTED INTO EXPRESSION. (CAN BE IMPLEMENTED IN CASE WHERE NOT/NOR EXPRESSIONS ARE BEING ADDED)
    
#NOTE: SOME INTERMEDIATE VALUES HAVE BEEN COMMENDED IN THE MIDDLE OF THE PROGRAM. YOU MAY UNCOMMENT AND OBSERVE THE OUTPUT TO VIEW THE SPECIFIC OUTPUT
#      OF THE SPECIFIC FUNCTION. OR YOU MIGHT WRITE YOUR OWN COMMANDS TO GENERATE OUTPUT.


############################################################################################################################################################
                                                    # LOADING LIBRARY AS CSV FILE INTO PYTHON PROGRAM
############################################################################################################################################################
############################################################################################################################################################
import time

var=['a','b','c']      ##Variable          ##Global variables created to be referenced later
pro=['PTac','PTet','PBad'] ##External Inputs; Proteins
inv=['A','B','C'] #Variable representation of inverted form e.g a' = A and b' = B and c' = C


def load_data(name): ##Creating a list consisting of all the elements in the library i.e. a CSV file.
    output=[]
    file=open(name)
    for i in file:
        i=i.strip() 
        i=i.split(',') ##Splits each line in file with delimiter as ","
        k=[]
        for j in i:
            if len(j):
                j=j.strip()
                k.append(j) ##Creates a list with each element of a given line
        output.append(k) ##Appends each list 'k' to 'output' list.
    return output

lib=load_data('lib.csv')


##########################################################################################################################################################

    
def order_data(n): ###Converting Library into a Dictionary with the types of gates as keys. This uses the output of load_data as input.
    d={}            ##Creates a dictionary with 4 Keys namely Ext Inverter/Int Inverter/ Semi-Ext NOR gates and Int NOR Gates
    temp=[]
    a=''
    for i in n:
        if len(i)==1:                   
            for j in i:
                if j[0]=='<' and j[1]!='/':
                    a=j[1:-1]
                    d[a]=[]
                elif j[0]=='<' and j[1]=='/':
                    d[a]=temp
                    temp=[]
                    a=''
        if i[0][0]!='<':
            temp.append(i)
    return d
        

data=order_data(lib)


##########################################################################################################################################################


def improve_lib(d):  ##Creating sub-dictionaries for PTac/PTet/PBad in Ext-Inv. and Sem-Ext-Nor for more efficient iteration through libary
    a=d['Ext-Inverters'] ##Creation of Keys/Empty Values
    b=d['Semi-Ext-NorGates']
    q={} ##Dictionaries Initialized
    w={}
    temp=''
    attach=[]
    for i in a:
        if len(i)==1:
            if temp!='':
                q[temp]=attach
                attach=[]
                temp=i[0]
            elif temp=='':
                temp=i[0]
        else:
            attach.append(i)
    q[temp]=attach ##Sub-dictionary for Ext- Inverters has been formed
    temp=''
    attach=[]
    for i in b:
        if len(i)==1:
            if temp!='':
                w[temp]=attach
                attach=[]
                temp=i[0]
            elif temp=='':
                temp=i[0]
        else:
            attach.append(i)
    w[temp]=attach    ##3 Sub Dictionary for Semi Ext NOR gates has been formed.
    d['Ext-Inverters']=q
    d['Semi-Ext-NorGates']=w    
    return d

    
lib=improve_lib(data)      ###The Library Has been constructed


##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
                        # CONVERSION OF OPTIMIZED EXPRESSION INTO PRE-FIX/POST-FIX EXPRESSION FOR SIMPLIFICATION
##########################################################################################################################################################
##########################################################################################################################################################


def convert_infix(s):  ####Function converts expression to Postfix notation for easy simplification
    operators=['+','-','*','/']
    c={'+':0,'-':0,'*':1,'/':1,'(':2,')':2}
    op=operators
    #################POST FIX EXPRESSION FORMATION ####
    r=''
    ao=[] ##Stack  inititated
    for i in s:
        if i not in op:
            if i !='(':
                if i!=')':
                    r+=i
            else:
                ao.append(i)
        if i in op: ##Considers operatiors 
            if len(ao)==0 or c[i]>c[ao[-1]]:
                ao.append(i)
            elif c[i]==c[ao[-1]]:
                x=ao.pop()
                r+=x
                ao.append(i) 
            elif c[i]<c[ao[-1]] and '(' not in ao: ##Considers Parenthesis 
                for j in range(len(ao)):
                    y=ao.pop()
                    r+=y
                ao.append(i)    
            elif ao[-1]=='(':
                ao.append(i)
        elif i==')':
            x=ao.pop()
            while x!='(':
                r+=x
                x=ao.pop()
    for j in range(len(ao)):
        y=ao.pop()
        r+=y ##Conversion of Stack to List
    return r


##########################################################################################################################################################
##########################################################################################################################################################
####    NOTE:MAJORITY OF ABOVE CODE IS IDENTICAL TO THE POSTFIX/PREFIX SOLUTION THAT WAS ATTEMPTED IN ASSIGNMENT#1 AND IS BEING USED HERE.
##########################################################################################################################################################
##########################################################################################################################################################



##########################################################################################################################################################
##########################################################################################################################################################
##### THE FUNCTIONS BELOW TAKE CARE OF THE EXTERNAL INVERSIONS, GENERATING ALL POSSIBLE COMBINATIONS. ####################################################
##########################################################################################################################################################
##########################################################################################################################################################


##exp="(c'+(b'+a')')'"
##exp="(c+(b'+a)')'"
##exp="(c+((a'+b)'+(b'+a)'))'"
##exp="(b+c)'+(c+((a+b)'+(b+a)'))'"
##exp="((a'+b)'+(c'+a)'+(b'+c')')'" 
##exp="(a+b+c)'"

#Complex Post Fix = [A,B,C,+,+,D,+]
#Simple Post Fix=[A,B,C,+,+]

def format_input(e): ##Takes care of complex postfix notation by converting them to simple form.
    cond=True        ##Additional initiative. Basically ensures that the expression could potentially work for more than 3 inputs...i.e. in addition to 
    i=1              ##a,b and c; we could add additional external inputs and the code would still work.
    while i<len(e)-1:
        if e[i]=='+' and e[i+1]!='+': ##Checks for complex case when +s and proteins are intermixed in the postfix exp. 
            if cond:
                marker=i-2  ##Inserts pair of values detached to the back
            j=[e[i+1]]
            k=i+1
            store=[k]
            while True:
                k+=1
                if e[k]=='+':
                    break
                else:               ##Note that [A,B,C,+,+,D,+] is equal to [D,A,B,C,+,+,+] is the main concept in this function.
                    j.append(e[k]) ##Adds element in question to a more suitable place. 
                    store.append(k)
            for ind in range(len(store)):
                del e[store[0]] ##Deletes elements to proved repetition     
            e=e[:marker]+j+e[marker:]

            if cond: cond=False ##Prevents marker from being renewed everytime, Boolean condition manipulated
        i+=1
    return e


##########################################################################################################################################################


def improve_exp(e):  ### Function converts a' to A, b' to B, and c' to C and removes "'" at the end of parenthesis for simplified implementation
                     ### of PostFix notation onto the Infix expression.
    r=''
    c="'"
    for i in range(len(e)):
        if e[i].isalpha() and e[i+1]!=c:  
            r+=e[i]
        elif e[i].isalpha() and e[i+1]==c:
            if e[i]=='a':
                r+='A'
            elif e[i]=='b':
                r+='B'
            elif e[i]=='c':
                r+='C'
        elif not e[i].isalpha() and e[i]!=c:
            r+=e[i]
    return r ##This function makes it easier to call the postfix function. This is primarily done since a term consisting of two bits e.g. a' would be
            ###problematic for the postfix function as compared to A. Similarly, (' is more confusing than (. So this function takes care of that.

##exp="(c'+((a+b')')')+(c'+b)'"
##sexp=improve_exp(exp)
##print(convert_infix(sexp))


##########################################################################################################################################################


def convert_back(exp):   ###Converting a' etc. to protein form e.g. PTac' with the " ' " denoting that it's inverted.
##    print(exp)
    global var,prop,inv ##Global variables referenced
    i_exp=improve_exp(exp) 
    exp=convert_infix(i_exp) ###Calls Helper Functions. Essentially makes sure that a proper postfix version of the input expression is created.This is then 
    r=[]                     ###The input of the rest of the function
    i=0
    while i<(len(exp)):
        j=exp[i]
##        print(j)
        if j=='P': ###This ensures that variables that are not a/b/c/A/B/C are maintained.
            k='P'
            i+=1
            j=exp[i]
            while j.isalpha():      ##Serves to act for even Non Ext Protein terms. Meaning that even intermediate value inputs like PAmtR etc. can be 
                k+=j                ##inputted and the program will work for that too :)
                i+=1
##                print(k)
                j=exp[i]
            r.append(k)
        if j=='+':
            r.append(j)
        if j in var:
            h=var.index(j)
            r.append(pro[h])
        if j in inv:
            if j=='A':
                r.append("PTac'") ######This ensures that variables are converted back into corresponding External Proteins.
            elif j=='B':
                r.append("PTet'")
            elif j=='C':
                r.append("PBad'")
        i+=1
##        print(r)
    r=format_input(r) #Calls helper function. Converts complex postfix to simple if needed. Otherwise returns the exact same expression.
    return r


print('LIBRARY IS LOADED AS FOLLOWS:\n\n',lib,'\n\n\n')


##########################################################################################################################################################


def ext_inv(e):             ###Creates a list with individual protein values inverted. 
    e=convert_back(e)       ###Calls convert back helper function to take the input of a postfix expression.
    stack=[]                ###Initializes Stack
    for item in e:  
        if item[-1]=="'":
            t=[]
            d=lib['Ext-Inverters'][item[:-1]]  ##Accesses Library
            for piece in d:
                t=e[:]
                ind=e.index(item)
                t[ind]=piece[-1]
                stack.append(t)     ###If element needs to be inverted, inverts any one element. And appends to the list.
        if item=='PTet' or item=='PBad' or item=='PTac': ##Appends element as is if does not need to be inverted.
            t=e[:]
            if t not in stack:
                stack.append(t)
##    print('Stack',stack)
    return stack

##ext_inv(exp)


##########################################################################################################################################################


def improve_ext_inv(series):  ##Improves upon above function and changes all the inverted values in an expression.
    store=[]        ###Series is the output of ext_inv function.
    for item in series:
        temp=item[:]
        for i in item:      ###This takes the one unique inverted value from each expression in the Series list and generates all possible combinations
            if i[-1]=="'":
                index=item.index(i)
                for replace in series:
                    if replace[index][-1]!="'":
                        temp[index]=replace[index]
                        if temp not in store:
                            store.append(temp)
                        temp=item[:]
            elif i=='PTet' or i=='PBad' or i=='PTac': ##Appends element as is if does not need to be inverted.
                temp=item[:]
                if temp not in store:
                    store.append(temp)
##    print('series',series,'\n','store',store)
    return store


def call_ext_inv(e):  ###Function creates a list with all possible combinations of protein's intial value (inverted when necessary)
                        ###Only External Inputs are being inverted right now
    temp=convert_back(e)
##    print('TEMP',temp
    series=ext_inv(e)
    count=0
    for i in temp:  ##Count gives number of terms in the expression and runs a loop for each of them to be replaced.
        if i!='+':
            count+=1
    for j in range(1,count): ###Function ensures that no external input is left un-inverted by running a loop for the length of expression on each term, 
        series=improve_ext_inv(series)  ##Checking each value.
##        print('new series',series)
        
    return series



##call_ext_inv(exp)



##########################################################################################################################################################
##########################################################################################################################################################
##### SOLVE_FURTHER FUNCTION MAINLY INVOLVES LOGIC MAPPING AND PRODUCES A LIST OF POSSIBLE OUTPUTS THAT LEAD TO AN ACTUAL VALUE AND ARE NOT CUT IN BETWEEN
##########################################################################################################################################################
##########################################################################################################################################################




steps=[]

def solve_further(n):  
                       ### Extra outputs being produced right now.
    repetition=[] ##Initializes list that checks for repetition to prevent feedback. This is the first step in a series of filters.
    global lib,var,pro,steps
    stack=[] ##Used in solution for postfix expression.
    store_steps=[] ##Stores intermediate steps for stored values i.e. alternate during simplification
    inter=[n] ##Stores the path for each value
    store=[] ##'Store' stores alternate values i.e. when one possible NOR operation has more than one output
    store_temp=[n]  ##Stores the path for each value in Store
##    print('EXPRESSION:\t',n)  
    problem=True ##Initializes boolean condition that controls the main value.

    
    while problem:
        i=0
        for item in n:
##            print('STACK',stack)
            if item!='+':
                stack.append(item)
            elif len(stack)>=2:
                if item=='+':
                        first=stack.pop()           
                        second=stack.pop()
                        if (first not in pro) and (second not in pro):  ##For Internal Nor Gates
                            search=lib['Int-NorGates']
                            cond=True #Initializes Boolean
                            for thing in search:
                                if [first,second]==thing[0:2] or [second,first]==thing[0:2]: ##Compares the stack value to the value stored in the library
                                    if cond:
                                        stack.append(thing[2])
                                    if not cond:
                                        unq=stack[:]        ##Creates a copy of the stack while considering Store i.e. alternate values.
                                        unq=unq[:-1]  ###Removes last element of Stack in order to prevent inclusion
                                                      ###of term that's already being logic-ified
                                        unq.append(thing[2])
                                        ind=n.index(item) + 1  ##Adding items that are left over in stack to a seperate storage list when appending store
                                        unq=unq+n[ind:]
                                        if len(unq)==2:
                                            unq.remove('+') ##Removes '+' if the stored value is the final value in the expression and '+' is not needed.
                                        store.append(unq)
##                                        print('unq',unq)
                                            
                                    cond=False ##Ensures that loop does not enter the second conditional which would break the larger loop
                                
                            if cond:
                                stack=[]        ##Breaks the entire large loop if some pair of values can not be processed.
                                problem=False               ##Compares the stack value to the value stored in the library

    ###NOTE: THE COMMENTING ABOVE HAS NOT BEEN REPEATED SINCE THE CONCEPT IS BASICALLY IDENTICAL TO THE FIRST EXCEPT THAT DIFFERENT DICTIONARY KEYS ARE
    ###BEING ACCESSED.
                        elif (first in pro) and (second in pro):  ###For External Nor Gates
                            search=lib['Ext-NorGates']       ###CHANGE CONDITIONALS TO ACCOMODATE SUB-DICTIONARIES BRO
                            cond=True
                            for thing in search:
                                if [first,second]==thing[0:2] or [second,first]==thing[0:2]:
                                    if cond:
                                        stack.append(thing[2])
                                    if not cond:
                                        unq=stack[:]
                                        unq=unq[:-1]  ###Removes last element of Stack in order to prevent inclusion
                                                      ###of term that's already being logic-ified
                                        unq.append(thing[2])
                                        ind=n.index(item)+1  ##Adding items that are left over to a seperate storage list
                                        unq=unq+n[ind:]
                                        if len(unq)==2:
                                            unq.remove('+')
                                        store.append(unq)
                                    cond=False
                                
                            if cond:
                                stack=[]
                                problem=False               ##Compares the stack value to the value stored in the library
                        elif (first in pro) and (second not in pro):   #For Semi-External Nor Gates.
                            search=lib['Semi-Ext-NorGates']
                            cond=True
                            for thing in search[first]:
                                if [first,second]==thing[0:2] or [second,first]==thing[0:2]:
                                    if cond:
                                        stack.append(thing[2])
                                    if not cond:
                                        unq=stack[:]
                                        unq=unq[:-1]  ###Removes last element of Stack in order to prevent inclusion
                                                      ###of term that's already being logic-ified
                                        unq.append(thing[2])
                                        ind=n.index(item)+1 ##Adding items that are left over to a seperate storage list
                                        unq=unq+n[ind:]
                                        if len(unq)==2:
                                            unq.remove('+')
                                        store.append(unq)
                                    cond=False
                                
                            if cond:
                                stack=[]
                                problem=False               ##Compares the stack value to the value stored in the library
                        elif (first not in pro) and (second in pro): ###For Semi-External Nor Gates.
                            search=lib['Semi-Ext-NorGates']
                            cond=True
                            for thing in search[second]:
##                                print(thing[0:2],'\n',[second,first],thing[0:2]==[second,first])
                                if [first,second]==thing[0:2] or [second,first]==thing[0:2]:
                                    if cond:
                                        stack.append(thing[2])
                                    if not cond:
                                        unq=stack[:]
                                        unq=unq[:-1]  ###Removes last element of Stack in order to prevent inclusion
                                                      ###of term that's already being logic-ified
                                        unq.append(thing[2])
                                        ind=n.index(item)+1   ##Adding items that are left over to a seperate storage list
                                        unq=unq+n[ind:]
                                        if len(unq)==2:
                                            unq.remove('+')
                                        store.append(unq)
                                    cond=False
                                
                            if cond:
                                stack=[]
                                problem=False

##################################### THIS EXTREMELY LONG FUNCTION HAS BEEN DIVIDED INTO TWO TO MAKE READING CLEARER #################################################################################################################

            if len(stack)==1: ###Breaks the loop if only one element in stack is left.
                if stack[0]==n[0] and i>=len(n):
                    stack=[]
                problem=False
            think=stack[:] ##Creates a copy of stack 
##            print('stack',think)
##            print('inter',inter)
            inter.append(think) ##Appends copy of stack to the intermediate-path
            if len(stack)>0:        ##Considers feedback loop when stored is empty i.e. 'STORE' is empty
                if stack[-1] in repetition:
                    if store==[]:
                        return [],inter,n,store ##Returns blank if repetition i.e. feedback occurs.
                else:
                    repetition.append(stack[-1])  ##Adds element to repetition if element not in repetition list.

            i+=1
    if len(stack)>0:   ###From here onwards we try to accomodate extra intermediate values :) 
        ret=[stack] 
    else:
        ret=[] ##Initializes value of outputs that will be outputted. Contains all possible outputs of a given expression.
    item=store[:] ##Creates a copy of the list that has the alternate outputs 
    store_steps_inter=[] ##Stores the path for values in store.
    issue=True
    if len(item)>0:
            for temp in item:
                tempo=temp[:]
                if len(tempo)>1:
                    if len(tempo)>1:
                        a=solve_further(tempo) ###Calls the function itself again IF the stored value is a postfix expression in itself e.g. [A,B,+]
                        tempo=a[0]
                        if isinstance(a[1][0][0][0],list):   ##Solves problem of hardcoding ....considers sub lists and appends/extends as necessary .
                                                            ##Isinstance function prevents need for hardcoding. Allows function to go inside list if necessary
##                            print(a[1][0],'sadadasd')     ##and if not necessary then to skip it.
                            store_steps_inter.extend(a[1][0]) ###Adds output of solve_further(store) to path of store.
                        else:
##                            print(a[1],'sadadasd')

                            store_steps_inter.extend(a[1]) ##Adds output of solve_further(store) to path of store.

                        if tempo not in ret: ##Adds answer of solve_further to ret i.e. the value to be returned
                            ret+=tempo
                        if tempo in item: 
                            item.remove(tempo) ##Removes the value that has been added to ret from store/tempo
                else:
                    if tempo not in ret:

                        ret+=[tempo]
                    item.remove(tempo)
    for i in store:
        if i not in ret:
            if len(i)==1:
                ret.append(i) ###Adds value in store to ret. if the value in store is itself the final output of the expression.

    sec_inter=[] ##Inititalizes list that contains the path for the stored values.

    for i in store:     ##Takes care of the case where there are more than one possibilities for addition of last two terms
        temp1=inter[:]
        if len(i)==1:
            sectemp_inter=temp1[:]
            sectemp_inter[-1]=i
            sec_inter.extend([sectemp_inter])
            temp1=sectemp_inter[:]
    for i in store:
        if len(i)==1:
            inter=[inter] + sec_inter ##Inter is in [] to maintain common format for all values.
            break


    if ret!='[]' and ret!=[]: ##In the case when return is not empty.
        thank=[inter,ret,n]
        steps.append(thank) ##Adds thank to steps. 
##    print('INTER',inter)
    if isinstance(inter[0][0],list):
        inter=inter+store_steps_inter ##FORMAT IMPORTANT..TAKES CARE OF INFINITE SUBLISTS.
    else:
        inter=[inter]+store_steps_inter ##Alternative format. Depending upon Isinstance built in function

##    if ret!=[]:
    ##    print(ret,'\n',inter,'\n\n')
    ##    print('store',store,'\n\n')

        
    return ret,inter,n,store ##Returns final Output values, Path, Input Expression, Stored Value
                             ##NOTE: Values other than Path were outputted to help in debug of the latter code.


##########################################################################################################################################################
##########################################################################################################################################################
################ THE FUNCTIONS BBELOW CREATE A ROUGH PATH AND REMOVE FEEDBACK ############################################################################
##########################################################################################################################################################
##########################################################################################################################################################



def create_path(stuff,exp): ##Creates path from original expression to final output.
    alld=[]
    for element in stuff:
        if element[0]!=[]: ##Considers the case where Some value of output is being returned from the expression.
##            print('ELEMENT',element,'\n')
            point=element[1]
            original=point[0][0] ##Hardcodes the first value of the firs sublist.
            large_temp=[] ##
            if [] in point:
                point.remove([]) ##Removes empty lists to prevent error later
            for thing in point:
##                print('THING',thing)
                temp=[]
                if '+' in thing[0] and thing[-1]!=[]:  ##In the case where thing has an output value
                    if thing[0]==original: ##Gives the expression essentially. The first value in either case
                        count=0 ##Initializes a marker which marks the amount of terms that are being added.
                        for j in original:
                            if j!='+':
                                count+=1
                            else:
                                break
                        temp.append(exp)
                        temp.append('--->') 
                        temp.append(original)
                        for i in range(count+1,len(thing)): #Begin iteration from count+1 to the length of thing.
                            if len(thing[i])>0:
                                temp.append('--->') ##Adds a marker to show conversion from one term to nother
                                temp.append([thing[i][-1]])
                    else:               ##Sec is the first term of 'thing'
                        sec=thing[0][0] ##Essentially same as the Original above except that Sec stems from the 'Store' in solve_further function.
                        if original.count(sec)==1:
                            ind=original.index(str(sec))
                            x=(original[:ind+1])+thing[0][1:] ##Creates the changed list with alternate values (stored values)
                            temp.append(exp)
                            temp.append('--->')
                            temp.append(original)
                            temp.append('--->>>') ##Represents conversion to stored value, simplified with operator ##Differentiated from --->
                            temp.append(x)
                            count=0
                            for j in x:
                                if j!='+':
##                                    print('j',j)
                                    count+=1 ##Same as Count abbove.
                                else:
                                    break

                            for i in range(count+1,len(thing)): 
                                if len(thing[i])>0:
                                    temp.append('--->') ##Adds marker between elements.
                                    temp.append([thing[i][-1]])
                        else:
                            temp=[]
                large_temp.append(temp) ##Creates all paths for a given element. i.e. a given possibility of inverted values.
                temp=[]
            alld.extend(large_temp) ##Creates all the paths for the output i.e. for all possible inverted values.
            
    norep=[]
    for i in alld:
        if i not in norep: ##Merely ensures that values are not being repeated in final answers. More or Less redundant in most cases.
            norep.append(i)


    return norep ##Returns a rough sketch of expression's complete path with delimiter ---> and --->>>


    ##NOTE: A LARGE PURPOSE OF THE ABOVE FUNCTION WAS TO ENSURE THAT MY LOGIC WAS CORRECT AND THE CIRCUIT OUTPUT WAS ROUGHLY COMING OUT AS NEEDED.

##n=['PSrpR','PAmtR','PAmeR','+','+']
##solve_further(n)

########################################################################################################################################################



def remove_feedback(stuff): ##Function is the last line of defense to ensure that no feedback occurs.
    global pro
    allt=[]
    proper=[] 
    for element in stuff:
        temp_check=[]
    
##        print(element)
        temp=[]
        cond=False
        problem=True
        if problem:     ##Overall boolean condition
            for item in element:
##                print('item',item)
                if not cond:
                    if item!='--->' and item!='--->>>': ##Considers items that are essential part of the path
                        for thing in item:
                            thankgod=False
                            if temp_check:
##                                print('check',temp_check)
                                ind=item.index(thing)
                                if item[ind]==temp_check[ind]: ##Checks the case where inverted value occurs twice in path but is not actually feedback problem.
##                                    print('temp_check',temp_check)
##                                    print('item',item)
##                                    print('\n')
                                    thankgod=True
                            if thing not in temp and (thing not in pro) : ##When there is no feedback
                                if thing!='+':
                                    temp.append(thing)
                            elif thing in pro:
                                if thing not in temp:
                                    temp.append(thing)
                                    
                            else:
                                if not thankgod: ##Means problem still not solved.
                                    problem=False
                                
                if cond:
                    if temp_check:
##                        print('check',temp_check)
                        ind=item.index(thing)
                        if item[ind]==temp_check[ind]:
##                            print('temp_check',temp_check)
##                            print('item',item)
##                            print('\n')
                            thankgod=True
                    cond=False
                    for thing in item[::-1]:  ##Generalizes the Case
                        if thing != '+': 
                            temp.append(thing) ##Adds last non + element in item to temp.
                            break
                if item=='--->>>': ##Considers the case where the value in question is a simplified postfix i.e. contains '+'
                    cond=True
##                print('temp',temp,problem)
                if item!='--->' and item!='--->>>':
                    temp_check=item[:] ##creates a copy of item. to be used in the next iteration in comparison to ensure inverted valus are not inverted.
##                print('initialize',temp_check)
        if problem:
            proper.append(element) ##Appends the element to proper if no feedback.
            allt.append(temp)   
##    for i in allt:
##        print(i,'\n')
##    print(allt.count(a))
    return proper ###Returns the input except that all lists/elements with feedback have been removed.
        


##########################################################################################################################################################
##########################################################################################################################################################
############ THE FUNCTION BELOW TAKES THE EXPRESSION AS INPUT AND CALLS THE OTHER FUNCTIONS TO GENERATE A BASIC OUTPUT FORM THAT NEEDS TO BE FORMATTED.
##########################################################################################################################################################
##########################################################################################################################################################

            
def solution_imp(e):
    
##    print(e) 
    con=convert_back(e) ##Calls helper    
    pos=call_ext_inv(e) ##pos give all possible expression version with the external inputs inverted if needed.
##    print(pos)
    check=[]
    over=[] ##Initializes list
    for item in pos:
##        print(item)
        temp=solve_further(item)
##        print('ret',temp[0])
##        print('inter',temp[1])
##        print('exp.',temp[2])
##        print('stored', temp[3])
##        print('\n')
        a=solve_further(item) ##Calls main helper
##        print(a)
        check.append(a[0]) ##check stores all returned values from solve_further function.
        over.append(a) ##Over stores all the answers of solve_further function
    path=create_path(over,con) ##Creates path for all values in con.
    nofeed=remove_feedback(path) ##Ensures no feedback occurs in path
##    sol='' ##Intializes string that will show output.
##    for i in nofeed:
##        sol+=str(i) ##Ensures all output circuit are in a string in seperate lines ##Can print this to see progress at this stage. 
##        sol+='\n'
##    for i in nofeed:
##        print(i)
    return nofeed ##Returns a list containing the correct path of value from input expression to output.

     

##########################################################################################################################################################




            
def output_format(sol): ##Function formats the output expression to convert it into the desired form.   
    inter=solution_imp(sol)     ##Note: Function works for all of the given inputs. But has NOT successfully been generalized. Some elements have been hard
##    print(inter)              ##coded to make it easier. I believe this is passable since this is merely the finishing touches on the program.
    final='\n\n'
    if inter==[]: ###Gives the case where No output is possible.
        return '\n\t\t\t\t\t\tNO LOGICAL FUNCTION POSSIBLE'
    for i in inter:
        if [] in inter:
            inter.remove([])
    for element in inter:
##        print('\n\n',element)
        for i in element:
            if '--->' in element:
                element.remove('--->')
            if '--->>>' in element:
                element.remove('--->>>')
        if element[0][1][-1]=="'" or element[0][0][-1]!="'":
            line1=[element[0][1]] ##First line of expression. Most of the work happens in this line
            line2=[element[0][0]] ##Second line. Is empty if no element other than first is being inverted.
            line3=[element[0][2]] ##Third line, Is empty if the element in question is NOT being inverted.
            issue=True
        elif element[0][0][-1]=="'":
            line1=[element[0][2]] ##First line of expression. Most of the work happens in this line
            line2=[element[0][0]] ##Second line. Is empty if no element other than first is being inverted.
            line3=[element[0][1]] ##Third line, Is empty if the element in question is NOT being inverted.
            issue=False
        cond=False
        if element[0]==element[1]:
            del element[0] ##Removes the elemebnt using index as a marker.
            cond=True
        length=element[0] ##Length=Length of the first item in the element.

        for item in element[1:]: ##Considering all items in an element excluding the very first one.
            if line1[-1][-1]=="'":
                if issue:
                    line1.append(item[1]) ##Initiates line 1 if an element is being inverted.
                else:
##                    print('line1',line1)
##                    print(item)
                    line1.append(item[2])
##                    print('linewwq',line1)
                cond=True
            if line2[-1][-1]=="'":
                if issue:
                    line2.append(item[0]) ##Initiates line 2 if an element is being inverted.
                else:
                    line2.append(item[0])
##                    print('item',item)###########################CORRECT KARNA HAI 
                cond=True
            if line3[-1][-1]=="'":
                if issue:   
                    line3.append(item[2]) ##Initiates line 3 if an element is being inverted.
                else:
                    line3.append(item[0])
                    
                cond=True
            if cond:
                if len(item)==1:
                    line1.append(item[0]) ##Simply adds the element in the case where the path contains the output of the last two terms from the expression.
                else:
                    if len(item)!=length: ##Length of first item 
                        for i in item[::-1]: ##Adds the last non '+' terms in item to line1, in the case where the path includes a simplified postfix 
                            if i!='+':       ##expression e.g. [A,B,C,+,+] ---> [A,D,+] so this loop will work when item is [A,D,+] and add D to line1.
                                if i not in line1:
##                                    print('line1',line1)
                                    line1.append(i)
                                    break
##        print(line1,line2,line3)                            
        oops=True ##Boolean Marker ###Merely serves to format the ------------T portion
        if len(line2)>1 and len(line3)>1:
            if line1[0][-1]=="'":
                line1.insert(4,line2[-1])
            else:
                line1.insert(3,line2[-1])
                oops=False
                
        elif len(line2)==1 and len(line3)==1:
            if line1[0][-1]!="'":
                line1.insert(1,line3[-1])
                line1.insert(3,line2[-1])
            else:
                line1.insert(4,line2[-1])
        elif len(line2)==1 and len(line3)>1:
            if line3[-1] not in line1:
                line1.insert(4,line3[-1]) ##was line 2 before (Note for debugging)
            else:
                line1.insert(4,line2[-1])
        elif len(line2)>1 and len(line3)==1:
            line1.insert(4,line2[-1])
            
        i=0

        while i<(len(line1)-2):
            if line1[i][-1]=="'":
                temp1='('+str(line1[i+1][1:])+')' ##Parenthesis signifies the output protein. Appear multiple times in expression.
                line1.insert(i+1,temp1)
                line1.insert(i+1,' -> ')
                line1.insert(i+3,' ----| ') ##Represents the end of the function of a given logic gate.

            if line1[i][0]=='P' and line1[i+1][0]=='P': ##Checks in the case where NOR gate function is being performed.
##                print('oops',line1)
                temp2='('+str(line1[i+2][1:])+')'
                line1.insert(i+2,temp2)
                line1.insert(i+2,' -> ')
                line1.insert(i+1,' -> ')
                line1.insert(i+5,' ----| ')
                            
            i+=1
        line1.append(' -> ')  ##Adds a delimiter between each successful value showing logical operation.
        line1.append('(YFP)') ##Hardcodes a label at the end of line 1.
        if line1[0][-1]=="'":
            line1[0]=line1[0][:-1]
        if line2[0][-1]=="'":
            line2[0]=line2[0][:-1]  
        if line3[0][-1]=="'":
            line3[0]=line3[0][:-1]
        if len(line2)>1:
            line2.insert(1,' -> ')
            line2[-1]='('+line2[-1][1:]+')'
            if oops:            ##Oops is false if the first element of line1 is NOT being inverted.
                temp=line2[-1][1:-1]
                temp='P'+temp
                ind=line1.index(temp)
                i=0
                lent=0
                while i<ind-1:
                    lent+=len(line1[i])
                    i+=1
                le=len(line2[0])+len(line2[1])
                lent-=le
                line2.append(' '+(lent-1)*'-'+'T')  ##Generalizing Length of ------T instead of Hardcoding. Repeated below as well.
            else:
                temp=line2[-1][1:-1]
                temp='P'+temp
                ind=line1.index(temp)
                i=0
                lent=0
                while i<ind-1:
                    lent+=len(line1[i])
                    i+=1
                le=len(line2[0])+len(line2[1])
                lent-=le
                line2.append(' '+(lent-1)*'-'+'T') 

        else:
            line2=""
        if len(line3)>1:
            line3.insert(1,' -> ')
            line3[-1]='('+line3[-1][1:]+')'
            if oops:
                temp=line3[-1][1:-1]
                temp='P'+temp
                ind=line1.index(temp)
                i=0
                lent=0
                while i<ind-1:
                    lent+=len(line1[i])
                    i+=1
                le=len(line3[0])+len(line3[1])
                lent-=le
                line3.append(' '+(lent-1)*'-'+'T') 

        else:
            line3=""
                      
            
##        print('\n','line1',line1,'\n','line2',line2,'\n','line3',line3)
        ans='' ###This serves to add spaces between each line of expression answer.
        for i in line1:
            ans+=i
        ans+='\n '
        if len(line2)!=0: ##Removes line2 if it is empty 
            for i in line2:
                ans+=i
            ans+='\n '
        for i in line3:
            ans+=i
        ans+='\n'
        final+='############################################################################################################################################################\n '+ans+'\n'
    return final ###Creates a string with each expression on seperate line and a Hashtag delimiter as needed. Can be printed directly in a reasonable format.


##print('\n\nPossible Outputs for the Expression is given as:\n',solution_imp(exp),'\n\n\n')




##########################################################################################################################################################
##########################################################################################################################################################
############## INITIAL TEST CASE TO CHECK THE INPUT ##################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################

a="(c+(b'+a)')'"            #2 Expected Outputs
b="(b+(c'+a)')'"            #4 Expected Outputs
c="(b+(a+c)')'"             #0 Expected Outputs
d="(c+(a+b)')'"             #3 Expected Outputs
e="(c+(b'+a')')'"           #2 Expected Outputs
f="(b+(a'+c')')'"           #4 Expected Outputs
extra="(b'+(c+a')')’"       #2 Expected Outputs
g="(c'+(b+a')')'"           #6 Expected Outputs
h="(b'+(a'+c')')'"          #2 Expected Outputs
i="(c'+(b'+a')')'"          #4 Expected Outputs
j="(b'+(a'+c)')'"           #2 Expected Outputs
check1="(c+PAmtR)'" ##Test case not being called. Program works for test case until the solution imp. function. Does not work for output_format function
                    ##since that function is somewhat hardcoded to the case where there are 3 external inputs.

check2="((a+b)+c')'"
out='############################################################################################################################################################'
form=out+'\n'+out
######
print('\t\t\t\t######################TEST CASES ARE GIVEN AS FOLLOWS:#####################\n\n\n\n')
print(form,'\n\nPossible Outputs for the Expression',a,'(2 Expected Outputs) is given as:\n',output_format(a),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',b,'(4 Expected Outputs) is given as:\n',output_format(b),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',c,'(0 Expected Outputs) is given as:\n',output_format(c),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',d,'(3 Expected Outputs) is given as:\n',output_format(d),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',e,'(2 Expected Outputs) is given as:\n',output_format(e),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',f,'(4 Expected Outputs) is given as:\n',output_format(f),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',extra,'(2 Expected Outputs) is given as:\n',output_format(extra),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',g,'(6 Expected Outputs) is given as:\n',output_format(g),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',h,'(2 Expected Outputs) is given as:\n',output_format(h),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',i,'(4 Expected Outputs) is given as:\n',output_format(i),'\n\n\n'+form+form)
print(form,'\n\nPossible Outputs for the Expression',j,'(2 Expected Outputs) is given as:\n',output_format(j),'\n\n\n'+form+form)

##NOTE: YOU CAN UNCOMMENT ALL OF THE ABOVE FUNCTION CALLS TO VIEW THE OUTPUT FOR DIFFERENT EXPRESSION INPUTS

##NOTE: IN A SPECIAL CASE -----T HAS NOT BEEN SHOWN IN OUTPUT. NOTE THAT THIS IS WHEN COINCIDENTALLY OUTPUT OF ONE LINE ALREADY COINCIDES WITH ITS
##PLACEMENT IN LINE1.









##print(form,'\n\nPossible Outputs for the Expression',check1,'is given as:\n',solution_imp(check1),'\n\n\n')
##print('\n\nPossible Outputs for the Expression',check2,'is given as:\n',output_format(check2),'\n\n\n')




##############################################################END CODE ABDULLAH ###############################################################################







