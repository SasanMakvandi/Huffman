"""
Assignment 2 starter code
CSC148, Winter 2020
Instructors: Bogdan Simion, Michael Liut, and Paul Vrbik

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Bogdan Simion, Michael Liut, Paul Vrbik, Dan Zingaro
"""
from __future__ import annotations
import time
from typing import Dict, Tuple
from utils import *
from huffman import HuffmanTree


# ====================
# Functions for compression


def build_frequency_dict(text: bytes) -> Dict[int, int]:
    """ Return a dictionary which maps each of the bytes in <text> to its
    frequency.

    >>> d = build_frequency_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    """
    final = {}
    for el in text:
        if el in final:
            final[el] += 1
        else:
            final[el] = 1
    return final


def build_huffman_tree(freq_dict: Dict[int, int]) -> HuffmanTree:
    """ Return the Huffman tree corresponding to the frequency dictionary
    <freq_dict>.

    Precondition: freq_dict is not empty.

    >>> freq = {2: 6, 3: 4}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> t == result
    True
    >>> freq = {2: 6, 3: 4, 7: 5}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(2), \
                            HuffmanTree(None, HuffmanTree(3), HuffmanTree(7)))
    >>> t == result
    True
    >>> import random
    >>> symbol = random.randint(0,255)
    >>> freq = {symbol: 6}
    >>> t = build_huffman_tree(freq)
    >>> any_valid_byte_other_than_symbol = (symbol + 1) % 256
    >>> dummy_tree = HuffmanTree(any_valid_byte_other_than_symbol)
    >>> result = HuffmanTree(None, HuffmanTree(symbol), dummy_tree)
    >>> t.left == result.left or t.right == result.right
    True
    """
    i, j = find_smallest_dict(freq_dict)
    if j == 0:
        a = freq_dict.pop(i)
        smaller = HuffmanTree(i)
        temp = HuffmanTree(None, smaller, None)
        freq_dict['Total'] = a
    else:
        a, b = freq_dict.pop(i), freq_dict.pop(j)
        smaller = HuffmanTree(i)
        second_smallest = HuffmanTree(j)
        temp = HuffmanTree(None, smaller, second_smallest)
        freq_dict['Total'] = a + b
    if not len(freq_dict) == 1:
        result = build_huffman_tree(freq_dict)
        result.right = temp
        return result
    else:
        return temp


def find_smallest_dict(dic: Dict[int, int]) -> Tuple(int, int):
    """" Returns the two smallest elements in the dictionary
    Helper for build_huffman_tree

    >>> a = {2: 32, 3: 34, 4: 21, 5: 55}
    >>> find_smallest_dict(a)
    (4, 2)
    >>> b = {2 : 6, 3 : 4}
    >>> find_smallest_dict(b)
    (3, 2)
    """
    smallest = 0
    second_smallest = 0
    # find the smallest frequency
    temp1 = 0
    for el in dic:
        if temp1 == 0:
            temp1 = dic[el]
            smallest = el
        else:
            if dic[el] < temp1:
                temp1 = dic[el]
                smallest = el
    # find the second smallest
    temp2 = 0
    for el in dic:
        if temp2 == 0 and dic[el] != temp1:
            temp2 = dic[el]
            second_smallest = el
        elif dic[el] < temp2 and dic[el] != temp1:
            temp2 = dic[el]
            second_smallest = el
    return smallest, second_smallest


def get_codes(tree: HuffmanTree) -> Dict[int, str]:
    """ Return a dictionary which maps symbols from the Huffman tree <tree>
    to codes.

    >>> tree = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    >>> tree1 = HuffmanTree(None, HuffmanTree(3), HuffmanTree(None, HuffmanTree(2), HuffmanTree(4)))
    >>> d = get_codes(tree1)
    >>> d == {3: "0", 2: "10", 4: "11"}
    True
    """
    result = {}
    if tree.symbol is None and tree.left is not None:
        left = get_codes(tree.left)
        for el in left:
            left[el] = "0" + left[el]
        result.update(left)
    if tree.symbol is None and tree.right is not None:
        right = get_codes(tree.right)
        for el in right:
            right[el] = "1" + right[el]
        result.update(right)
    else:
        return {tree.symbol: ""}
    return result


def number_nodes(tree: HuffmanTree) -> None:
    """ Number internal nodes in <tree> according to postorder traversal. The
    numbering starts at 0.
    >>> leftleft = HuffmanTree(None, HuffmanTree(4), HuffmanTree(12))
    >>> left = HuffmanTree(None, leftleft, HuffmanTree(2))
    >>> right = HuffmanTree(None, HuffmanTree(9), HuffmanTree(10))
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.left.number
    0
    >>> tree.left.number
    1
    >>> tree.right.number
    2
    >>> tree.number
    3
    """
    curr_number = 0
    list_of_nodes = []
    dict_of_nodes = find_internal_nodes(tree, 0)
    for el in dict_of_nodes:
        list_of_nodes.append(el)
    list_of_nodes.reverse()
    for el in list_of_nodes:
        for tree in dict_of_nodes[el]:
            tree.number = curr_number
            curr_number += 1


def find_internal_nodes(tree: HuffmanTree, starter: 0) -> Dict[int, list]:
    """
    Function finds all the internal nodes in a tree
    Helper function of the number_nodes function
    :return a dictionary with nodes to each corresponding level
    >>> leftleft = HuffmanTree(None, HuffmanTree(20), HuffmanTree(71))
    >>> left = HuffmanTree(None, HuffmanTree(3), leftleft)
    >>> right = HuffmanTree(None, HuffmanTree(9), HuffmanTree(10))
    >>> tree = HuffmanTree(None, left, right)
    >>> find_internal_nodes(tree, 0)
    {0: [tree], 1: [left, right], 2: [leftleft]}
    """
    result = {}
    if tree.symbol is None:
        result[starter] = [tree]
        left = find_internal_nodes(tree.left, starter + 1)
        right = find_internal_nodes(tree.right, starter + 1)
        for el in left:
            if el in result:
                result[el].extend(left[el])
            else:
                result[el] = left[el]
        for el in right:
            if el in result:
                result[el].extend(right[el])
            else:
                result[el] = right[el]
    return result


def avg_length(tree: HuffmanTree, freq_dict: Dict[int, int]) -> float:
    """ Return the average number of bits required per symbol, to compress the
    text made of the symbols and frequencies in <freq_dict>, using the Huffman
    tree <tree>.

    The average number of bits = the weighted sum of the length of each symbol
    (where the weights are given by the symbol's frequencies), divided by the
    total of all symbol frequencies.

    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(9)
    >>> tree = HuffmanTree(None, left, right)
    >>> avg_length(tree, freq)  # (2*2 + 7*2 + 1*1) / (2 + 7 + 1)
    1.9
    """
    total_num_freq = 0
    for num in freq_dict:
        total_num_freq += freq_dict[num]
    total_bit = total_bits(tree, freq_dict, 0)
    return total_bit/total_num_freq


def total_bits(tree: HuffmanTree, freq_dict: Dict[int, int], curr_level: int):
    """Return the total number of bits in this tree
    Helper function for avg_length
    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(9)
    >>> tree = HuffmanTree(None, left, right)
    >>> total_bits(tree, freq, 0)
    19
    """
    total_bit = 0
    if tree.symbol is not None:
        total_bit = freq_dict[tree.symbol] * curr_level
    else:
        if tree.left is not None:
            total_bit += total_bits(tree.left, freq_dict, (curr_level + 1))
        if tree.right is not None:
            total_bit += total_bits(tree.right, freq_dict, (curr_level + 1))
    return total_bit


def compress_bytes(text: bytes, codes: Dict[int, str]) -> bytes:
    """ Return the compressed form of <text>, using the mapping from <codes>
    for each symbol.

    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0])
    >>> result = compress_bytes(text, d)
    >>> result == bytes([184])
    True
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> result = compress_bytes(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    """
    result = []
    curr_text = ''
    for el in text:
        if not (len(curr_text)) + (len(codes[el])) >= 8:
            curr_text += codes[el]
        else:
            diff = (len(curr_text) + len(codes[el])) - 8
            curr_text += (codes[el][:diff])
            result.append(curr_text)
            curr_text = (codes[el][diff:])
    if not result:
        while len(curr_text) != 8:
            curr_text += '0'
        temp = int(curr_text, 2)
        return bytes([temp])
    else:
        if curr_text not in result:
            result.append(curr_text)
        final = []
        for el in result:
            if len(el) != 8:
                while len(el) != 8:
                    el += '0'
            final.append(int(el, 2))
        return bytes(final)



def tree_to_bytes(tree: HuffmanTree) -> bytes:
    """ Return a bytes representation of the Huffman tree <tree>.
    The representation should be based on the postorder traversal of the tree's
    internal nodes, starting from 0.

    Precondition: <tree> has its nodes numbered.

    >>> tree = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> right = HuffmanTree(5)
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    >>> tree = build_huffman_tree(build_frequency_dict(b"helloworld"))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))\
            #doctest: +NORMALIZE_WHITESPACE
    [0, 104, 0, 101, 0, 119, 0, 114, 1, 0, 1, 1, 0, 100, 0, 111, 0, 108,\
    1, 3, 1, 2, 1, 4]
    """
    # TODO: Implement this function
    pass


def compress_file(in_file: str, out_file: str) -> None:
    """ Compress contents of the file <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = build_frequency_dict(text)
    tree = build_huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (tree.num_nodes_to_bytes() + tree_to_bytes(tree) +
              int32_to_bytes(len(text)))
    result += compress_bytes(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)


# ====================
# Functions for decompression

def generate_tree_general(node_lst: List[ReadNode],
                          root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes nothing about the order of the tree nodes in the list.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(10, None, None), \
HuffmanTree(12, None, None)), \
HuffmanTree(None, HuffmanTree(5, None, None), HuffmanTree(7, None, None)))
    """
    # TODO: Implement this function
    pass


def generate_tree_postorder(node_lst: List[ReadNode],
                            root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes that the list represents a tree in postorder.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(5, None, None), \
HuffmanTree(7, None, None)), \
HuffmanTree(None, HuffmanTree(10, None, None), HuffmanTree(12, None, None)))
    """
    # TODO: Implement this function
    pass


def decompress_bytes(tree: HuffmanTree, text: bytes, size: int) -> bytes:
    """ Use Huffman tree <tree> to decompress <size> bytes from <text>.

    >>> tree = build_huffman_tree(build_frequency_dict(b'helloworld'))
    >>> number_nodes(tree)
    >>> decompress_bytes(tree, \
             compress_bytes(b'helloworld', get_codes(tree)), len(b'helloworld'))
    b'helloworld'
    """
    # TODO: Implement this function
    pass


def decompress_file(in_file: str, out_file: str) -> None:
    """ Decompress contents of <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_general(node_lst, num_nodes - 1)
        size = bytes_to_int(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(decompress_bytes(tree, text, size))


# ====================
# Other functions

def improve_tree(tree: HuffmanTree, freq_dict: Dict[int, int]) -> None:
    """ Improve the tree <tree> as much as possible, without changing its shape,
    by swapping nodes. The improvements are with respect to the dictionary of
    symbol frequencies <freq_dict>.

    >>> left = HuffmanTree(None, HuffmanTree(99, None, None), \
    HuffmanTree(100, None, None))
    >>> right = HuffmanTree(None, HuffmanTree(101, None, None), \
    HuffmanTree(None, HuffmanTree(97, None, None), HuffmanTree(98, None, None)))
    >>> tree = HuffmanTree(None, left, right)
    >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
    >>> avg_length(tree, freq)
    2.49
    >>> improve_tree(tree, freq)
    >>> avg_length(tree, freq)
    2.31
    """
    # TODO: Implement this function
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compress_file', 'decompress_file'],
        'allowed-import-modules': [
            'python_ta', 'doctest', 'typing', '__future__',
            'time', 'utils', 'huffman', 'random'
        ],
        'disable': ['W0401']
    })

    mode = input("Press c to compress, d to decompress, or other key to exit: ")
    if mode == "c":
        fname = input("File to compress: ")
        start = time.time()
        compress_file(fname, fname + ".huf")
        print("Compressed {} in {} seconds."
              .format(fname, time.time() - start))
    elif mode == "d":
        fname = input("File to decompress: ")
        start = time.time()
        decompress_file(fname, fname + ".orig")
        print("Decompressed {} in {} seconds."
              .format(fname, time.time() - start))
