# -*- coding: utf-8 -*-
"""
Created on Sun Jul 06 19:09:58 2014

@author: Morten
"""
from __future__ import division, absolute_import, print_function, unicode_literals
from anypytools.utils.py3k import * # @UnusedWildImport
import pytest
import numpy as np

from anypytools.generate_macros import MacroGenerator, MonteCarloMacroGenerator, LatinHyperCubeMacroGenerator

@pytest.yield_fixture()
def fixture():
    mg = MacroGenerator()
    yield mg

    
class TestMacroGenerator:

    def test_add_macro(self):
        mg = MacroGenerator()
        mg.add_macro(['load "main.any"', 'operation Main.RunApplication'])
        macro = mg.generate_macros()
        assert macro[0] == ['load "main.any"', 'operation Main.RunApplication']
    
    def test_set_value(self):
        mg = MacroGenerator()
        mg.add_set_value('val0', 23.1)
        mg.add_set_value('val1', -0.123010929395)
        mg.add_set_value('val2', "hallo world")
        mg.add_set_value(['val3','val4'], [3.0,4])
        mg.add_set_value('val5', np.array([1,2,3,4]) )
        mg.add_set_value('val6', np.array([[1,0],[0,1]]) )
        macro = mg.generate_macros()
        assert macro[0][0] == 'classoperation val0 "Set Value" --value="23.1"'
        assert macro[0][1] == 'classoperation val1 "Set Value" --value="-0.123010929395"'
        assert macro[0][2] == 'classoperation val2 "Set Value" --value="hallo world"'
        assert macro[0][3] == 'classoperation val3 "Set Value" --value="3"'
        assert macro[0][4] == 'classoperation val4 "Set Value" --value="4"'
        assert macro[0][5] == 'classoperation val5 "Set Value" --value="{1,2,3,4}"'
        assert macro[0][6] == 'classoperation val6 "Set Value" --value="{{1,0},{0,1}}"'
        
    def test_set_value_multiple(self):
        mg = MacroGenerator(number_of_macros = 3)
        mg.add_set_value('val0', [2,2.5,3])
        macros = mg.generate_macros()
        assert macros[0] == ['classoperation val0 "Set Value" --value="2"'] 
        assert macros[1] == ['classoperation val0 "Set Value" --value="2.5"'] 
        assert macros[2] == ['classoperation val0 "Set Value" --value="3"'] 

    def test_set_value_range(self):
        n_macros = 4
        mg = MacroGenerator(number_of_macros = n_macros)
        mg.add_set_value_range('testvar', 0, 3)
        macros = mg.generate_macros()
        assert macros[0] == ['classoperation testvar "Set Value" --value="0"']
        assert macros[-1] == ['classoperation testvar "Set Value" --value="3"']
        
        mg = MacroGenerator(number_of_macros = n_macros)
        mg.add_set_value_range('testvar',
                               start = np.array([[1.0,0.0],
                                                 [0.0, 1.5]]),
                               stop = np.array([[10.0,-0.5],
                                                [10.5,100.5]]) )
        macros = mg.generate_macros()
        assert macros[0] == ['classoperation testvar "Set Value" --value="{{1,0},{0,1.5}}"']
        assert macros[-1] == ['classoperation testvar "Set Value" --value="{{10,-0.5},{10.5,100.5}}"']



if __name__ == '__main__':
    import pytest
    pytest.main(str( 'test_generate_macros.py ../anypytools/generate_macros.py --doctest-modules'))    
