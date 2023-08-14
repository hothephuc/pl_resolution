
def pl_resolution(kb, query):
    clauses = kb.copy()

    temp = []
    for q in query:
        if isinstance(q, list):
            if q[0][0] == '-':
                temp.append([q[0][1:]])
            else:
                temp.append(["-" + q[0] ])
        elif q[0] == '-':
            temp.append(q[1:])
        else:
            temp.append("-" + q )
    if isinstance(temp[0], list):
        clauses.extend(temp)
    else:
        clauses.append(temp)
    loops = []
    while True:
        new_clauses = []

        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvents, flag = resolve(clauses[i], clauses[j])
                resolvents = remove_duplicates(resolvents)
                if(flag == True and resolvents == []):
                    new_clauses.append(resolvents)
                    new_clauses = remove_duplicates(new_clauses)
                    new_clauses = [clause for clause in new_clauses if clause not in clauses]
                    new_clauses = remove_complementary_literals(new_clauses)
                    clauses.extend(new_clauses)
                    
                    loops.append(remove_duplicates(new_clauses))
                    return clauses, loops
                resolvents = remove_complementary_literals(resolvents)
                new_clauses.extend(remove_duplicates(resolvents))
        new_clauses = remove_duplicates(new_clauses)
        new_clauses = [clause for clause in new_clauses if clause not in clauses]
        new_clauses = remove_complementary_literals(new_clauses)
        
        if all(c in clauses for c in new_clauses):
            break
        loops.append(remove_duplicates(new_clauses))
        clauses.extend(new_clauses)
        clauses = remove_duplicates(clauses)
    return [], loops

def resolve(c1, c2):
    c1 = list(c1)
    c2 = list(c2)
    resolvents = []
    flag = False
    for l1 in c1:
        if(l1[0] == '-'):
            root_l1 = l1[1:]
        else:
            root_l1 = l1
        for l2 in c2:
            if(l2[0] == '-'):
                root_l2 = l2[1:]
            else:
                root_l2 = l2
            if root_l1 == root_l2 and ((l1[0] == "-" and l2[0] != "-") or (l1[0] != "-" and l2[0] == "-")):
                flag =True
                my_set = c1.copy()  # Create a copy of c1 to preserve the original list
                my_set.extend(c2)    # Extend the list with elements from c2
                my_set.remove(l1)
                my_set.remove(l2)
                my_set = set(my_set)
                resolvent = list(my_set)
                if resolvent != []:
                    resolvents.append(resolvent)
    return resolvents, flag

def remove_duplicates(clauses):
    unique_clauses = []
    for clause in clauses:
        if clause not in unique_clauses:
            unique_clauses.append(clause)
    return unique_clauses

def contains_complementary_literals(literals):
    for literal in literals:
        if f"-{literal}" in literals:
            return True
    return False

def remove_complementary_literals(clauses):
    unique_clauses = []
    for clause in clauses:
        if not contains_complementary_literals(clause):
            unique_clauses.append(clause)
    return unique_clauses

def read_input_file(file_path):
    kb = []
    queries = []

    with open(file_path, 'r') as file:
        num_query_clauses = int(file.readline().strip())

        for _ in range(num_query_clauses):
            query_clause = file.readline().strip()
            if 'OR'in query_clause:
                temp_list = [[element] for element in query_clause.split(' OR ')]
                queries.append(temp_list)
            else:
                queries.append(query_clause.split(' OR '))

        num_kb_clauses = int(file.readline().strip())

        for _ in range(num_kb_clauses):
            kb_clause = file.readline().strip()
            kb.append(kb_clause.split(' OR '))

    return kb, queries

def format_clause(literals):
    return " OR ".join(literals)

def main():
    input_file = input("please input the path to input file:")
    output_file = input("please input the path to output file:")

    kb, queries = read_input_file(input_file)

    results = []
    loopsres = []
    for query in queries:
        result, loops = pl_resolution(kb, query)
        results.append(result)
        loopsres.extend(loops)
    
    
    conclusion = "YES" if all(results) else "NO"

    with open(output_file, 'w') as file:
        for resolution_clauses in loopsres:
            num_clauses = len(resolution_clauses)
            file.write(f"{num_clauses}\n")
            for clause in resolution_clauses:
                
                if clause != []:
                    clause_str = format_clause(sorted(clause))
                    file.write(f"{clause_str}\n")
                else:
                    file.write("{}\n")
        file.write(conclusion)

if __name__ == "__main__":
    main()
