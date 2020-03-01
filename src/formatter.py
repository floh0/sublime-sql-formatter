# Based on Hive SQL Syntax 👍
# https://cwiki.apache.org/confluence/display/Hive/LanguageManual

from .ply import yacc
from .ply import lex
import re

#              _   _                 
#   ___  _ __ | |_(_) ___  _ __  ___ 
#  / _ \| '_ \| __| |/ _ \| '_ \/ __|
# | (_) | |_) | |_| | (_) | | | \__ \
#  \___/| .__/ \__|_|\___/|_| |_|___/
#       |_|                          

options = {
    "tab": "\t",
    "newline": "\n",
    "newline_sep": "\n",
    "drop_comments": False    
}

#  _           _                      
# | |_   ___  | | __  ___  _ __   ___ 
# | __| / _ \ | |/ / / _ \| '_ \ / __|
# | |_ | (_) ||   < |  __/| | | |\__ \
#  \__| \___/ |_|\_\ \___||_| |_||___/

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
    'partition': 'PARTITION',
    'having': 'HAVING',
    'limit': 'LIMIT',
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
    'except': 'EXCEPT',
    'between': 'BETWEEN',
    'asc': 'ASC',
    'desc': 'DESC',
    'join': 'JOIN',
    'on': 'ON',
    'inner': 'INNER',
    'outer': 'OUTER',
    'left': 'LEFT',
    'right': 'RIGHT',
    'full': 'FULL',
    'semi': 'SEMI',
    'cross': 'CROSS',
    'natural': 'NATURAL',
    'with': 'WITH',
    'option': 'OPTION',
    'over': 'OVER'
}

tokens = [
    'COMMENT',
    'COMMENT_ALONE',
    'COMMA',
    'COMPARISON',
    'SYMBOL',
    'SEMICOLON',
    'POINT',
    'LABEL',
    'LEFT_PAR',
    'RIGHT_PAR',
    'LEFT_BRA',
    'RIGHT_BRA',
    'STRING_SIMPLE',
    'STRING_DOUBLE',
    'STRING_GRAVE',
    'TEMPLATE'
] + list(reserved.values())

t_COMMA = r','
t_COMPARISON = r'!?[=<>]+'
t_NOT = r'[!~]'
t_SYMBOL = r'[\*\%\&\+\-\/\^\|]'
t_SEMICOLON = r';'
t_POINT = r'\.'
t_LEFT_PAR = r'\('
t_RIGHT_PAR = r'\)'
t_LEFT_BRA = r'\['
t_RIGHT_BRA = r'\]'
t_STRING_SIMPLE = r'\'.*?\''
t_STRING_DOUBLE = r'\".*?\"'
t_STRING_GRAVE = r'\`.*?\`'
t_TEMPLATE = r'\#[a-zA-Z0-9$\{\}\_\:\@\(\)\[\]]+\#?'

def t_LABEL(t):
     r'[a-zA-Z0-9$\{\}\_\:\@]+'
     t.type = reserved.get(t.value.lower(),'LABEL')        # Check for reserved words
     return t

def t_COMMENT_ALONE(t):
    r'((^|(?<=\n))(?:\s*)--[^\n]*)|\s'
    if '--' in t.value:
        return t
    else:
        pass

def t_COMMENT(t):
    r'--[^\n]*'
    return t

def t_error(t):
    raise ValueError(t.lexpos)

#  _ __   ___   __ _   ___ __  __
# | '__| / _ \ / _` | / _ \\ \/ /
# | |   |  __/| (_| ||  __/ >  < 
# |_|    \___| \__, | \___|/_/\_\
#              |___/             

numeric_regex = re.compile(r'^[\s\d\.\+\-\*\/\^\%\&\|\(\)\=\<\>\!\~\,\$]*$')
is_numeric_expression = lambda x: numeric_regex.match(x)

empty_line_regex = re.compile(r'\n\s*\n')
spaces_start_regex = re.compile(r'^[ ]+', re.MULTILINE)
comments_regex = re.compile(r'--\s*')
comments_alone_regex = re.compile(r'^\s*--', re.MULTILINE)
remove_useless_whitespaces = lambda x: comments_alone_regex.sub('--', comments_regex.sub('-- ', spaces_start_regex.sub('', empty_line_regex.sub('\n', x)))).strip()

space_after_left_par_regex = re.compile(r'\( ')
space_before_right_par_regex = re.compile(r' \)')
sanitize_one_line_subquery = lambda x: space_after_left_par_regex.sub('(', space_before_right_par_regex.sub(')' ,x))

#   __ _  _ __   __ _  _ __ ___   _ __ ___    __ _  _ __ 
#  / _` || '__| / _` || '_ ` _ \ | '_ ` _ \  / _` || '__|
# | (_| || |   | (_| || | | | | || | | | | || (_| || |   
#  \__, ||_|    \__,_||_| |_| |_||_| |_| |_| \__,_||_|   
#  |___/                                                 

#   __                                 _    _              _                                    
#  / _|  ___   _ __  _ __ ___    __ _ | |_ | |_   ___   __| |    __ _  _   _   ___  _ __  _   _ 
# | |_  / _ \ | '__|| '_ ` _ \  / _` || __|| __| / _ \ / _` |   / _` || | | | / _ \| '__|| | | |
# |  _|| (_) || |   | | | | | || (_| || |_ | |_ |  __/| (_| |  | (_| || |_| ||  __/| |   | |_| |
# |_|   \___/ |_|   |_| |_| |_| \__,_| \__| \__| \___| \__,_|   \__, | \__,_| \___||_|    \__, |
#                                                                  |_|                    |___/ 

def p_formatted_query(p):
    'formatted_query : query'
    p[0] = remove_useless_whitespaces(p[1])

                                 
#   __ _  _   _   ___  _ __  _   _ 
#  / _` || | | | / _ \| '__|| | | |
# | (_| || |_| ||  __/| |   | |_| |
#  \__, | \__,_| \___||_|    \__, |
#     |_|                    |___/ 

def p_query(p):
    'query : subquerry'
    p[0] = p[1]

def p_query_with_semicolon(p):
    'query : query semicolon'
    p[0] = "%s%s" % (p[1], p[2])

def p_query_with_comment(p):
    'query : comment query'
    p[0] = "%s%s" % (p[1], p[2])

#              _                                            
#  ___  _   _ | |__    __ _  _   _   ___  _ __  _ __  _   _ 
# / __|| | | || '_ \  / _` || | | | / _ \| '__|| '__|| | | |
# \__ \| |_| || |_) || (_| || |_| ||  __/| |   | |   | |_| |
# |___/ \__,_||_.__/  \__, | \__,_| \___||_|   |_|    \__, |
#                        |_|                          |___/ 

def p_subquerry(p):
    'subquerry : expr_definition_list'
    p[0] = p[1]

#             _              _   
#  ___   ___ | |  ___   ___ | |_ 
# / __| / _ \| | / _ \ / __|| __|
# \__ \|  __/| ||  __/| (__ | |_ 
# |___/ \___||_| \___| \___| \__|
     
def p_select_full_select(p):
    'select_full : select_block'
    p[0] = p[1]

def p_select_full_combined(p):
    'select_full : select_full combine_keyword select_full'
    p[0] = "%s%s%s%s%s" % (p[1], options["newline_sep"], p[2], options["newline_sep"], p[3])

def p_select_full_parentheses(p):
    'select_full : left_par select_full right_par'
    p[2] = p[2].replace('\n','\n\t')
    p[0] = "%s%s%s%s%s%s" % (p[1], options["newline"], options["tab"], p[2], options["newline"], p[3])

def p_select_full_more(p):
    'select_full : select_block additional_block_list'
    p[0] = "%s%s%s" % (p[1], options["newline_sep"], p[2])

def p_select_block(p):
    'select_block : select_keyword select_clause'
    p[2] = p[2].replace('\n','\n\t')
    p[0] = "%s%s%s%s" % (p[1], options["newline_sep"], options["tab"], p[2])

def p_select_keyword_alone(p):
    'select_keyword : select'
    p[0] = p[1]

def p_select_keyword_enriched(p):
    '''
    select_keyword : select distinct
                   | select all
    '''
    p[0] = "%s %s" % (p[1], p[2])

def p_select_clause_next(p):
    'select_clause : expr comma select_clause'
    p[0] = "%s%s%s%s" % (p[1], p[2], options["newline"], p[3])

def p_select_clause_end(p):
    'select_clause : expr'
    p[0] = p[1]

#                                     _      _               _    
#   __ _  _   _   ___  _ __  _   _   | |__  | |  ___    ___ | | __
#  / _` || | | | / _ \| '__|| | | |  | '_ \ | | / _ \  / __|| |/ /
# | (_| || |_| ||  __/| |   | |_| |  | |_) || || (_) || (__ |   < 
#  \__, | \__,_| \___||_|    \__, |  |_.__/ |_| \___/  \___||_|\_\
#     |_|                    |___/                                

def p_additional_block_list_next(p):
    'additional_block_list : additional_block additional_block_list'
    p[0] = "%s%s%s" % (p[1], options["newline_sep"], p[2])

def p_additional_block_list_end(p):
    'additional_block_list : additional_block'
    p[0] = p[1]

def p_additional_block(p):
    '''
    additional_block : keyword_block
                     | by_block
                     | join_block
    '''
    p[0] = p[1]

def p_keyword_block(p):
    '''
    keyword_block : from clause
                  | where clause
                  | limit clause
                  | having clause
                  | option clause
    '''
    p[0] = "%s %s" % (p[1], p[2])

def p_by_block(p):
    '''
    by_block : group by clause
             | order by clause
             | cluster by clause
             | distribute by clause
             | sort by clause
             | partition by clause
    '''
    p[0] = "%s %s %s"  % (p[1], p[2], p[3])

def p_clause(p):
    'clause : expr_list'
    if p[1][0] != '(' and '\n' in p[1]:
        p[1] = p[1].replace('\n','\n\t')
    p[0] = p[1]

#                          _      _              
#   ___   ___   _ __ ___  | |__  (_) _ __    ___ 
#  / __| / _ \ | '_ ` _ \ | '_ \ | || '_ \  / _ \
# | (__ | (_) || | | | | || |_) || || | | ||  __/
#  \___| \___/ |_| |_| |_||_.__/ |_||_| |_| \___|
                                               
def p_combine_keyword_composed(p):
    '''
    combine_keyword : union all
                    | union distinct
    '''
    p[0] = "%s %s" % (p[1], p[2])

def p_combine_keyword_alone(p):
    '''
    combine_keyword : union
                    | except
    '''
    p[0] = p[1]

#    _         _        
#   (_)  ___  (_) _ __  
#   | | / _ \ | || '_ \ 
#   | || (_) || || | | |
#  _/ | \___/ |_||_| |_|
# |__/                  

def p_join_block_on(p):
    'join_block : join_expression clause on expr_list'
    p[4] = p[4].replace('\n','\n\t')
    p[0] = "%s %s%s%s%s %s" % (p[1], p[2], options["newline_sep"], options["tab"], p[3], p[4])

def p_join_block_alone(p):
    'join_block : join_expression clause'
    p[0] = "%s %s" % (p[1], p[2])

def p_join_expression(p):
    'join_expression : join_prefix_list join'
    p[0] = "%s %s" % (p[1], p[2])

def p_join_expression_alone(p):
    'join_expression : join'
    p[0] = p[1]

def p_join_prefix(p):
    '''
    join_prefix : inner
                | outer
                | left
                | right
                | full
                | semi
                | cross
                | natural
    '''
    p[0] = p[1]


def p_join_prefix_list_next(p):
    'join_prefix_list : join_prefix join_prefix_list'
    p[0] = "%s %s" % (p[1], p[2])

def p_join_prefix_list_end(p):
    'join_prefix_list : join_prefix'
    p[0] = p[1]

#                                      _                  
#   ___   __ _  ___   ___   __      __| |__    ___  _ __  
#  / __| / _` |/ __| / _ \  \ \ /\ / /| '_ \  / _ \| '_ \ 
# | (__ | (_| |\__ \|  __/   \ V  V / | | | ||  __/| | | |
#  \___| \__,_||___/ \___|    \_/\_/  |_| |_| \___||_| |_|
                                                        

def p_case_when(p):
    'case_when : case case_when_clause_list end'
    p[2] = p[2].replace('\n','\n\t')
    p[0] = "%s%s%s%s%s%s" % (p[1], options["newline_sep"], options["tab"], p[2], options["newline_sep"], p[3])

def p_case_when_clause_list_next(p):
    'case_when_clause_list : case_when_clause case_when_clause_list'
    p[0] = "%s%s%s" % (p[1], options["newline_sep"], p[2])

def p_case_when_clause_list_end(p):
    'case_when_clause_list : case_when_clause'
    p[0] = p[1]

def p_case_when_clause_if(p):
    'case_when_clause : when expr then expr'
    p[2] = p[2].replace('\n','\n\t')
    p[0] = "%s %s %s %s" % (p[1], p[2], p[3], p[4])

def p_case_when_clause_else(p):
    'case_when_clause : else expr'
    p[0] = "%s %s" % (p[1], p[2])

#   _____   _____ _ __ 
#  / _ \ \ / / _ \ '__|
# | (_) \ V /  __/ |   
#  \___/ \_/ \___|_|   

def p_over_block(p):
    'over_block : over left_par over_clause_list right_par'
    p[3] = p[3].replace('\n','\n\t')
    p[0] = "%s %s%s%s%s%s%s" % (p[1], p[2], options["newline"], options["tab"], p[3], options["newline"], p[4])

def p_over_clause_list_next(p):
    'over_clause_list : over_clause_list over_clause'
    p[0] = "%s%s%s" % (p[1], options["newline_sep"], p[2])

def p_over_clause_list_alone(p):
    'over_clause_list : over_clause'
    p[0] = p[1]

def p_over_clause(p):
    'over_clause : by_block'
    p[0] = p[1].replace('\t',' ').replace('\n','')

                     

#                                           _                  _  _       _   
#   ___ __  __ _ __   _ __   ___  ___  ___ (_)  ___   _ __    | |(_) ___ | |_ 
#  / _ \\ \/ /| '_ \ | '__| / _ \/ __|/ __|| | / _ \ | '_ \   | || |/ __|| __|
# |  __/ >  < | |_) || |   |  __/\__ \\__ \| || (_) || | | |  | || |\__ \| |_ 
#  \___|/_/\_\| .__/ |_|    \___||___/|___/|_| \___/ |_| |_|  |_||_||___/ \__|
#             |_|                                                             

def p_expr(p):
    'expr : expr_definition_list'
    p[0] = p[1]

def p_expr_definition_list_next(p):
    'expr_definition_list : expr_definition expr_definition_list'
    if p[2][0] in ['(', '['] or p[1] in ['+', '-']:
        p[0] = "%s%s" % (p[1], p[2])
    else:
        p[0] = "%s %s" % (p[1], p[2])

def p_expr_definition_list_point(p):
    'expr_definition_list : expr_definition point expr_definition_list'
    p[0] = "%s%s%s" % (p[1], p[2], p[3])

def p_expr_definition_list_end(p):
    'expr_definition_list : expr_definition'
    p[0] = p[1]

def p_expr_definition_list_prefix(p):
    'expr_definition_list : not expr_definition_list'
    if len(p[1]) == 1:
        p[0] = "%s%s" % (p[1], p[2])
    else:
        p[0] = "%s %s" % (p[1], p[2])

def p_expr_definition_list_infix(p):
    '''
    expr_definition_list : expr_definition comparison expr_definition_list
                         | expr_definition symbol expr_definition_list
                         | expr_definition as expr_definition_list
                         | expr_definition is expr_definition_list
                         | expr_definition in expr_definition_list
                         | expr_definition with expr_definition_list
    '''
    p[0] = "%s %s %s" % (p[1], p[2], p[3])

def p_expr_definition_list_between(p):
    'expr_definition_list : between expr_definition_list'
    p[2] = p[2].replace('\n',' ')
    p[0] = "%s %s" % (p[1], p[2])

#                                           _               
#   ___ __  __ _ __   _ __   ___  ___  ___ (_)  ___   _ __  
#  / _ \\ \/ /| '_ \ | '__| / _ \/ __|/ __|| | / _ \ | '_ \ 
# |  __/ >  < | |_) || |   |  __/\__ \\__ \| || (_) || | | |
#  \___|/_/\_\| .__/ |_|    \___||___/|___/|_| \___/ |_| |_|
#             |_|                                           

def p_expr_definition_list_boolean(p):
    '''
    expr_definition_list : expr_definition and expr_definition_list
                         | expr_definition or expr_definition_list
    '''
    p[0] = "%s%s%s %s" % (p[1], options["newline_sep"], p[2], p[3])

def p_expr_definition_value(p):
    '''
    expr_definition : label
                    | string_simple
                    | string_double
                    | string_grave
                    | template
    '''
    p[0] = p[1]

def p_expr_definition_keyword(p):
    '''
    expr_definition : distinct
                    | all
                    | null
                    | true
                    | false
                    | coalesce
                    | cast
                    | concat
                    | asc
                    | desc
                    | symbol
    '''
    p[0] = p[1]

def p_expr_definition_block(p):
    '''
    expr_definition : case_when
                    | select_full
                    | over_block
    '''
    p[0] = p[1]

def p_expr_definition_brackets(p):
    'expr_definition : left_bra expr_list right_bra'
    p[2] = sanitize_one_line_subquery(p[2].replace('\n',' ').replace('\t',''))
    p[0] = "%s%s%s" % (p[1], p[2], p[3])

def p_expr_definition_brackets_empty(p):
    'expr_definition : left_bra right_bra'
    p[0] = "%s%s" % (p[1], p[2])

def p_expr_definition_parentheses_unique(p):
    'expr_definition : left_par expr_definition_list right_par'
    if "\t" in p[2]:
        p[2] = p[2].replace('\n','\n\t')
        p[0] = "%s%s%s%s%s%s" % (p[1], options["newline"], options["tab"], p[2], options["newline"], p[3])
    else:
        p[2] = p[2].replace('\n',' ').replace('\t','')
        p[0] = "%s%s%s" % (p[1], p[2], p[3])

def p_expr_definition_parentheses(p):
    'expr_definition : left_par expr_list right_par'
    if is_numeric_expression(p[2]):
        p[2] = p[2].replace('\n',' ')
        p[0] = "%s%s%s" % (p[1], p[2], p[3])
    else:
        p[2] = p[2].replace('\n','\n\t')
        p[0] = "%s%s%s%s%s%s" % (p[1], options["newline"], options["tab"], p[2], options["newline"], p[3])

def p_expr_definition_parentheses_empty(p):
    'expr_definition : left_par right_par'
    p[0] = "%s%s" % (p[1], p[2])
        

def p_expr_list_next(p):
    'expr_list : expr_definition_list comma expr_list'
    p[0] = "%s%s%s%s" % (p[1], p[2], options["newline"], p[3])

def p_expr_list_end(p):
    'expr_list : expr_definition_list'
    p[0] = p[1]

#  _           _                                _                     
# | |_   ___  | | __  ___  _ __   ___     __ _ | |  ___   _ __    ___ 
# | __| / _ \ | |/ / / _ \| '_ \ / __|   / _` || | / _ \ | '_ \  / _ \
# | |_ | (_) ||   < |  __/| | | |\__ \  | (_| || || (_) || | | ||  __/
#  \__| \___/ |_|\_\ \___||_| |_||___/   \__,_||_| \___/ |_| |_| \___|
                                                                    
def p_token_to_upper(p):
    '''
    select : SELECT
    all : ALL
    distinct : DISTINCT
    from : FROM
    where : WHERE
    by : BY
    group : GROUP
    order : ORDER
    cluster : CLUSTER
    distribute : DISTRIBUTE
    sort : SORT
    partition : PARTITION
    having : HAVING
    limit : LIMIT
    as : AS
    case : CASE
    when : WHEN
    then : THEN
    else : ELSE
    end : END
    or : OR
    and : AND
    not : NOT
    is : IS
    in : IN
    true : TRUE
    false : FALSE
    null : NULL
    coalesce : COALESCE
    cast : CAST
    concat : CONCAT
    union : UNION
    except : EXCEPT
    between : BETWEEN
    asc : ASC
    desc : DESC
    join : JOIN
    on : ON
    inner : INNER
    outer : OUTER
    left : LEFT
    right : RIGHT
    full : FULL
    semi : SEMI
    cross : CROSS
    natural : NATURAL
    with : WITH
    option : OPTION
    over : OVER
    '''
    p[0] = p[1].upper()

def p_token_unchanged(p):
    '''
    comma : COMMA
    comparison : COMPARISON
    symbol : SYMBOL
    semicolon : SEMICOLON
    point : POINT
    label : LABEL
    left_par : LEFT_PAR
    right_par : RIGHT_PAR
    left_bra : LEFT_BRA
    right_bra : RIGHT_BRA
    string_simple : STRING_SIMPLE
    string_double : STRING_DOUBLE
    string_grave : STRING_GRAVE
    template : TEMPLATE
    '''
    p[0] = p[1]

def p_token_commented(p):
    '''
    select : select comment
    all : all comment
    distinct : distinct comment
    from : from comment
    where : where comment
    by : by comment
    group : group comment
    order : order comment
    cluster : cluster comment
    distribute : distribute comment
    sort : sort comment
    partition : partition comment
    having : having comment
    limit : limit comment
    as : as comment
    case : case comment
    when : when comment
    then : then comment
    else : else comment
    end : end comment
    or : or comment
    and : and comment
    not : not comment
    is : is comment
    in : in comment
    true : true comment
    false : false comment
    null : null comment
    coalesce : coalesce comment
    cast : cast comment
    concat : concat comment
    union : union comment
    except : except comment
    between : between comment
    asc : asc comment
    desc : desc comment
    join : join comment
    on : on comment
    inner : inner comment
    outer : outer comment
    left : left comment
    right : right comment
    full : full comment
    semi : semi comment
    cross : cross comment
    natural : natural comment
    with : with comment
    option : option comment
    over : over comment
    comma : comma comment
    comparison : comparison comment
    symbol : symbol comment
    semicolon : semicolon comment
    point : point comment
    label : label comment
    left_par : left_par comment
    right_par : right_par comment
    left_bra : left_bra comment
    right_bra : right_bra comment
    string_simple : string_simple comment
    string_double : string_double comment
    string_grave : string_grave comment
    template : template comment
    '''
    p[0] = "%s%s" % (p[1], p[2])

#                                                  _        
#   ___   ___   _ __ ___   _ __ ___    ___  _ __  | |_  ___ 
#  / __| / _ \ | '_ ` _ \ | '_ ` _ \  / _ \| '_ \ | __|/ __|
# | (__ | (_) || | | | | || | | | | ||  __/| | | || |_ \__ \
#  \___| \___/ |_| |_| |_||_| |_| |_| \___||_| |_| \__||___/
                                                          

def p_comment(p):
    'comment : COMMENT'
    if options["drop_comments"]:
        p[0] = ""
    else:
        p[0] = " %s\n" % p[1]

def p_comment_alone(p):
    'comment : COMMENT_ALONE'
    if options["drop_comments"]:
        p[0] = ""
    else:
        p[0] = "\n%s\n" % p[1]
   
#   ___  _ __  _ __   ___   _ __ 
#  / _ \| '__|| '__| / _ \ | '__|
# |  __/| |   | |   | (_) || |   
#  \___||_|   |_|    \___/ |_|

def p_error(p):
    raise SyntaxError(p.lexpos if p else -1)
    
lex.lex()
yacc.yacc()

def set_options(minify):
    if minify:
        options["tab"] = ""
        options["newline"] = ""
        options["newline_sep"] = " "
        options["drop_comments"] = True
    else:
        options["tab"] = "\t"
        options["newline"] = "\n"
        options["newline_sep"] = "\n"
        options["drop_comments"] = False

def format_query(query, minify=False):
    set_options(minify)
    return yacc.parse(query)