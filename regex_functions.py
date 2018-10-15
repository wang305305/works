"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, Yining Wang, 2013, 2014,
2015, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.


def is_regex(s):
    '''(str) -> bool
    return whether it is a valid regex
    >>> is_regex('0')
    True
    >>> is_regex('21asjdncv')
    False
    >>> is_regex('e*')
    True
    >>> is_regex('1**')
    True
    >>> is_regex('*1')
    False
    >>> is_regex('((1.(0|2)*).0)')
    True
    >>> is_regex('((1.(0|2))*).0)')
    False
    '''
    degree = 0
    if len(s) == 1:
        # if length is 1, s can only be one of these to be a valid regex
        return (s in ['0', '1', '2', 'e'])
    elif s != "" and s[-1] == '*':
        # if s is end with "*", cut the star and check the rest of s
        return is_regex(s[:-1])
    # if s is in brackets
    elif s != "" and s[0] == "(" and s[-1] == ")":
        # find index of the dot or bar that's in the first brackets
        for i in range(len(s)):
            if s[i] == "(":
                degree += 1
            elif s[i] == ")":
                degree -= 1
            if degree == 1 and (s[i] == "." or s[i] == '|'):
                I = i
                # recursion: remove the two brackets
                # divide to 2 parts at the dot or bar found
                return is_regex(s[1:I]) and is_regex(s[I+1:-1])
    # if s is not in any of the form above return False
    return False


def all_regex_permutations(s):
    '''(str) -> set
    returns a set of strings that are possible permutation of the given string
    and are valid regexes
    >>>all_regex_permutations('(0|2)')
    set(['(2|0)', '(0|2)'])
    >>>all_regex_permutations("")
    set([])
    '''
    result = set()
    # loop through every permutation of the string
    for item in perms(s):
        if is_regex(item):
            # add the permutation into result set iff it is a valid regex
            result.add(item)
    return result


def perms(s):
    '''(str) -> set
    returns all permutations of the given string
    >>>perms("abc")
    set(['acb', 'cba', 'bca', 'abc', 'bac', 'cab'])
    >>>perms("a")
    set(['a'])
    >>>perms("")
    set([''])
    '''
    # if length is 0 or 1 return a set including only itself
    if len(s) < 2:
        return {s}
    res = set()
    # find all the permutation of the string with the first character removed
    for permutation in perms(s[1:]):
        for i in range(len(s)):
            # insert the first character in every place between characters
            res.add(permutation[:i] + s[0:1] + permutation[i:])
    return res


def regex_match(r, s):
    '''(RegexTree, str) -> bool
    returns True iff s matches the regex tree whose root is r
    >>>Tree = RegexTree
    >>>regex_match(build_regex_tree("(1.2)*"), "")
    True
    >>>regex_match(build_regex_tree("(1.2)*"), "1212")
    True
    >>>regex_match(build_regex_tree("(1.2)*"), "21")
    False
    >>>regex_match(build_regex_tree("(0|2)"), "2")
    True
    >>>regex_match(build_regex_tree("(0|2)"), "1")
    False
    '''
    # if the root is a Leaf
    if type(r) == Leaf:
        if symbol == "e":
            # "e" means ""
            return s == ""
        else:
            return s == symbol
    # if the root is star
    elif type(r) == StarTree:
        if s == "":
            return True


def build_regex_tree(regex):
    '''(str) -> RegexTree
    takes a string regex, build a regex tree, and returns the root of the tree
    >>>build_regex_tree("(1.2)") == RegexTree('.', [Leaf('1'), Leaf('2')])
    True
    >>>build_regex_tree("(1*|e)") == RegexTree('|', [StarTree(Leaf('1')), Leaf(
    'e')])
    True
    >>>build_regex_tree("(((e.1).2*)|((0***.e).(1|2*)))") == RegexTree('|', [
    RegexTree('.', [RegexTree('.', [Leaf('e'), Leaf('1')]), StarTree(Leaf(
    '2'))]), RegexTree('.', [RegexTree('.', [StarTree(StarTree(StarTree(Leaf(
    '0')))), Leaf('e')]), RegexTree('|', [Leaf('1'), StarTree(Leaf('2'))])])])
    True
    '''
    degree = 0
    # base case if length is 1,regex is a leaf since it does not have any child
    if len(regex) == 1:
        return Leaf(regex)
    # if it ends with a "*"
    elif regex != "" and regex[-1] == '*':
        # set the star to be the parent of a tree built with the rest of regex
        return StarTree(build_regex_tree(regex[:-1]))
    # if it is in brackets
    elif regex != "" and regex[0] == "(" and regex[-1] == ")":
        # loop and index of the dot or bar that's in the first brackets
        for i in range(len(regex)):
            if regex[i] == "(":
                degree += 1
            elif regex[i] == ")":
                degree -= 1
            if degree == 1 and (regex[i] == "." or regex[i] == '|'):
                I = i
                # recursion: remove the two brackets
                # divide to 2 parts at the dot or bar found and build trees
                # for each of the parts
                return RegexTree(regex[I], [build_regex_tree(
                    regex[1:I]), build_regex_tree(regex[I+1:-1])])
