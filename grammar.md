lang -> expr+
expr -> assign_expr|if_expr|while_expr

assign_expr -> VAR ASSIGN_OP value_expr SEMICOLON
if_expr -> IF log_expr body ELSE body
while_expr -> WHILE log_expr body


log_expr -> OP value LOG_OP value CP
body -> OB expr+ CB
value_expr -> value (OP value)*
value -> VAR|DIGIT


VAR -> [a-zA-Z]+
DIGIT -> 0|([1-9][0-9]*)
ASSIGN_OP -> =
ARI_OP -> +|-|*|/
LOG_OP -> ==|!=|<|>
IF -> if
ELSE -> else
WHILE -> while
SEMICOLON -> ;
OP -> (
CP -> )
OB -> {
CB -> }