#!/usr/bin/env python3

import os
import sys

sep = os.linesep

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


def create_class(class_name, implementations, list_objects, methods_objects):

    lines = [
             'package lang;',
             'import lang.ast.*;',
            ]

    decleration_tokens = [
                          'public',
                          'abstract',
                          'class',
                           class_name,
                          'implements',
                          ' '.join(implementations),
                          '{'
                         ]

    class_declaration = ' '.join(decleration_tokens)

    lines.append(class_declaration)


    private_method_lines = [
            "private Object visitChildren(ASTNode node, Object data) {",
            "for (int i = 0; i < node.getNumChild(); ++i) {",
            "node.getChild(i).accept(this, data);",
            "}",
            "return data;",
            "}",
        ]

    lines += private_method_lines

    default_class_method = "return visitChildren(node, data);"

    for element in list_objects:

        format_string = "public Object visit({} node, Object data) {{"
        lines.append(format_string.format(element))

        element_method = methods_objects.get(element)
        if not element_method:
            element_method = default_class_method
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

    def make_aspect():
        unindented_lines = create_aspect("Visitor", objects, aspect_methods)
        indented_lines = indent(unindented_lines)
        return sep.join(indented_lines)

    def make_class():
        unindented_class_lines = create_class("TraversingVisitor",
                                              ['lang.ast.Visitor'],
                                              objects,
                                              {})

        class_lines = indent(unindented_class_lines)
        return sep.join(class_lines)

    if 'aspect' in args:
        print(make_aspect())
    elif 'class' in args:
        print(make_class())
    else:
        current_path = os.getcwd()

        visitor_jarg_tokens = ['src', 'jastadd', 'Visitor.jarg']
        visitor_class_tokens = ['src', 'java', 'lang', 'TravelingVisitor.java']

        jarg_path = os.path.join(*visitor_jarg_tokens)
        class_path = os.path.join(*visitor_class_tokens)

        file_objects = {
                    jarg_path : make_aspect(),
                    class_path : make_class(),
                }

        for path, data in file_objects.items():
            path = os.path.join(current_path, path)
            print("Printing data to: {}".format(path))
            with open(path, 'w') as file_handle:
                file_handle.write(data+sep)
            print("Done writing.")

if __name__ == "__main__":
    main(sys.argv[1:])