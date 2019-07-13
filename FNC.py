#-------------------------------------------------------------------------------
# Name:        Context-Free Grammar to Normal-Chomsky Form (CFG to NCF)
# Purpose:     This script transforms a context-free grammar to Normal-Chomsky
#              form, according to the book 'Elements of Theory of Computation'
#              written by Lewis and Papadimitriou.
#
# Author:      Nikos Katirtzis (nikos912000)
#
# Created:     29/04/2014
# Modificaciones: Laura Sophia Gonzalez (laurasgm)
#                 Juan Pablo Amaya   
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

def replaceTerminalNode(rules, new_rules, noTerminal, terminal):
    new_rules[noTerminal] = terminal
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            rules[key][i] = values[i].replace(terminal, noTerminal)
    #print new_rules
    return rules, new_rules

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def short(rules,let,voc):
    #piscina de minusculas con la que comparemos ese simbolo no terminal
    minusculas=list(letters[:26])
    new_rules = {}
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key] #values nos contendra los valores de las reglas o new_dict 
        
        
        for i in range(len(values)):#i en el rango del numero de los values
            
            #for j in values[i]:#j va dentro del rango de cada una de las cadenas que contiene values 
                #print values[i]
            if len(values[i]) > 1:
                #print("hola")
                for k in values[i]:# ka va a recorrer la cadena 
                    if k in minusculas:# Si un caracter de la cadena es una minuscula, por ende es un simbolo no terminal
                    #print let[0]
                    #c[u] = let[0]
                        #print values[i]+" antes"
                        #values[i] = values[i].replace(k, let[0])#en la posicion i de los values reemplazamos esa k por l[0]
                        #print values[i]+" despues"
                        #w={k}#las minusculas repetidas
                        #x= set(let[0])#las claves a esas minusculas
                        
                        #for k in w:
                            #new = x.pop()
                            #values[i] = values[i].replace(k,new)
                            
                        n=k#guarmanos a k en n para no perderla
                        #minusculas.remove(k)#removemos a k de las minisculas
                        #print k
#                            voc.append(let[0])
                        new_key = let.pop(0)#copiamos el nuevo simbolo no terminal en new_key
                        
                        rules, new_rules = replaceTerminalNode(rules, new_rules, new_key, k)
                        new_dict = copy.deepcopy(rules)
                        #rules.setdefault(new_key, []).append(n)#creamos la nueva regla que nos contendra el simbolo terminal           
                
                        
#            rules[key][i] = values[i]
 #           let.remove(let[0])
    z = merge_two_dicts(rules, new_rules)
    return z,let,voc


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
    # Piscina de letras 
    #let me contiene la picina que usaremos para sacar las nuevas letras de los axiomas
    let = list(letters[26:]) + list(letters[:25])
    '''print letters[:26]
    abcdefghijklmnopqrstuvwxyz
    print letters[26:]
    ABCDEFGHIJKLMNOPQRSTUVWXYZ'''

    #quitamos la letra e, ya que es la letra que nos representa vacio
    let.remove('e')
    

    # Number of grammar rules
    #se hace el input de reglas y se verifica que sean mas de 2
    while True:
        userInput = raw_input('Give number of rules ')
        try:
            # check if N is integer >=2
            N = int(userInput)
            if N <=2: print 'N must be a number >=2!'
            else: break
        except ValueError:
            print "That's not an int!"

    # Initial state
    # Se hace el input del estado inicial y se verifica que sea solo una variable  
    while True:
        S = raw_input('Give initial state ')
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
    rules,let,voc = short(rules,let,voc)
    print_rules(rules)
    #print voc

if __name__ == '__main__':
    main()
