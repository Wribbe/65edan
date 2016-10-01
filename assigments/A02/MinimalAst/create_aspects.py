
def create_structure(aspect_name, list_objects, aspect_methods):

    lines = []

    lines.append("aspect {} {{".format(aspect_name))
    lines.append("public interface {} {{".format(aspect_name))

    for element in list_objects:
        format_string = "public Object visit({} node, Object data);"
        lines.append(format_string.format(element))

    lines.append("}")

    defult_visit_method = "return visitor.visit(this, data);"

    accept_objects = ["ASTNode"] + list_objects
    for element in accept_objects:
        format_string = "public Object {}.accept({} {}, Object data) {{"
        asp_lower = aspect_name.lower()
        lines.append(format_string.format(element, aspect_name, asp_lower))

        element_method = aspect_methods.get(element)
        if not element_method:
            element_method = defult_visit_method
        lines.append(element_method)

        lines.append("}")

    lines.append("}")

    return lines


def indent(list_lines):

    indentation_step = 4
    level = 0

    indented_lines = []

    for line in list_lines:

        if "}" in line:
            level -= 1

        indentation = indentation_step * level * ' '
        indented_line = "{}{}".format(indentation, line)
        indented_lines.append(indented_line)

        if "{" in line:
            level += 1

    return indented_lines


def main(args=[]):

    objects = [
            "Add",
            "Mul",
            "Div",
            "Minus",
            "Remainder",
            "FunctionDeclaration",
            "FunctionUse",
            "Assign",
            "Return",
            "LogicExpression",
            "IF",
            "WHILE",
            "ELSE",
            "NOEQ",
            "EQ",
            "LTEQ",
            "GTEQ",
            "LT",
            "GT",
            "IdExpression",
            "IdUse",
            "IdDeclare",
            "Numeral",
            ]

    aspect_methods = {
                "ASTNode": 'throw new Error("Visitor: ' +\
                           'accept method not available for " +'+\
                           ' getClass().getName());'
            }

    unindented_lines = create_structure("Visitor", objects, aspect_methods)
    indented_lines = indent(unindented_lines)

    print("\n".join(indented_lines))


if __name__ == "__main__":
    main()
