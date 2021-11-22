import unittest

import pandas as pd

from main import segregate_by_column


class TestSegregateByColumn(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.DataFrame(data={'column1': [1,2,3,4,5,6], 'column2': list('ABCABC')})
        self.by_column = 'column2'
        self.data_segregated_by_column = segregate_by_column(data=self.data, column=self.by_column)
    
    def test_segregate_by_column_return_datatype(self) -> None:
        self.assertIsInstance(self.data_segregated_by_column, dict)
    
    def test_segregate_by_column_num_items(self) -> None:
        self.assertEquals(len(self.data_segregated_by_column), self.data[self.by_column].nunique())
    
    def test_segregate_by_column_keys(self) -> None:
        self.assertEquals(self.data[self.by_column].unique().tolist(), list(self.data_segregated_by_column.keys()))
    
    def test_segregate_by_column_lengths(self) -> None:
        length = 0
        for _, dataframe in self.data_segregated_by_column.items():
            length += len(dataframe)
        self.assertEquals(length, len(self.data))


if __name__ == "__main__":
    unittest.main()