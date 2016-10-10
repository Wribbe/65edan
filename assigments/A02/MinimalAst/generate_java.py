#!/usr/bin/env python3

import os
import sys

sep = os.linesep


def emptyline(lines):
    lines.append("")


def strip_text(text):

    if type(text) == list:
        text_lines = list
    else:
        text_lines = text.splitlines()
    return sep.join([line.strip() for line in text_lines])


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

    for element in sorted(list_objects):

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
            lines.append(strip_text(body_text))
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

    class_name = "PrettyPrint"
    object_type = ['aspect']
    inheritance = []

    class_methods = {
            }

    preamble = ['import java.io.PrintStream;']

    class_method_lines = []
    class_functions = class_method_lines

    fmt_defult_class = "out.print(\"{}\");"
    default_class_method = ""
    class_methods = {element : fmt_defult_class.format(element) for
                     element in objects}

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

    format_string = "public void {}.prettyPrint(PrintStream out, String indent) {{"

    def iter_over(length_method):
        return "for (int i=0; i<{}; i++) {{".format(length_method)

    child_loop = iter_over("getNumChild()")

    # Add ASTNode methods.
    diff_ast_func = "public void {}.prettyPrint(PrintStream out) {{"
    astnode_methods = [

            { 'function_format': diff_ast_func,
              'body': sep.join(["prettyPrint(out, \"\");",
                                "out.println();",])},

            sep.join([child_loop,
                      "   getChild(i).prettyPrint(out, indent);",
                      "}",]),
            ]

    class_methods.update({
            'ASTNode': astnode_methods
        })

    # Add ast-types that only get a primitive attribute.
    def prim_expression(get_type):
        return "out.print(get{}());".format(get_type)

    prim_types = [
                ('IdUse', 'ID'),
                ('IdDeclare', 'ID'),
                ('Numeral', 'NUMERAL'),
            ]

    class_methods.update({ast_type : prim_expression(prim_type) for ast_type,
                          prim_type in prim_types})

    class_methods['Program'] = ""
    class_methods['List'] = ""

    space = 'out.print(" ");'

    def jprint(value, quotes=True):
        if quotes:
            return "out.print(\"{}\");".format(value)
        return "out.print({});".format(value)

    def jinprint(value, quotes=True):
        if quotes:
            return "out.print(indent+\"{}\");".format(value)
        return "out.print(indent+{});".format(value)

    def jinprintln(value, quotes=True):
        if quotes:
            return "out.println(indent+\"{}\");".format(value)
        return "out.println(indent+{});".format(value)

    def jprintln(value, quotes=True):
        if quotes:
            return "out.println(\"{}\");".format(value)
        return "out.println({});".format(value)

    def pretty_print(str_object):
        pretty_format = '{}.prettyPrint(out, indent+"  ");'
        return pretty_format.format(str_object);

    def jif(expression):
        return "if ({}) {{".format(expression)


    newline = jprintln('')

    id_from_decl = jprint('getIdDeclare().getID()', False)
    id_from_use = jprint('getIdUse().getID()', False)

    class_methods['FunctionDeclaration'] = sep.join([
            jinprint('int'),
            space,
            id_from_decl,
            jprint('('),
            "int iMax = getNumFunctionParameters();",
            iter_over("iMax"),
            jprint("int"),
            space,
            pretty_print('getFunctionParameters(i)'),
            'if (iMax > 1 && i < (iMax - 1)) {',
            jprint(', '),
            '}',
            '}',
            jprint(')'),
            space,
            jprintln('{'), # End of function definition.
            iter_over("getNumBlock()"),
            pretty_print('getBlock(i)'),
            '}', # Iter over ends.
            pretty_print('getReturn()'),
            newline,
            jinprint('}'),
        ])

    class_methods['Return'] = sep.join([
            jinprint('return'),
            space,
            pretty_print('getExpression()'),
            jprint(';'),
        ])

    class_methods['VarDeclare'] = sep.join([
            jinprint('int'),
            space,
            id_from_decl,
            jif('hasExpression()'),
            jprint(" = "),
            pretty_print('getExpression()'),
            '}',
            jprint(';'),
            newline,
        ])

    class_methods['Assign'] = sep.join([
            jinprint(''),
            id_from_use,
            jprint(" = "),
            pretty_print('getExpression()'),
            jprint(';'),
            newline,
        ])

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

        if line.startswith('}'):
            level -= 1

        indentation = indentation_step * level * ' '
        indented_line = "{}{}".format(indentation, line)
        if not line.strip(): # Don't append only whitespace.
            indented_lines.append(indented_line.strip())
        else:
            indented_lines.append(indented_line)

        if line.endswith('{'):
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
            "BinaryLogicalExpression",
            "IF",
            "WHILE",
            "ELSE",
            "NOEQ",
            "EQ",
            "LTEQ",
            "GTEQ",
            "LT",
            "GT",
            "IdUse",
            "IdDeclare",
            "VarDeclare",
            "Numeral",
            ]

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
