from graphviz import Digraph

def reduce_ast(ast):
    ast_now = []
    if not isinstance(ast, (tuple, list)):
        """base condition"""
        ast_now = ast
        return ast_now

    else:
        node_len = len(ast) 
        ast_now.insert(len(ast_now), ast[0])
        """iterate over each child node"""
        k = 1 
        for node in ast[1:]:
            reduce_child_node = reduce_ast(node)
            if not reduce_child_node[0] == ast[0]:
                """add the reduce_child_node to the present ast"""
                ast_now.insert(len(ast_now), reduce_child_node)
            else:
                ast_now.extend(reduce_child_node[1:])    
        if node_len == 2:
            """directly return second element""" 
            return ast_now[k]
        return ast_now

def generate_graph_from_ast_2(tree, ast, child_id, parent_id, count):
    
    """traverse until all nodes visited """
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
                tree.node(str(child_id_duplicate), str(ast[i]), color = "blue", shape = "ellipse")
                tree.edge(str(parent_id), str(child_id_duplicate), color = "black")
            else:
                """recurse"""
                child_id = generate_graph_from_ast_2(tree, ast[i], child_id, child_id-1, count)
                tree.node(str(child_id_duplicate), str(ast[i][j]), color = "blue", shape = "ellipse")
                tree.edge(str(parent_id), str(child_id_duplicate), color = "black")
        return child_id

    else:
        tree.node(str(child_id), str(ast), color = "blue", shape = "ellipse")
        tree.edge(str(parent_id), str(child_id), color = "black")
        """ updated node id when base case """
        update_id = child_id + 1
        return update_id
        

def generate_graph_from_ast(ast, filename="AST"):
    
    """".dot format """
    tree = Digraph(format="dot")

    """index 0 from root"""
    root = 0
    add_to_root = root + 1
    count = 1

    """add root node """
    tree.node(str(root), str(ast[0]), color = "blue", shape = "ellipse")

    generate_graph_from_ast_2(tree, ast, add_to_root, root, count)

    ##print(visited)

    """render for drawing graphical represenattions """
    tree.render(filename=filename)

    """Return: The tree object."""
    return tree


