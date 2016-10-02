#!/usr/bin/env python3

import os
import sys

sep = os.linesep


def emptyline(lines):
    lines.append("")


def create_aspect(aspect_name, list_objects, aspect_methods):

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


def create_class(dict_data):

    class_name = dict_data['class_name']
    inheritance = dict_data['inheritance']
    list_objects = dict_data['objects']
    methods_objects = dict_data['class_methods']
    abstract = dict_data['abstract']
    class_functions = dict_data['class_functions']
    default_class_method = dict_data['default_class_method']
    state_variables = dict_data.get('state_variables', [])

    lines = [
             'package lang;',
             'import lang.ast.*;',
            ]

    emptyline(lines)

    decleration_tokens = [
                          'public',
                          'abstract',
                          'class',
                           class_name,
                          ' '.join(inheritance),
                          '{'
                         ]

    if not abstract:
        del(decleration_tokens[1])

    class_declaration = ' '.join(decleration_tokens)

    lines.append(class_declaration)

    if class_functions:
        emptyline(lines)
        lines += class_functions

    if state_variables:
        emptyline(lines)
        lines.append('//state variables')
    for state_variable in state_variables:
        lines.append(state_variable)
    emptyline(lines)

    for element in list_objects:

        format_string = "public Object visit({} node, Object data) {{"

        element_method = methods_objects.get(element)
        if not element_method:
            element_method = default_class_method
        if not element_method: # No default, don't print.
            continue

        # Append whole object function.
        lines.append(format_string.format(element))
        lines.append(element_method)
        lines.append("}")
        emptyline(lines)

    lines.append("}")

    return lines


def create_traversing_visitor(objects):

    class_name = "TraversingVisitor"
    inheritance = ['implements', 'lang.ast.Visitor']
    abstract = True

    class_methods = {

            }

    class_functions = [
            "private Object visitChildren(ASTNode node, Object data) {",
            "   for (int i = 0; i < node.getNumChild(); ++i) {",
            "       node.getChild(i).accept(this, data);",
            "   }",
            "   return data;",
            "}",
        ]

    default_class_method = "return visitChildren(node, data);"

    dict_data = {
            'class_name': class_name,
            'inheritance': inheritance,
            'objects': objects,
            'class_methods': class_methods,
            'abstract': abstract,
            'class_functions': [line.strip() for line in class_functions],
            'default_class_method': default_class_method,
            }

    unindented_class_lines = create_class(dict_data)

    class_lines = indent(unindented_class_lines)
    return sep.join(class_lines)


def create_msn_visitor(objects):

    class_name = "MsnVisitor"
    inheritance = ['extends', 'TraversingVisitor']
    abstract = False

    class_methods = {

            }

    class_functions = [
            "private Object visitChildren(ASTNode node, Object data) {",
            "   for (int i = 0; i < node.getNumChild(); ++i) {",
            "       node.getChild(i).accept(this, data);",
            "   }",
            "   return data;",
            "}",
        ]

    default_class_method = "return visitChildren(node, data);"

    state_variables = [
                'private int maxDepth = 0;'
            ]

    dict_data = {
            'class_name': class_name,
            'inheritance': inheritance,
            'objects': objects,
            'class_methods': class_methods,
            'abstract': abstract,
            'class_functions': [line.strip() for line in class_functions],
            'default_class_method': default_class_method,
            'state_variables': state_variables,
            }

    unindented_class_lines = create_class(dict_data)

    class_lines = indent(unindented_class_lines)
    return sep.join(class_lines)


def indent(list_lines):

    indentation_step = 4
    level = 0

    indented_lines = []

    for line in list_lines:

        if "}" in line:
            level -= 1

        indentation = indentation_step * level * ' '
        indented_line = "{}{}".format(indentation, line)
        if not line.strip(): # Don't append only whitespace.
            indented_lines.append(indented_line.strip())
        else:
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

    def make_aspect():
        unindented_lines = create_aspect("Visitor", objects, aspect_methods)
        indented_lines = indent(unindented_lines)
        return sep.join(indented_lines)

    def make_classes():
        return [create_traversing_visitor(objects),
                create_msn_visitor(objects),
               ]

    if 'aspect' in args:
        print(make_aspect())
    elif 'class' in args:
        for class_data in make_classes():
            print(class_data)
    else:
        current_path = os.getcwd()

        visitor_jarg_tokens = ['src', 'jastadd', 'Visitor.jrag']
        visitor_class_tokens = ['src', 'java', 'lang', 'TraversingVisitor.java']
        msn_class_tokens = ['src', 'java', 'lang', 'MsnVisitor.java']

        jarg_path = os.path.join(*visitor_jarg_tokens)
        class_path = os.path.join(*visitor_class_tokens)
        msn_class_path = os.path.join(*msn_class_tokens)

        file_objects = {
                    jarg_path : make_aspect(),
                    class_path : create_traversing_visitor(objects),
                    msn_class_path: create_msn_visitor(objects),
                }

        for path, data in file_objects.items():
            path = os.path.join(current_path, path)
            print("Printing data to: {}".format(path))
            with open(path, 'w') as file_handle:
                file_handle.write(data+sep)
            print("Done writing.")

if __name__ == "__main__":
    main(sys.argv[1:])
