# DPLL SAT solver

This is a naive implementation of the DPLL algorithm for solving SAT problems. It accepts CNF formulas encoded in DIMACS format.
It is written by me in a course: Logic and Programme Verification.

## Usage

```shell
$ python solver.py path_of_file
```

For example, 

```shell
$ python solver.py test_cases\sat\1.cnf
```

The program will output 

```
$ s SATISFIABLE 
```

if the formula is sarisfiable or

```
$ s UNSATISFIABLE 
```

if not. Both Python 2 and Python 3 are supported. 

Due to the time constraint, I haven't had time to sanitize the input yet, so if the input file is not in valid DIMACS CNF format, or the arguments are if incorrect syntax, it will result in undefined behaviour.

## Data Structure

Two dictionaries are employed to store the formula. `Formula` is used to store the formula it self, with the elements being the clauses. For example, 

```
p cnf 3 3
1 -3 0
2 3 -1 0
2 0
```

is stored as

```
Formula = 
{
	1: [1,-3],
	2: [2,3,-1],
  	3: [2]
}
```

While `Var_clauses` is to store the id of the clauses which variables appear in. Continuing with the example above,

```
Var_clauses =
{
	1: [1,-2],
	2: [2,3],
  	3: [-1,2]
} 
```

Note that the minus indicates the *negation* of the variable appears in that clause. Using dictionaries, or hash maps, can result in constant time finding operations. 

## Algorithm

This program uses DFS(depth first search), with preprocessing to speed up the process.

The program in pseducode is:

```python
def dfs(Formula, Var_clauses):
    while true:
      BCP()
      set_pure_true()
      if nothing happened:
      	break
    if Formula is_sat():
    	return true
    elif Formula un_sat():
    	return false
    else:
    	x = choose_variable()
        new_formula1 = x_is_true()
        new_formula2 = x_is_false()
    return dfs(new_formula1) or dfs(new_formula2)
```

The valuation of variables is recorded by removing clauses and variables. If a clause is rendered satsifiable, then it is removed and the `Var_clause` hash map dealt with accordingly. If a variable is interpretated as false, then the variable is removed from the relevant clauses. So in this way, every time the search goes down a step, the own hash map is copied, making this implementation somewhat memory intensive.

The search stops when `Formula` is satisiable or unsatisfiable. `is_sat()` will return true if formula is empty. That is, 

```
Formula = 
{
}
```

While `un_sat()` will when `Formula` has empty elements. That is:

```
Formula = 
{
	blahblahblah...
	2: [],
  	3: blahblahblah
}
```

The `BCP()` function sets all the unit variables, clauses with only one element, to true. The `set_pure_true()` function sets all the pure literals, variables that are the same in every clause, all negations or all originals, to true. Right before the BCP function, `Formula` is searched for unit variables.  

## Benchmarks

In practice this program is useless.

| Size of Input / kB | Satisfiability | Time / s   |
| ------------------ | :------------- | ---------- |
| 3.3                | sat            | 0.06       |
| 5.28               | sat            | 2.9        |
| 12.9               | sat            | 19.4       |
| 35.9               | sat            | 3.1        |
| 881                | sat            | unsolvable |
| 2.51               | unsat          | 0.04       |
| 3.63               | unsat          | 3.2        |
| 5.31               | unsat          | 23.5       |
| 10.8               | unsat          | unsolvable |
| 44                 | unsat          | unsolvable |
