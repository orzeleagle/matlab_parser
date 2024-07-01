import numpy as np


def tree_to_python(matlab_node):
    if isinstance(matlab_node[0], tuple):
        # Handle tuple nodes representing variables or literals
        return tree_to_python(matlab_node[0])

    if matlab_node[0] == 'code_block':
        return tree_to_python(matlab_node[1][0])

    if matlab_node[0] == 'statement':
        return tree_to_python(matlab_node[1][0])

    if matlab_node[0] == 'anonym_func':
        args = tree_to_python(matlab_node[1][0])
        body = tree_to_python(matlab_node[1][1])
        return f"lambda {args}: {body}"

    if matlab_node[0] == 'args':
        return ', '.join(tree_to_python(arg) for arg in matlab_node[1])

    if matlab_node[0] == 'expr':
        return tree_to_python(matlab_node[1][0])

    if matlab_node[0] == 'func_call/array_idxing':
        func_expr = tree_to_python(matlab_node[1][0])
        args = [tree_to_python(arg) for arg in matlab_node[1][1]]
        if func_expr == 'isequal':
            # Ensure the correct mapping of 'WHATIF' and variable in the isequal function
            return f"np.nan if not ({args[1]} == {args[0]}) else 0"
        else:
            return f"{func_expr}({', '.join(args)})"

    if matlab_node[0] == '"/" oper':
        left = tree_to_python(matlab_node[1][0])
        right = tree_to_python(matlab_node[1][1])
        # Handle 'isequal' within the '/' operation by ignoring the '/' if 'isequal' is present
        if 'isequal' in right:
            return right
        return f"{left} / {right}"

    if isinstance(matlab_node[0], str):
        return matlab_node[0]

    raise ValueError(f"Unknown node type: {matlab_node[0]}")


# Example usage
parsed_expression = "XDD"

# Generate Python code from parsed tree
python_code = tree_to_python(parsed_expression)
print(python_code)


# Display the tree for visualization
def display_tree(matlab_node, indent_str=''):
    if len(matlab_node) == 1:
        return str(matlab_node[0]) + '\n'

    node_name_string = matlab_node[0]
    childens_indent_str = len(node_name_string) * ' '

    if len(matlab_node[1]) == 1:
        display_string = node_name_string + ' ──── ' + \
                         display_tree(matlab_node[1][0], indent_str=indent_str + childens_indent_str + '      ')
    else:
        display_string = node_name_string + ' ─┬── ' + \
                         display_tree(matlab_node[1][0], indent_str=indent_str + childens_indent_str + '  │   ')
        for child_node in matlab_node[1][1:-1]:
            display_string += indent_str + len(node_name_string) * ' ' + '  ├── ' + \
                              display_tree(child_node, indent_str=indent_str + childens_indent_str + '  │   ')
        display_string += indent_str + len(node_name_string) * ' ' + '  └── ' + \
                          display_tree(matlab_node[1][-1], indent_str=indent_str + childens_indent_str + '      ')
    return display_string


print(display_tree(parsed_expression))

'''
eyJAKHgpMC9pc2VxdWFsKHgsJ1dIQVRJRicpIjogImxhbWJkYSB4OiBucC5uYW4gaWYgbm90IHggPT0gJ1dIQVRJRicgZWxzZSAwIiwgIkAoeCkwL2lzZXF1YWwoeCwnTm90IEFwcGxpY2FibGUnKSI6ICJsYW1iZGEgeDogbnAubmFuIGlmIG5vdCB4ID09ICdOb3QgQXBwbGljYWJsZScgZWxzZSAwIiwgIkAoeCkxIjogImxhbWJkYSB4OiAxIiwgIkAoeCkwLy14IjogImxhbWJkYSB4OiBucC5uYW4gaWYgeCA9PSAwIGVsc2UgLXgiLCAiQCh4LG92KTAvfmNvbnRhaW5zKGNoYXIoeCksJ0RlZmF1bHQnKSI6ICJsYW1iZGEgeDogbnAubmFuIGlmICdEZWZhdWx0JyBub3QgaW4gc3RyKHgpIGVsc2UgMCIsICJAKHgpTWFwU2xvdDJTY29yZS5wcmVkaWN0KHgpIjogImxhbWJkYSB4OiBNYXBTbG90MlNjb3JlLnByZWRpY3QoeCkiLCAiQCh4KTAveH49MCI6ICJsYW1iZGEgeDogbnAubmFuIGlmIHggPT0gMCBlbHNlIDAiLCAiQCh4KTAvKDEuMT49eCkrNCI6ICJsYW1iZGEgeDogbnAubmFuIGlmIDEuMSA8IHggZWxzZSA0IiwgIkAoeCkwLygxLjM
'''
