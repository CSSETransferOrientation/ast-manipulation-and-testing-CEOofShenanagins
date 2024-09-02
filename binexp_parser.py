#!/usr/bin/python3
import os
from os.path import join as osjoin
import unittest
from enum import Enum

NodeType = Enum('BinOpNodeType', ['number', 'operator'])

class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """
    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """
        if prefix_list:
            self.val = prefix_list.pop(0)
            if self.val.isnumeric():
                self.type = NodeType.number
                self.left = False
                self.right = False
            else:
                self.type = NodeType.operator
                self.left = BinOpAst(prefix_list)
                self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def additive_identity(self):
        """
        Reduce additive identities
        x + 0 = x
        """
        if (self.val == '+'): 
            #If left is zero, assign right value/type/left/right to self
            if self.left.val.isnumeric() and int(self.left.val) == 0:
                self.val = self.right.val
                self.type = self.right.type
                #if operator, carry over left/right values
                if self.right.type == NodeType.operator:
                    self.left = self.right.left
                    self.right = self.right.right 
                else:
                    self.left = False
                    self.right = False

            # if right is zero, assign left values to self
            elif self.right.val.isnumeric() and int(self.right.val) == 0:
                self.val = self.left.val
                self.type = self.left.type
                #if operator, carry over left/right values
                if self.left.type == NodeType.operator:
                    self.left = self.left.left
                    self.right = self.left.right 
                else:
                    self.left = False
                    self.right = False
         
    def multiplicative_identity(self):
        """
        Reduce multiplicative identities
        x * 1 = x
        """
        if (self.val == '*'): 
            #if left = 1, assign right value to self
            if self.left.val.isnumeric() and int(self.left.val) == 1:
                self.val = self.right.val
                self.type = self.right.type
                #if operator, carry over left/right values
                if self.right.type == NodeType.operator:
                    self.left = self.right.left
                    self.right = self.right.right 
                else:
                    self.left = False
                    self.right = False
            #if right = 1, assign left value to self 
            elif self.right.val.isnumeric() and int(self.right.val) == 1:
                self.val = self.left.val
                self.type = self.left.type
                #if operator, carry over left/right values
                if self.left.type == NodeType.operator:
                    self.left = self.left.left
                    self.right = self.left.right 
                else:
                    self.left = False
                    self.right = False
    
    def mult_by_zero(self):
        """
        Reduce multiplication by zero
        x * 0 = 0
        """
        if (self.val == '*'): 
            if (self.left.val.isnumeric() and int(self.left.val) == 0) or (self.right.val.isnumeric() and int(self.right.val) == 0):
                self.val = '0'
                self.type = NodeType.number
                self.left = False
                self.right = False          

    def simplify_binops(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        # The individual functions should recur, you aren't testing each individually like this
        if self.left.type == NodeType.operator:
            self.left.simplify_binops()
        if self.right.type == NodeType.operator:
            self.right.simplify_binops()
        self.additive_identity()
        self.multiplicative_identity()
        #self.mult_by_zero()
        #self.constant_fold()


class Test_BinOps(unittest.TestCase):
    def test_arith_id(self):
        self.generic_test('arith_id')
                    
    def test_mult_id (self):
        self.generic_test('mult_id')

    def generic_test (self, folder_name):
        ins = osjoin('testbench', folder_name, 'inputs')
        outs = osjoin('testbench', folder_name, 'outputs')
        for fname in os.listdir(ins):
            with open(osjoin(ins, fname)) as inputs_file, open(osjoin(outs, fname)) as outputs_file:
                for in_line, out_line in zip(inputs_file.readlines(), outputs_file.readlines()):
                    input_list = in_line.strip().split(" ")
                    AST = BinOpAst(input_list)
                    AST.simplify_binops()
                    prefix = AST.prefix_str()
                    self.assertEqual(prefix, out_line.strip())

if __name__ == "__main__":
    unittest.main()
