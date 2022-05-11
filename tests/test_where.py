# -*- coding: utf-8 -*-
import unittest

from djangopg.where import RelabeledWhereNode


class RelabeledWhereNodeTestCase(unittest.TestCase):

    def setUp(self):
        self.rwn = RelabeledWhereNode('my_table1',
                                      'SELECT * FROM %s', ['param1', 'param2'])

    def test_as_sql_with_params(self):
        self.assertEqual(self.rwn.as_sql(),
                         ('SELECT * FROM my_table1', ['param1', 'param2']))

    def test_relabel_aliases_with_change_map(self):
        self.rwn.relabel_aliases(change_map={'my_table1': 'my_table2'})
        self.assertEqual(self.rwn.table, 'my_table2')

    def test_as_sql_without_params(self):
        self.rwn.params = ''
        self.assertEqual(self.rwn.as_sql(),
                         ('SELECT * FROM my_table1', ()))
