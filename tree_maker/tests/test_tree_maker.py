import pytest
import tree_maker.NodeJob as nj
import tree_maker.tag as tag
from collections import OrderedDict

def test_method1():
	x = 1
	y = 2
	assert x + y == 3

def test_sum_is_five():
	assert nj.sum_is_five(1, 4) == True

def test_tag_first():
	tag.tag_first('example_file.yaml', 'hello')
	a = tag.read_yaml('example_file.yaml')
	b = tag.convert_to_dict(a)
	assert b['0']['tag'] == 'hello' 

def test_tag_it():
	tag.tag_first('example_file.yaml', 'hello')
	tag.tag_it('example_file.yaml', 'bonjour')
	a = tag.read_yaml('example_file.yaml')
	b = tag.convert_to_dict(a)
	assert b['1']['tag'] == 'bonjour'