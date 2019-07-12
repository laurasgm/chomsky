#-------------------------------------------------------------------------------
# Name:        Context-Free Grammar to Normal-Chomsky Form (CFG to NCF)
# Purpose:     This script transforms a context-free grammar to Normal-Chomsky
#              form, according to the book 'Elements of Theory of Computation'
#              written by Lewis and Papadimitriou.
#
# Author:      Nikos Katirtzis (nikos912000)
#
# Created:     29/04/2014
#-------------------------------------------------------------------------------

from string import letters
import copy
import re

# Remove large rules (more than 2 states in the right part, eg. A->BCD)
def large(rules,let,voc):

    # Make a hard copy of the dictionary (as its size is changing over the
    # process)
    #copiamos las reglas una variable diferente en este caso new_dict
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key] #values nos contendra los valores de las llaves dentro de las reglas o new_dict
        print values
        #i se va a mover en vertical y j en horizontal 
        for i in range(len(values)):#i en el rango del numero de los values
            # Check if we have a rule violation
            
            if len(values[i]) > 2:  

                # A -> BCD gives 1) A-> BE (if E is the first "free"
                # letter from letters pool) and 2) E-> CD
                for j in range(0, len(values[i]) - 2): # j es de 0 hasta el numero de values -2 
                    # replace first rule
                    if j==0:
                        rules[key][i] = rules[key][i][0] + let[0] # es A en el ejemplo en la posicion de i osea baja verticalmente
                        print str(rules) + "  k"
                        #print let[0] + "  j"
                        

                        #A = B + E
                        #recordemos de rules es una lista de diccionario 
                        #las reglas en la posicion de la llave e i = a las reglas en la posicion 0 de esa llave + la letra de piscina 
                    # add new rules
                    '''else:
                        rules.setdefault(new_key, []).append(values[i][j] + let[0])
                        print values[i][j] + "d"
                        print let[0]'''

                    #print values[i][j] + "   h"
                    voc.append(let[0]) #guardamos la letra en el vocabulario
                    # save letter, as it'll be used in next rule
                    new_key = copy.deepcopy(let[0]) #guardamos la letra en new_key para ser usada y crear la regla
                    # remove letter from free letters list
                    let.remove(let[0])# borramos la letra de la piscina
                    #print values[i][-2:] + "   d" 
                # last 2 letters remain always the same
                rules.setdefault(new_key, []).append(values[i][-2:])
                #creamos la regla con new_key dandole los valores de las dos ultimas letras de la regla anterior
                # A -> BCD ______ E-> CD


    return rules,let,voc




def short_laura(rules,let,voc):
    minusculas=list(letters[:26])
    new_dict = copy.deepcopy(rules)
    cnt = 0
    n=''
    for key in new_dict:
        values = new_dict[key] #values nos contendra los valores de las reglas o new_dict 
        print values
        
        for i in range(len(values)):#i en el rango del numero de los values
            
            for j in values[i]:   
                #print(j)

                for k in j:
                    if k in minusculas:
                    #print let[0]
                    #c[u] = let[0]
                        print values[i]+" antes"
                        values[i] = values[i].replace(k, let[0])
                        print values[i]+" despues"
                        n=k
                        minusculas.remove(k)
                        print k
                        new_key = copy.deepcopy(let[0])
                        rules.setdefault(new_key, []).append(n)
                
                    #si es una minuscula entonces
                    #las reglas en la posicion de la key y verticalmente en el i 
                    #digale que la reemplace con una de la piscina 
                                
                voc.append(let[0])
                
                
            
            rules[key][i] = values[i]

            
            let.remove(let[0])
    
    return rules,let,voc


        
'''
# Remove empty rules (A->e)
def empty(rules,voc):

    # list with keys of empty rules
    e_list = []

    # find  non-terminal rules and add them in list
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            # if key gives an empty state and is not in list, add it
            if values[i] == 'e' and key not in e_list:
                e_list.append(key)
                # remove empty state
                rules[key].remove(values[i])
        # if key doesn't contain any values, remove it from dictionary
        if len(rules[key]) == 0:
            if key not in rules:
                voc.remove(key)
            rules.pop(key, None)

    # delete empty rules
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            # check for rules in the form A->BC or A->CB, where B is in e_list
            # and C in vocabulary
            if len(values[i]) == 2:
                # check for rule in the form A->BC, excluding the case that
                # gives A->A as a result)
                if values[i][0] in e_list and key!=values[i][1]:
                    rules.setdefault(key, []).append(values[i][1])
                # check for rule in the form A->CB, excluding the case that
                # gives A->A as a result)
                if values[i][1] in e_list and key!=values[i][0]:
                    if values[i][0]!=values[i][1]:
                        rules.setdefault(key, []).append(values[i][0])

    return rules,voc

# Remove short rules (A->B)
def short(rules,voc):

    # create a dictionary in the form letter:letter (at the beginning
    # D(A) = {A})
    D = dict(zip(voc, voc))

    # just transform value from string to list, to be able to insert more values
    for key in D:
        D[key] = list(D[key])

    # for every letter A of the vocabulary, if B->C, B in D(A) and C not in D(A)
    # add C in D(A)
    for letter in voc:
        for key in rules:
            if key in D[letter]:
                values = rules[key]
                for i in range(len(values)):
                    if len(values[i]) == 1 and values[i] not in D[letter]:
                        D.setdefault(letter, []).append(values[i])

    rules,D = short1(rules,D)
    return rules,D


def short1(rules,D):

    # remove short rules (with length in right side = 1)
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            if len(values[i]) == 1:
                rules[key].remove(values[i])
        if len(rules[key]) == 0: rules.pop(key, None)

    # replace each rule A->BC with A->B'C', where B' in D(B) and C' in D(C)
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            # search all possible B' in D(B)
            for j in D[values[i][0]]:
                # search all possible C' in D(C)
                for k in D[values[i][1]]:
                    # concatenate B' and C' and insert a new rule
                    if j+k not in values:
                        rules.setdefault(key, []).append(j + k)

    return rules,D


# Insert rules S->BC for every A->BC where A in D(S)-{S}
def final_rules(rules,D,S):

    for let in D[S]:
        # check if a key has no values
        if not rules[S] and not rules[let]:
            for v in rules[let]:
                if v not in rules[S]:
                    rules.setdefault(S, []).append(v)
    return rules
'''
# Print rules
def print_rules(rules):
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            print key + '->' + values[i]
    return 1


def main():

    rules = {} #reglas
    voc = [] # vocabulario
    # This list's going to be our "letters pool" for naming new states
    let = list(letters[26:]) + list(letters[:25])
    '''print letters[:26]
    abcdefghijklmnopqrstuvwxyz'''

    let.remove('e')
    #let me contiene la picina que usaremos para sacar las nuevas letras de los axiomas

    # Number of grammar rules
    while True:
        userInput = raw_input('Dame el numero de reglas')
        try:
            # check if N is integer >=2
            N = int(userInput)
            if N <=2: print 'N debe ser mayor a 2'
            else: break
        except ValueError:
            print "No es un entero"

    # Initial state
    while True:
        S = raw_input('Dame el estado inicial')
        #hacemos un match para verificar que solo haya metido un solo dato
        if not re.match("[a-zA-Z]*$", S): print 'Initial state must be a single \
character!'
        else:break

    print '+------------------------------------------------------+'
    print '|Give rules in the form A B (space-delimited), for A->B|'
    print '|or A BCD, if more than one states in the right part   |'
    print '|(without spaces between right part members).          |'
    print '+------------------------------------------------------+'

    for i in range(N):
        # A rule is actually in the form fr->to. However, user gives fr to.
        fr, to = map(str,raw_input('Rule #' + str(i + 1)).split()) 
        print str
        # Remove given letters from "letters pool"
        for l in fr:
            if l!='e' and l not in voc: voc.append(l)#si l no es vacio y l no esta en el vocabulario agreguela
            if l in let: let.remove(l)#remuevala de la picina 
        for l in to:
            if l!='e' and l not in voc: voc.append(l) 
            if l in let: let.remove(l)
        # Insert rule to dictionary
        rules.setdefault(fr, []).append(to) #agrega a las reglas fr concatenado de to 
        print rules
        #rules.setdefault ("hola",[]).append("perro")
        #{'hola': ['perro']}

    # remove large rules and print new rules
    print '\nRules after large rules removal'
    rules,let,voc = large(rules,let,voc)
    print_rules(rules)
    #print voc

    print '\nrterminales en nuevos axiomas'
    rules,let,voc = short_laura(rules,let,voc)
    print_rules(rules)
    #print voc

    '''
    # remove empty rules and print new rules
    print '\nRules after empty rules removal'
    rules,voc = empty(rules,voc)
    print_rules(rules)
    #print voc

    print '\nRules after short rules removal'
    rules,D = short(rules,voc)
    print_rules(rules)

    print '\nFinal rules'
    rules = final_rules(rules,D,S)
    print_rules(rules)'''

if __name__ == '__main__':
    main()
