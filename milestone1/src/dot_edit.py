from graphviz import Digraph


def tree_gen_helper(tree, ast, child_id, parent_id, count):
    """traverse until all nodes visited"""
    if isinstance(ast, (tuple, list)):
        count = count + 1
        node_len = len(ast)
        for i in range(1, node_len):
            j = 0
            """update of nodes"""
            child_id = child_id + 1
            child_id_duplicate = child_id - 1
            """recursive check"""
            if not isinstance(ast[i], (tuple, list)):
                """no further recurse"""
                tree.node(str(child_id_duplicate), str(ast[i]), color="blue", shape="ellipse")
                tree.edge(str(parent_id), str(child_id_duplicate), color="black")
            else:
                """recurse"""
                child_id = tree_gen_helper(tree, ast[i], child_id, child_id - 1, count)
                tree.node(str(child_id_duplicate), str(ast[i][j]), color="blue", shape="ellipse")
                tree.edge(str(parent_id), str(child_id_duplicate), color="black")
        return child_id

    else:
        tree.node(str(child_id), str(ast), color="blue", shape="ellipse")
        tree.edge(str(parent_id), str(child_id), color="black")
        """ updated node id when base case """
        update_id = child_id + 1
        return update_id


def tree_gen(ast, filename="AST"):
    """ ".dot format"""
    tree = Digraph(format="dot")

    """index 0 from root"""
    root = 0
    add_to_root = root + 1
    count = 1

    """add root node """
    tree.node(str(root), str(ast[0]), color="blue", shape="ellipse")

    tree_gen_helper(tree, ast, add_to_root, root, count)

    """render for drawing graphical representations """
    tree.render(filename=filename)

    """Return: The tree object."""
    return tree

def tree_reduce(ast):
    current_ast = []
    if isinstance(ast, (tuple, list)):
        nChildren = len(ast) - 1
        current_ast.append(ast[0])
        for child in ast[1:]:
            reduced_child = tree_reduce(child)
            if reduced_child is not None and reduced_child[0] == ast[0]:
                current_ast.extend(reduced_child[1:])
            elif reduced_child is not None:
                current_ast.append(reduced_child)
        if nChildren == 1:
            if len(current_ast) > 1 and isinstance(current_ast[1], (tuple, list)):
                return current_ast[1]
            else:
                return current_ast
    else:
        current_ast = ast
    return current_ast
