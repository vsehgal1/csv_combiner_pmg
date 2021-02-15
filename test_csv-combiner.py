# Sources referenced
# https://kapeli.com/cheat_sheets/Python_unittest_Assertions.docset/Contents/Resources/Documents/index
# https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.testing.assert_frame_equal.html


import CSVCombiner
import generatefixtures
import unittest
import io
import os
import pandas as pd
import sys


class TestCSVCombiner(unittest.TestCase):

    # Everytime tests are run new CSV files are generated to ensure random testing data.
    @classmethod
    def setUpClass(cls):
        generatefixtures.main()

    def setUp(self):
        self.captured = io.StringIO()
        sys.stdout = self.captured

    def open_output(self,num):
        self.test_csv = open('test'+num+'.csv', 'w+')

    def write_output(self):
        self.test_csv.write(self.captured.getvalue())
        self.test_csv.close()

    # Test argument validation with empty arguments passed inside CSVCombiner constructor.
    def test_arg_validation(self):
        combiner_1 = CSVCombiner.CSVCombiner()
        combiner_1.csv_combine()
        sys.stdout = sys.__stdout__
        self.assertEqual(self.captured.getvalue(),
                         'Please input correct arguments.')

        self.captured = io.StringIO()
        sys.stdout = self.captured
        combiner_1 = CSVCombiner.CSVCombiner([])
        combiner_1.csv_combine()
        sys.stdout = sys.__stdout__
        self.assertEqual(self.captured.getvalue(),
                         'Please input correct arguments.')

        self.captured = io.StringIO()
        sys.stdout = self.captured
        combiner_1 = CSVCombiner.CSVCombiner(['csv-combiner.py'])
        combiner_1.csv_combine()
        sys.stdout = sys.__stdout__
        self.assertEqual(self.captured.getvalue(),
                         'Please input correct arguments.')

    # Test path file validation with non existent csv passed as argument
    def test_path_validation(self):
        combiner_1 = CSVCombiner.CSVCombiner(
            ['csv-combiner.py', './fixtures/test_file.csv', ' ./fixtures/accessories.csv'])
        combiner_1.csv_combine()
        sys.stdout = sys.__stdout__
        self.assertEqual(self.captured.getvalue(),
                         'File: ./fixtures/test_file.csv not found.')

    # Test whether new column with correct file name has been added.
    def test_filename_feature(self):
        self.open_output('1')
        combiner_1 = CSVCombiner.CSVCombiner(
            ['csv-combiner.py', './fixtures/names.csv', './fixtures/accessories.csv'])
        combiner_1.csv_combine()
        sys.stdout = sys.__stdout__
        self.write_output()
        csv_table = pd.read_csv('test1.csv')
        self.assertIn('filename', csv_table.columns.values)
        self.assertIn('names.csv', list(csv_table['filename']))
        self.assertIn('accessories.csv', list(csv_table['filename']))

    # Test whether combined csv contains 2 csv passed inside the argument
    def test_combined_csv_2(self):
        self.open_output('2')
        combiner_1 = CSVCombiner.CSVCombiner(
            ['csv-combiner.py', './fixtures/names.csv', './fixtures/accessories.csv'])
        combiner_1.csv_combine()
        sys.stdout = sys.__stdout__
        self.write_output()

        names = pd.read_csv('./fixtures/names.csv')
        accessories = pd.read_csv('./fixtures/accessories.csv')
        output_csv = pd.read_csv('test2.csv')

        self.assertEqual(len(names)+len(accessories), len(output_csv))

        # Test for accessories csv
        output_accessories = output_csv.iloc[len(names):]
        del output_accessories['filename']
        output_accessories.index = pd.RangeIndex(
            len(output_accessories.index))
        pd.testing.assert_frame_equal(output_accessories, accessories)

        # Test for names csv
        output_names = output_csv.iloc[:-len(accessories)]
        del output_names['filename']
        output_names.index = pd.RangeIndex(
            len(output_names.index))
        pd.testing.assert_frame_equal(output_names, names)
    
    # Test whether combined csv contains 3 csv passed inside the argument
    def test_combined_csv_3(self):
        self.open_output('3')
        combiner_1 = CSVCombiner.CSVCombiner(
            ['csv-combiner.py', './fixtures/names.csv', './fixtures/accessories.csv', './fixtures/clothing.csv'])
        combiner_1.csv_combine()
        sys.stdout = sys.__stdout__
        self.write_output()

        names = pd.read_csv('./fixtures/names.csv')
        accessories = pd.read_csv('./fixtures/accessories.csv')
        clothing = pd.read_csv('./fixtures/clothing.csv')
        output_csv = pd.read_csv('test3.csv')

        self.assertEqual(len(names)+len(accessories)+len(clothing), len(output_csv))

       # Test for names csv
        output_names = output_csv.iloc[:len(names)]
        del output_names['filename']
        output_names.index = pd.RangeIndex(
            len(output_names.index))
        pd.testing.assert_frame_equal(output_names, names)

        # Test for accessories csv
        output_accessories = output_csv.iloc[len(names):-len(clothing)]
        del output_accessories['filename']
        output_accessories.index = pd.RangeIndex(
            len(output_accessories.index))
        pd.testing.assert_frame_equal(output_accessories, accessories)

        # Test for clothing csv
        output_clothing = output_csv.iloc[-len(clothing):]
        del output_clothing['filename']
        output_clothing.index = pd.RangeIndex(
            len(output_clothing.index))
        pd.testing.assert_frame_equal(output_accessories, accessories)
