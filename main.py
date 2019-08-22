# Based on Hive SQL Syntax 👍
# https://cwiki.apache.org/confluence/display/Hive/LanguageManual

from ply import lex
from ply import yacc
import re

reserved = {
    'select': 'SELECT',
    'all': 'ALL',
    'distinct': 'DISTINCT',
    'from': 'FROM',
    'where': 'WHERE',
    'by': 'BY',
    'group': 'GROUP',
    'order': 'ORDER',
    'cluster': 'CLUSTER',
    'distribute': 'DISTRIBUTE',
    'sort': 'SORT',
    'having': 'HAVING',
    'limit': 'LIMIT',
    'join': 'JOIN',
    'as': 'AS',
    'case': 'CASE',
    'when': 'WHEN',
    'then': 'THEN',
    'else': 'ELSE',
    'end': 'END',
    'or': 'OR',
    'and': 'AND',
    'not': 'NOT',
    'is': 'IS',
    'in': 'IN',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'coalesce': 'COALESCE',
    'cast': 'CAST',
    'concat': 'CONCAT',
    'union': 'UNION',
    'distinct': 'DISTINCT',
    'except': 'EXCEPT',
    'between': 'BETWEEN'
}

tokens = [
    'COMMENT',
    'COMMENT_ALONE',
    'COMMA',
    'COMPARISON',
    'STAR',
    'SYMBOL',
    'SEMICOLON',
    'LABEL',
    'LEFT_PAR',
    'RIGHT_PAR',
    'LEFT_BRA',
    'RIGHT_BRA',
    'STRING_SIMPLE',
    'STRING_DOUBLE',
    'STRING_GRAVE'
] + list(reserved.values())

t_COMMA = r','
t_COMPARISON = r'!?[=<>]+'
t_NOT = r'[!~]'
t_STAR = r'\*'
t_SYMBOL = r'[\%\&\+\-\/\^\|]'
t_SEMICOLON = r';'
t_LEFT_PAR = r'\('
t_RIGHT_PAR = r'\)'
t_LEFT_BRA = r'\['
t_RIGHT_BRA = r'\]'
t_STRING_SIMPLE = r'\'.*?\''
t_STRING_DOUBLE = r'\".*?\"'
t_STRING_GRAVE = r'\`.*?\`'

def t_LABEL(t):
     r'[a-zA-Z0-9$\{\}\_\.\:\@]+'
     t.type = reserved.get(t.value.lower(),'LABEL')        # Check for reserved words
     return t

def t_COMMENT_ALONE(t):
    r'(^|(?<=\n))[ \t]*--[^\n]*'
    return t

def t_COMMENT(t):
    r'--[^\n]*'
    return t

t_ignore = " \t\n"

def t_error(t):
    print(f"Illegal value '{t.value}'")
    t.lexer.skip(1)

lex.lex()

numeric_regex = re.compile(r'^[\s\d\n\t\.\+\-\*\/\^\%\&\|\(\)\=\<\>\!\~\,\$]*$')
is_numeric_expression = lambda x: numeric_regex.match(x)

def p_query_with_semicolon(p):
    'query : query SEMICOLON'
    p[0] = f"{p[1]}{p[2]}"

def p_query_select(p):
    'query : select_block'
    p[0] = p[1]

def p_query_more(p):
    'query : select_block additional_block_list'
    p[0] = f"{p[1]}\n{p[2]}"

def p_additional_block_list_next(p):
    'additional_block_list : additional_block additional_block_list'
    p[0] = f"{p[1]}\n{p[2]}"

def p_additional_block_list_end(p):
    'additional_block_list : additional_block'
    p[0] = p[1]

def p_additional_block(p):
    '''
    additional_block : where_block
                     | from_block
    '''
    p[0] = p[1]

def p_select_block(p):
    'select_block : select_keyword select_clause'
    p[2] = p[2].replace('\n','\n\t')
    p[0] = f"{p[1]}\n\t{p[2]}"

def p_where_block(p):
    'where_block : WHERE where_condition'
    p[0] = f"{p[1].upper()} {p[2]}"

def p_from_block(p):
    'from_block : FROM from_clause'
    p[0] = f"{p[1].upper()} {p[2]}"

# ============================================================

def p_from_clause(p):
    'from_clause : expr'
    if (p[1][0] != '(' or p[1][-1] != ')') and '\n' in p[1]:
        p[1] = p[1].replace('\n','\n\t')
    p[0] = p[1]

# ============================================================

def p_where_condition(p):
    'where_condition : expr'
    if (p[1][0] != '(' or p[1][-1] != ')') and '\n' in p[1]:
        p[1] = p[1].replace('\n','\n\t')
    p[0] = p[1]

# ============================================================

def p_select_keyword_alone(p):
    'select_keyword : SELECT'
    p[0] = p[1].upper()

def p_select_keyword_enriched(p):
    '''
    select_keyword : SELECT DISTINCT
                   | SELECT ALL
    '''
    p[0] = f"{p[1].upper()} {p[2].upper()}"

# ============================================================

def p_select_clause_next(p):
    'select_clause : expr COMMA select_clause'
    p[0] = f"{p[1]}{p[2]}\n{p[3]}"

def p_select_clause_end(p):
    'select_clause : expr'
    p[0] = p[1]

# ============================================================

def p_case_when(p):
    'case_when : CASE case_when_clause_list END'
    p[2] = p[2].replace('\n','\n\t')
    p[0] = f"{p[1].upper()}\n\t{p[2]}\n{p[3].upper()}"

def p_case_when_clause_list_next(p):
    'case_when_clause_list : case_when_clause case_when_clause_list'
    p[0] = f"{p[1]}\n{p[2]}"

def p_case_when_clause_list_end(p):
    'case_when_clause_list : case_when_clause'
    p[0] = p[1]

def p_case_when_clause_if(p):
    'case_when_clause : WHEN expr THEN expr'
    p[2] = p[2].replace('\n',' ').replace('\t','')
    p[0] = f"{p[1].upper()} {p[2]} {p[3].upper()} {p[4]}"

def p_case_when_clause_else(p):
    'case_when_clause : ELSE expr'
    p[0] = f"{p[1].upper()} {p[2]}"

# ============================================================

def p_expr(p):
    'expr : expr_definition_list'
    p[0] = p[1]

def p_expr_definition_list_next(p):
    'expr_definition_list : expr_definition expr_definition_list'
    if p[2][0] in ['(', '[']:
        p[0] = f"{p[1]}{p[2]}"
    else:
        p[0] = f"{p[1]} {p[2]}"

def p_expr_definition_list_end(p):
    'expr_definition_list : expr_definition'
    p[0] = p[1]

def p_expr_definition_list_prefix(p):
    'expr_definition_list : NOT expr_definition_list'
    if len(p[1]) == 1:
        p[0] = f"{p[1]}{p[2]}"
    else:
        p[0] = f"{p[1].upper()} {p[2]}"

def p_expr_definition_list_infix(p):
    '''
    expr_definition_list : expr_definition COMPARISON expr_definition_list
                         | expr_definition SYMBOL expr_definition_list
                         | expr_definition AS expr_definition_list
                         | expr_definition IS expr_definition_list
                         | expr_definition IN expr_definition_list
    '''
    p[0] = f"{p[1]} {p[2].upper()} {p[3]}"

def p_expr_definition_list_between(p):
    'expr_definition_list : BETWEEN expr_definition_list'
    p[2] = p[2].replace('\n',' ')
    p[0] = f"{p[1].upper()} {p[2]}"

def p_expr_definition_list_boolean(p):
    '''
    expr_definition_list : expr_definition AND expr_definition_list
                         | expr_definition OR expr_definition_list
    '''
    p[0] = f"{p[1]}\n{p[2].upper()} {p[3]}"

def p_expr_definition_value(p):
    '''
    expr_definition : LABEL
                    | STRING_SIMPLE
                    | STRING_DOUBLE
                    | STRING_GRAVE
    '''
    p[0] = p[1]

def p_expr_definition_keyword(p):
    '''
    expr_definition : DISTINCT
                    | ALL
                    | STAR
                    | NULL
                    | TRUE
                    | FALSE
                    | COALESCE
                    | CAST
                    | CONCAT
    '''
    p[0] = p[1].upper()

def p_expr_definition_block(p):
    '''
    expr_definition : case_when
                    | query
    '''
    p[0] = p[1]

def p_expr_definition_brackets(p):
    'expr_definition : LEFT_BRA expr_list RIGHT_BRA'
    p[0] = f"{p[1]}{p[2]}{p[3]}"

def p_expr_definition_parentheses(p):
    'expr_definition : LEFT_PAR expr_list RIGHT_PAR'
    if is_numeric_expression(p[2]):
        p[2] = p[2].replace('\n',' ')
        p[0] = f"{p[1]}{p[2]}{p[3]}"
    else:
        p[2] = p[2].replace('\n','\n\t')
        p[0] = f"{p[1]}\n\t{p[2]}\n{p[3]}"
        

def p_expr_list_next(p):
    'expr_list : expr_definition_list COMMA expr_list'
    p[0] = f"{p[1]}{p[2]}\n{p[3]}"

def p_expr_list_end(p):
    'expr_list : expr_definition_list'
    p[0] = p[1]

# ============================================================

def p_error(p):
    print("Syntax error at '%s'" % p.value)

yacc.yacc()

query = """
select distinct
 --a between 1 and 2,
  case when x != 0 then 1 else case when x > 0 then 2 else 3 end end as toto_le_zigoto
, 
(f.f1 + '-' + f.f2)
, f.id in (1 ,2 ,42),
'(' + 'oui' + '`@)' + @ + 1 + (1 * 1) "select" carapuce
, F.je_suis_un_champ_avec_un_${uuid}, coalesce(null,null,f.champ1, f.champ2), ma_function(hex(f.est_true, b.est_true))[ 0 ]
where (m = true or m = false) and m is null and ((1 != 0) or (m.is_false or case when 1=1 or 2=2 or case when 7=7 then ahah end then true else false end)) and o and i and j or a
where (m = true or m = false) and m is null and ((1 != 0) or (m.is_false or case when 1=1 or 2=2 or case when 7=7 then ahah end then true else false end)) and o and i and j or a
from (select aa from (select * from (select * from non where (1 is 1)))) where (1=1) AND 2=2
"""

query = """--oui
select * from a --non
--peut-être
"""

lex.input(query)
for tok in iter(lex.token, None):
    print(repr(tok.type), repr(tok.value))
print()
print(yacc.parse(query))