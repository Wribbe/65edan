#!/usr/bin/env python3

import os
import sys

sep = os.linesep


def emptyline(lines):
    lines.append("")


def create_class(dict_data):

    class_name = dict_data['class_name']
    inheritance = dict_data['inheritance']
    list_objects = dict_data['objects']
    methods_objects = dict_data['class_methods']
    class_functions = dict_data['class_functions']
    default_class_method = dict_data['default_class_method']
    state_variables = dict_data.get('state_variables', [])
    preamble = dict_data.get('preamble', [])
    object_type = dict_data.get('object_type', [])
    format_string = dict_data.get('format_string', "")

    lines = [] + preamble

    emptyline(lines)

    decleration_tokens = [
                          ' '.join(object_type),
                           class_name,
                          ' '.join(inheritance),
                          '{'
                         ]

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

        element_methods = methods_objects.get(element)
        if not element_methods:
            element_methods = default_class_method
        if not element_methods: # No default, don't print.
            continue

        if hasattr(element_methods, "strip"): # It's a plain string.
            element_methods = [element_methods] # repackage.

        for method in element_methods:
            current_format = format_string
            try:
                temp_format = method.get('function_format')
                current_format = temp_format
                body_text = method.get('body')
            except AttributeError:
                body_text = method

            # Append whole object function.
            lines.append(current_format.format(element))
            lines.append(body_text)
            lines.append("}")
            emptyline(lines)

    lines.append("}")

    return lines


def create_traversing_visitor(objects):

    class_name = "TraversingVisitor"
    object_type = ['public', 'abstract', 'class']
    inheritance = ['implements', 'lang.ast.Visitor']

    class_methods = {

            }

    class_functions = [
            "protected Object visitChildren(ASTNode node, Object data) {",
            "   for (int i = 0; i < node.getNumChild(); ++i) {",
            "       node.getChild(i).accept(this, data);",
            "   }",
            "   return data;",
            "}",
        ]

    default_class_method = "return visitChildren(node, data);"

    preamble = ['package lang;', 'import lang.ast.*;']

    format_string = "public Object visit({} node, Object data) {{"

    dict_data = {
            'class_name': class_name,
            'inheritance': inheritance,
            'objects': objects,
            'class_methods': class_methods,
            'class_functions': [line.strip() for line in class_functions],
            'default_class_method': default_class_method,
            'preamble': preamble,
            'object_type': object_type,
            'format_string': format_string,
            }

    unindented_class_lines = create_class(dict_data)

    class_lines = indent(unindented_class_lines)
    return sep.join(class_lines)


def create_msn_visitor(objects):

    class_name = "MsnVisitor"
    object_type = ['public', 'class']
    inheritance = ['extends', 'TraversingVisitor']

    increment_function = sep.join(["int givenDepth = (int) data;",
                                    "int myDepth = givenDepth+1;",
                                    "if (myDepth > maxDepth) {",
                                    "   maxDepth = myDepth;",
                                    "}",
                                    "return visitChildren(node, (Object)myDepth);",
                                   ])

    increment_types = [
                "FunctionDeclaration",
                "WHILE",
                "IF"
            ]

    class_methods = {
            "Program": "return visitChildren(node, 0);",
            }

    preamble = ['package lang;', 'import lang.ast.*;']

    increment_dict = {name : increment_function for name in increment_types}
    class_methods.update(increment_dict)

    class_functions = [
            "public static int result(ASTNode root) {",
            "   MsnVisitor visitor = new MsnVisitor();",
            "   root.accept(visitor, 0);",
            "   return visitor.maxDepth;",
            "}",
        ]

    #default_class_method = "return visitChildren(node, data);"
    default_class_method = ""

    state_variables = [
                'private int maxDepth = 0;'
            ]

    format_string = "public Object visit({} node, Object data) {{"

    dict_data = {
            'class_name': class_name,
            'inheritance': inheritance,
            'objects': objects,
            'class_methods': class_methods,
            'class_functions': [line.strip() for line in class_functions],
            'default_class_method': default_class_method,
            'state_variables': state_variables,
            'preamble': preamble,
            'object_type': object_type,
            'format_string': format_string,
            }

    unindented_class_lines = create_class(dict_data)

    class_lines = indent(unindented_class_lines)
    return sep.join(class_lines)


def create_visitor_aspect(objects):

    class_name = "Visitor"
    object_type = ['aspect']
    inheritance = []

    class_methods = {
            }

    preamble = ['import java.io.PrintStream;']

    class_method_lines = ["public interface Visitor {"]
    method_format = "public Object visit({} node, Object data);"
    for element in objects:
        class_method_lines.append(method_format.format(element))
    class_method_lines.append('}')

    class_functions = class_method_lines


    default_class_method = "return visitor.visit(this, data);"

    state_variables = [
            ]

    format_string = "public Object {}.accept(Visitor visitor, Object data) {{"

    dict_data = {
            'class_name': class_name,
            'inheritance': inheritance,
            'objects': objects,
            'class_methods': class_methods,
            'class_functions': [line.strip() for line in class_functions],
            'default_class_method': default_class_method,
            'state_variables': state_variables,
            'preamble': preamble,
            'object_type': object_type,
            'format_string': format_string,
            }

    unindented_class_lines = create_class(dict_data)

    class_lines = indent(unindented_class_lines)
    return sep.join(class_lines)


def create_pertty_print_aspect(objects):

    class_name = "Visitor"
    object_type = ['aspect']
    inheritance = []

    class_methods = {
            }

    preamble = ['import java.io.PrintStream;']

    class_method_lines = []
    class_functions = class_method_lines

    default_class_method = ""

    state_variables = [
            ]

    def binary_expression(operator):
        lines = []
        lines.append("getLeft().prettyPrint(out, indent);")
        lines.append("out.print(\" {} \");".format(operator))
        lines.append("getRight().prettyPrint(out, indent);")
        return sep.join(lines)

    binary_expressions = [
                ('Add', '+'),
                ('Mul', '*'),
                ('Div', '/'),
                ('Minus', '-'),
                ('Remainder', '%'),
            ]

    binary_methods = {name : binary_expression(operand) for (name, operand) in
            binary_expressions}

    class_methods.update(binary_methods)

    # Add ASTNode methods.
    astnode_methods = [
            sep.join(["prettyPrint(out, \"\");",
                                 "out.println();",]),
            { 'function_format': "public void {}.prettyPrint(PrintStream out) {{",
              'body': sep.join(["for (int i=0; i<getNumChild(); i++) {",
                                "   getChild(i).pertyPrint(out, indent);",
                                "}",])},
            ]

    class_methods.update({
            'ASTNode': astnode_methods
        })

    format_string = "public void {}.prettyPrint(PrintStream out, String indent) {{"

    dict_data = {
            'class_name': class_name,
            'inheritance': inheritance,
            'objects': objects,
            'class_methods': class_methods,
            'class_functions': [line.strip() for line in class_functions],
            'default_class_method': default_class_method,
            'state_variables': state_variables,
            'preamble': preamble,
            'object_type': object_type,
            'format_string': format_string,
            }

    unindented_class_lines = create_class(dict_data)

    class_lines = indent(unindented_class_lines)
    return sep.join(class_lines)


def indent(list_lines):

    text = sep.join(list_lines)
    list_lines = text.splitlines()

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
            "ASTNode",
            "Program",
            "List",
            "Opt",
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

    current_path = os.getcwd()

    visitor_jarg_tokens = ['src', 'jastadd', 'Visitor.jrag']
    prettyp_aspect_tokens = ['src', 'jastadd', 'PrettyPrint.jrag']
    visitor_class_tokens = ['src', 'java', 'lang', 'TraversingVisitor.java']
    msn_class_tokens = ['src', 'java', 'lang', 'MsnVisitor.java']

    # Aspects.
    jarg_path = os.path.join(*visitor_jarg_tokens)
    pretty_print_path = os.path.join(*prettyp_aspect_tokens)

    # Classes.
    class_path = os.path.join(*visitor_class_tokens)
    msn_class_path = os.path.join(*msn_class_tokens)

    file_objects = {
                jarg_path : create_visitor_aspect(objects),
                class_path : create_traversing_visitor(objects),
                msn_class_path: create_msn_visitor(objects),
                pretty_print_path: create_pertty_print_aspect(objects),
            }

    for path, data in file_objects.items():
        path = os.path.join(current_path, path)
        print("Printing data to: {}".format(path))
        with open(path, 'w') as file_handle:
            file_handle.write(data+sep)
        print("Done writing.")

if __name__ == "__main__":
    main(sys.argv[1:])
