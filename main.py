import sys
import copy
import parse
import datetime
 
     

def main():
    begin = datetime.datetime.now()
    # import the filename from command line
    # TODO:add error detection
    filename = sys.argv[1]
    # parse the data input in CNF format
    # TODO: add sanitation
    formula, num_variables, num_clauses = parse.parse_file(filename)
    # [[1,2],[-1,-2],[3,5]...] NO ZEROS IN IT! NO EMPTY LISTS IN IT!(if there is, then unsat)
    
    # print (num_variables, num_clauses)
    
    # now we create the two hash maps:

    # the dictionary with all the formulas
    Formula = dict(zip(range(1,num_clauses+1), formula))
    
    # the dictionary with where every variable's whereabouts are recorded
    var_clause = [list() for i in range(1, num_variables+2)]
    j = 1
    for clause in formula:
        for variable in clause:
            if variable > 0:
                var_clause[abs(variable)] += [j]
            elif variable < 0:
                var_clause[-variable] += [-j]
        j =  j + 1
    Var_clause = dict(zip(range(1,num_variables+1), var_clause[1:]))
    

    def dfs(_Formula, _Var_clause):
        flagBCP = bool()
        flagPure = bool()
        _Unit_clause = set()

        def BCP():
            for i in _Formula:
                if len(_Formula[i]) == 1:
                    flagBCP = True
                    _Unit_clause.add(i)
                
            for clause_id in _Unit_clause:
               
                 # in case a empty one occurs.
                if _Formula.get(clause_id) == None:
                    continue
                if not _Formula[clause_id]:
                    return False
                    # prematurly ending the loop, as it is unsatisifable 
                var_name = _Formula[clause_id][0]
                del _Formula[clause_id]
               
                # when a clause is removed, the records in _Var_clause shall get removed as well. This activities occurs several times in the program               
                for clause in _Var_clause[abs(var_name)]:
                    if abs(clause) == clause_id:
                        continue
                    if clause * var_name < 0:
                        # if the interpretation of the variable (or its negation) is set to false, and the variable is removed from the clause
                        if _Formula.get(abs(clause)) != None:
                            _Formula[abs(clause)].remove(-var_name) 
                    elif clause * var_name > 0:
                        # if the clause is set to true
                        if _Formula.get(abs(clause)) != None:
                        # there's a chance of the clause getting prematurely removed...
                            for other_vars in _Formula[abs(clause)]:
                                if other_vars != var_name:
                                    if other_vars > 0:
                                        _Var_clause[abs(other_vars)].remove(abs(clause))
                                    elif other_vars < 0:
                                        _Var_clause[abs(other_vars)].remove(-abs(clause))
                            del _Formula[abs(clause)]
                if _Var_clause.get(abs(var_name)) != None:
                    del _Var_clause[abs(var_name)]
            _Unit_clause.clear()
            return True

        def set_pure():
        # set all the pure literals to true 
            pures = list()
            for var in _Var_clause:
                Flag = True
                for _cl in _Var_clause[var]:
                    if _cl * _Var_clause[var][0] < 0:
                        Flag = False
                        break
                if Flag:
                    flagPure = True
                    pures.append(var)

            for var in pures:
                for clause in _Var_clause[var]:
                    if _Formula.get(abs(clause)) != None:
                        for other_vars in _Formula[abs(clause)]:
                            if abs(other_vars) != var: #the abs here is very important!
                                if other_vars > 0:
                                    _Var_clause[abs(other_vars)].remove(abs(clause))
                                elif other_vars < 0:
                                    _Var_clause[abs(other_vars)].remove(-abs(clause))
                        del _Formula[abs(clause)]
                del _Var_clause[abs(var)]
        
        def isTrue():
            # if the _Formula is sat
            if not _Formula:
                return True
            return False
        
        def isFalse():
            # if the _Formula is unsat
            for _clause in _Formula:
                if len(_Formula[_clause]) == 0:
                    return True
            return False

        def longest_true(really_true):

            # we choose the variable that appears the most times
            def get_longest_var():
                _max = 0
                max_var = int()
                for _var in _Var_clause:
                
                    if len(_Var_clause[_var]) > _max:
                        max_var = _var
                        
                        _max = len(_Var_clause[_var])
                        
                return _max, max_var

            # deep copy here is very important! Python does not deep copy by default
            new_Formula = copy.deepcopy(_Formula)
            new_Var_clause = copy.deepcopy(_Var_clause)

            _max , max_var = get_longest_var()
            
            if _max == 0 or max_var == 0:
                if isTrue():
                    return True
                elif isFalse():
                    return False
            
            for _clause in new_Var_clause[max_var]:
                if _clause * really_true > 0:
                    # could remove?
                    if new_Formula.get(abs(_clause)) != None:
                        for other_vars in new_Formula[abs(_clause)]:
                            if other_vars != max_var * really_true:
                                if other_vars > 0:
                                    new_Var_clause[abs(other_vars)].remove(abs(_clause))
                                elif other_vars < 0:
                                    new_Var_clause[abs(other_vars)].remove(-abs(_clause))
                        del new_Formula[abs(_clause)]
                elif _clause * really_true < 0:
                    if new_Formula.get(abs(_clause)) != None:
                        new_Formula[abs(_clause)].remove(-really_true*max_var)
            del new_Var_clause[max_var]  
            ans = dfs(new_Formula, new_Var_clause)
            return ans

        # the real start of the program: BCP and set_pure loop!
        while True:
            flagPure = False
            flagBCP = False
            if BCP() == False:
            # to make it possible to halt if BCP encounters conflict
                return False
            set_pure()
            if(flagPure == False and flagBCP == False):
                break;

        if isTrue():
            return True
        elif isFalse():
            return False
        else:
            # find the var in max num of clauses. Could optimize?
            return longest_true(1) or longest_true(-1) 
    answer = dfs(Formula, Var_clause)
    if answer:
        print("s SATISFIABLE")
    else:
        print("s UNSATISFIABLE")

if __name__ == '__main__':
    main()