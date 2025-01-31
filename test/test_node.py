import unittest

from src.node import Node

class Test_Node(unittest.TestCase):
    observations = [1, 2, 3]
    targets = [1, 1, 1]
    semantics = {
            "+": [2, 3, 4], 
            "-": [0, 1, 2],
            "*": [1, 2, 3],
            "/": [1, 2, 3],
        }
    smes = {
        "+": 14/3, 
        "-": 2/3,
        "*": 5/3,
        "/": 5/3,
    }
    nodes = {}
    for operation in semantics.keys():
        nodes[operation] = Node(operation)
        node_left = Node("terminal", "x")
        node_right = Node("terminal", 1)
        nodes[operation].set_left_child(node_left)
        nodes[operation].set_right_child(node_right)
        print(f">>>>Operation {operation}")
        nodes[operation].update_semantics(observations)
        nodes[operation].update_sme(targets)

    def test_semantics(self):
        for operation in self.semantics.keys():
            node = self.nodes[operation]
            self.assertEqual(node.semantics, self.semantics[operation], f"Failed semantic {operation}")

    def test_sme(self):
        for operation in self.semantics.keys():
            node = self.nodes[operation]
            sme = self.smes[operation]
            for index, test_node in enumerate([node, node.right_child, node.left_child]):
                self.assertLess(abs(test_node.sme - sme), 1e-10, f"Failed sme {operation}. Node {index}. SME {test_node.sme}")

if __name__ == "__main__":
    unittest.main()
