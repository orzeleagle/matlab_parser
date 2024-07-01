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
"eyJAKHgpMC9pc2VxdWFsKHgsJ1dIQVRJRicpIjogImxhbWJkYSB4OiBucC5uYW4gaWYgbm90IHggPT0gJ1dIQVRJRicgZWxzZSAwIiwgIkAoeCkwL2lzZXF1YWwoeCwnTm90IEFwcGxpY2FibGUnKSI6ICJsYW1iZGEgeDogbnAubmFuIGlmIG5vdCB4ID09ICdOb3QgQXBwbGljYWJsZScgZWxzZSAwIiwgIkAoeCkxIjogImxhbWJkYSB4OiAxIiwgIkAoeCkwLy14IjogImxhbWJkYSB4OiBucC5uYW4gaWYgeCA9PSAwIGVsc2UgLXgiLCAiQCh4LG92KTAvfmNvbnRhaW5zKGNoYXIoeCksJ0RlZmF1bHQnKSI6ICJsYW1iZGEgeDogbnAubmFuIGlmICdEZWZhdWx0JyBub3QgaW4gc3RyKHgpIGVsc2UgMCIsICJAKHgpTWFwU2xvdDJTY29yZS5wcmVkaWN0KHgpIjogImxhbWJkYSB4OiBNYXBTbG90MlNjb3JlLnByZWRpY3QoeCkiLCAiQCh4KTAveH49MCI6ICJsYW1iZGEgeDogbnAubmFuIGlmIHggPT0gMCBlbHNlIDAiLCAiQCh4KTAvKDEuMT49eCkrNCI6ICJsYW1iZGEgeDogbnAubmFuIGlmIDEuMSA8IHggZWxzZSA0IiwgIkAoeCkwLygxLjM+PXgpKzMiOiAibGFtYmRhIHg6IG5wLm5hbiBpZiAxLjMgPCB4IGVsc2UgMyIsICJAKHgpMC8oMS41Pj14KSsyIjogImxhbWJkYSB4OiBucC5uYW4gaWYgMS41IDwgeCBlbHNlIDIiLCAiQCh4KXZhbHVlczJzbG90KG51bTJzdHIoeCkpIjogImxhbWJkYSB4OiB2YWx1ZXMyc2xvdChzdHIoeCkpIiwgIkAoeCkwLyg2MD49eCkrMSI6ICJsYW1iZGEgeDogbnAubmFuIGlmIDYwIDwgeCBlbHNlIDEiLCAiQCh4KTAvKDc1Pj14KSsyIjogImxhbWJkYSB4OiBucC5uYW4gaWYgNzUgPCB4IGVsc2UgMiIsICJAKHgpMC8oOTA+PXgpKzMiOiAibGFtYmRhIHg6IG5wLm5hbiBpZiA5MCA8IHggZWxzZSAzIiwgIkAoeCk0IjogImxhbWJkYSB4OiA0IiwgIkAobUNvbmQsZmluUixmaW5SUyxhZHZBLGFkdlJTLFN0ckFuLFByb3BQaCxDRmxvd1ByZWQpZmluYW5jaWFsU3RyZW5ndGhXZWlnaHQqKGRvdWJsZShtQ29uZCk7ZmluUjthZHZSO2RvdWJsZShTdHJBbik7ZG91YmxlKENGbG93UHJlZCkpIjogImxhbWJkYSBtQ29uZCwgZmluUiwgZmluUlMsIGFkdkEsIGFkdlJTLCBTdHJBbiwgUHJvcFBoLCBDRmxvd1ByZWQ6IGZpbmFuY2lhbFN0cmVuZ3RoV2VpZ2h0ICogbnAuYXJyYXkoW2Zsb2F0KG1Db25kKSwgZmluUiwgYWR2UlMsIGZsb2F0KFN0ckFuKSwgZmxvYXQoQ0Zsb3dQcmVkKV0pLnN1bSgpIiwgIkAoRmluU3RySU5EX0JSKXJvdW5kKEZpblN0cklORF9CUikiOiAibGFtYmRhIEZpblN0cklORF9CUjogcm91bmQoRmluU3RySU5EX0JSKSIsICJAKExSRW52LFBvbFRyUmlzaylwb2xpdGljYWxMZWdhbEVudldlaWdodCooZG91YmxlKExSRW52KStkb3VibGUoUG9sVHJSaXNrKSkiOiAibGFtYmRhIExSRW52LCBQb2xUclJpc2s6IHBvbGl0aWNhbExlZ2FsRW52V2VpZ2h0ICogKGZsb2F0KExSRW52KSArIGZsb2F0KFBvbFRyUmlzaykpIiwgIkAoUG9sTGVnRW52X0JSKXJvdW5kKFBvbExlZ0Vudl9CUikiOiAibGFtYmRhIFBvbExlZ0Vudl9CUjogcm91bmQoUG9sTGVnRW52X0JSKSIsICJAKHgpMC8oMTU+eCkrMSI6ICJsYW1iZGEgeDogbnAubmFuIGlmIDE1IDw9IHggZWxzZSAxIiwgIkAoeCkwLygyMD54KSsyIjogImxhbWJkYSB4OiBucC5uYW4gaWYgMjAgPD0geCBlbHNlIDIiLCAiQCh4KTAvKDI1PngpKzMiOiAibGFtYmRhIHg6IG5wLm5hbiBpZiAyNSA8PSB4IGVsc2UgMyIsICJAKEFtb3JTY2gsQW1vclNjaFMsTVJlZlJpc2spRmluYW5jaWFsU3RydWN0dXJlc1dlaWdodHMqW0Ftb3JTY2g7ZG91YmxlKE1SZWZSaXNrKV0iOiAibGFtYmRhIEFtb3JTY2gsIEFtb3JTY2hTLCBNUmVmUmlzazogbnAuZG90KEZpbmFuY2lhbFN0cnVjdHVyZXNXZWlnaHRzLCBucC5hcnJheShbQW1vclNjaCwgZmxvYXQoTVJlZlJpc2spXSkpIiwgIkAoRmluU3RydWN0SU5WX0JSKXJvdW5kKEZpblN0cnVjdElOVl9CUikiOiAibGFtYmRhIEZpblN0cnVjdElOVl9CUjogcm91bmQoRmluU3RydWN0SU5WX0JSKSIsICJAKGxvYyxEZXNDb25kLEZpblN0cnVjdElOVilBc3NldFRyYW5zYWN0aW9uQ2hhcmFjdFdlaWdodHMqW2RvdWJsZShsb2MpO2RvdWJsZShEZXNDb25kKTtGaW5TdHJ1Y3RJTlZdIjogImxhbWJkYSBsb2MsIERlc0NvbmQsIEZpblN0cnVjdElOVjogbnAuZG90KEFzc2V0VHJhbnNhY3Rpb25DaGFyYWN0V2VpZ2h0cywgbnAuYXJyYXkoW2Zsb2F0KGxvYyksIGZsb2F0KERlc0NvbmQpLCBGaW5TdHJ1Y3RJTlZdKSkiLCAiQChBc3NldFRyYW5zSU5WX0JSKXJvdW5kKEFzc2V0VHJhbnNJTlZfQlIpIjogImxhbWJkYSBBc3NldFRyYW5zSU5WX0JSOiByb3VuZChBc3NldFRyYW5zSU5WX0JSKSIsICJAKGZpbmNhcFdpbGwsUmVwLFJlbFJFKXN0cmVuZ3RoU3BvbnNEZVdlaWdodHMqW2RvdWJsZShmaW5jYXBXaWxsKTtkb3VibGUoUmVwKTtkb3VibGUoUmVsUkUpXSI6ICJsYW1iZGEgZmluY2FwV2lsbCwgUmVwLCBSZWxSRTogbnAuZG90KHN0cmVuZ3RoU3BvbnNEZVdlaWdodHMsIG5wLmFycmF5KFtmbG9hdChmaW5jYXBXaWxsKSwgZmxvYXQoUmVwKSwgZmxvYXQoUmVsUkUpXSkpIiwgIkAoU3BvbnNEZXZfQlIpcm91bmQoU3BvbnNEZXZfQlIpIjogImxhbWJkYSBTcG9uc0Rldl9CUjogcm91bmQoU3BvbnNEZXZfQlIpIiwgIkAobGllbixyZW50cyxxdWFsSW5zKXNlY3VyUGFja1dlaWdodHMqW2RvdWJsZShsaWVuKTtkb3VibGUocmVudHMpO2RvdWJsZShxdWFsSW5zKV0iOiAibGFtYmRhIGxpZW4sIHJlbnRzLCBxdWFsSW5zOiBucC5kb3Qoc2VjdXJQYWNrV2VpZ2h0cywgbnAuYXJyYXkoW2Zsb2F0KGxpZW4pLCBmbG9hdChyZW50cyksIGZsb2F0KHF1YWxJbnMpXSkpIiwgIkAoU2VjUGFja19CUilyb3VuZChTZWNQYWNrX0JSKSI6ICJsYW1iZGEgU2VjUGFja19CUjogcm91bmQoU2VjUGFja19CUikiLCAiQCh4MSx4Mix4Myx4NCx4NSlGaW5hbFNjb3JlV2VpZ2h0cypbeDE7eDI7eDM7eDQ7eDVdIjogImxhbWJkYSB4MSwgeDIsIHgzLCB4NCwgeDU6IG5wLmRvdChGaW5hbFNjb3JlV2VpZ2h0cywgbnAuYXJyYXkoW3gxLCB4MiwgeDMsIHg0LCB4NV0pKSIsICJAKG1vZGVsU2NvcmVfQlIpcm91bmQobW9kZWxTY29yZV9CUikiOiAibGFtYmRhIG1vZGVsU2NvcmVfQlI6IHJvdW5kKG1vZGVsU2NvcmVfQlIpIiwgIkAoeDEseDIseDMpMC94Mit4MiI6ICJsYW1iZGEgeDEsIHgyLCB4MzogeDIiLCAiQCh4MSx4Mix4MykwL3gxK01hcFNsb3QyU2NvcmUucHJlZGljdCh4MikiOiAibGFtYmRhIHgxLCB4MiwgeDM6IE1hcFNsb3QyU2NvcmUucHJlZGljdCh4MikiLCAiQCh4KXgiOiAibGFtYmRhIHg6IHgifQ=="
'''
