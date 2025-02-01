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

    def test_S(self):
        node_1 = Node("/")
        node_2= Node("terminal", 2)
        node_3 = Node("+")
        node_4 = Node("/")
        node_5 = Node("terminal", 3)
        node_6 = Node("-")
        node_7 = Node("terminal", 1)
        node_8 = Node("/")
        node_9 = Node("terminal", 2)
        node_10 = Node("terminal", "x")
        node_11 = Node("terminal", 1)
        node_1.set_left_child(node_2)
        node_1.set_right_child(node_3)
        node_3.set_left_child(node_4)
        node_3.set_right_child(node_11)
        node_4.set_left_child(node_5)
        node_4.set_right_child(node_6)
        node_6.set_left_child(node_7)
        node_6.set_right_child(node_8)
        node_8.set_left_child(node_9)
        node_8.set_right_child(node_10)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11]
        observations = [1, 4, -2]
        targets = [5, 4, 1]
        semantics = [(-1, 0.286, 0.8), (2, 2, 2), (-2, 7, 2.5), (-3, 6, 1.5), (3, 3, 3), (-1, 0.5, 2), (1, 1, 1), (2, 0.5, -1), (2, 2, 2), (1, 4, -2), (1, 1, 1)]
        aes = [(1, 1, 1), (1, 1, 1), (5, 4, 1), (-5, -4, -1), (-5, -4, -1), (-3, -2, 1), (-3, -2, 1), (3, 2, -1), (3, 2, -1), (-18, -14, -2), (-5, -4, -1)]
        bs = [(5, 4, 1), (-10, 28, 2.5), (2, 2, 2), (3, 2, -1), (-3, 1, -2), (15, 12, 3), (9, 11, 2), (18, 14, 2), (18, 56, -4), (-6, -4, 2), (-17, 22, -0.5)]
        cs = [(0, 0, 0), (0, 0, 0), (-1, -1, -1), (1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 1, 1), (-1, -1, -1), (-1, -1, -1), (4, 4, 4), (1, 1, 1)]
        ds = [(-1, -1, -1), (2, -7, -2.5), (0, 0, 0), (-1, -1, -1), (1, -0.5, -2), (-3, -3, -3), (-1, -2.5, -4), (-4, -4- -4), (-4, -16- 8), (2, 2, 2), (3, -6, -1.5)]
        Ss = [set(), set(), {(0,0,0)}, {(-1, -1, -1)}, {(1, -0.5, -2)}, {(0, 0, 0), (-3, -3, -3)}, {(2, 0.5, -1), (-1, -2.5, -4)}, {(1, 1, 1), (4, 4,4)}, {(1, 4, -2), (4, 16, -8)}, {(0, 0, 0), (2, 2, 2), (0.5, 0.5, 0.5)}, {(3, -6, -1.5)}]
        node_1.update_semantics(observations)
        node_1.update_sme(targets)

        for index in range(len(targets)):
            node = nodes[index]
            semantic = semantics[index]
            a = aes[index]
            b = bs[index]
            c = cs[index]
            d = ds[index]
            s = Ss[index]
            self.assertLess(self.dist(node.semantics, semantic), 1e-3, f"Semantic: error in node {index +1}\n{node.semantics}\n{semantic}")
            self.assertLess(self.dist(node.aes, a), 1e-3, f"Aes: error in node {index + 1}\n{node.aes}\n{a}")
            self.assertLess(self.dist(node.bs, b), 1e-3, f"Aes: error in node {index + 1}\n{node.bs}\n{b}")
            self.assertLess(self.dist(node.cs, c), 1e-3, f"Aes: error in node {index + 1}\n{node.cs}\n{c}")
            self.assertLess(self.dist(node.ds, d), 1e-3, f"Aes: error in node {index + 1}\n{node.ds}\n{d}")
            self.assertEqual(len(node.Ss), len(s), f"Ss: error in node {index + 1}\n{node.Ss}\n{s}")
            for node_s, s_s in zip(node.Ss, s):
                self.assertLess(self.dist(node_s, s_s), 1e-3, f"Ss: error in node {index + 1}\n{node.Ss}\n{s}")

    def dist(self, vs, ws):
        distance = (sum([abs(v-w) ** 2 for v, w in zip (vs, ws)])) ** 0.5
        return distance

if __name__ == "__main__":
    unittest.main()
