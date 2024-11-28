def add_exact_match_clause(query, column, value):
    return f"{query} AND {column} = '{value}'"

def add_starts_with_clause(query, column, value):
    return f"{query} AND {column} LIKE '{value}%'"

def add_ends_with_clause(query, column, value):
    return f"{query} AND {column} LIKE '%{value}'"

def add_between_clause(query, column, min_val, max_val):
    return f"{query} AND {column} BETWEEN {min_val} AND {max_val}"

    