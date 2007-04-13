#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2005 Shuttleworth Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Unit tests for schooltool.batching.batch

$Id$
"""

import unittest

from zope.testing import doctest

def doctest_Batch():
    """Test for Batch.

    Batching lets us split up a large list of information into smaller, more
    presentable lists.

    First we'll create a set of junk information that we can play with.

      >>> testData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    Now we can feed this to our Batch class.

      >>> from schooltool.batching.batch import Batch
      >>> batch = Batch(testData, 0, 3)

    Our 'batch' instance is now loaded up with our testData. The batch starts
    at the first element in the testData list and holds the first 3 items:

      >>> [item for item in batch]
      [1, 2, 3]
      >>> len(batch)
      3

    We can also fetch the first and last items in the batch which can be useful
    when building page navigation (if your list is sorted):

      >>> batch.first()
      1
      >>> batch.last()
      3

    We can also see how many batches it will take to cover our list of 14 items

      >>> batch.numBatches()
      5

    Note that the the starting point for the batch is irrelevant when
    calcualting how many batches are required for a list:

      >>> batch = Batch(testData, 10, 3)
      >>> batch.numBatches()
      5

    We can also see if an item is in our batch.  With our starting point at the
    10th item ('11'), '11' should be in our batch but '1' should not:

      >>> [item for item in batch]
      [11, 12, 13]
      >>> 11 in batch
      True
      >>> 1 in batch
      False

    Batches are navigated through the prev() and next() methods:

      >>> batch.start
      10
      >>> nbatch = batch.next()
      >>> nbatch.start
      13
      >>> pbatch = batch.prev()
      >>> pbatch.start
      7

    Given any batch in a set we can tell what position the batch is in relative
    to the set:

      >>> nbatch.num()
      5
      >>> batch.num()
      4
      >>> pbatch.num()
      3

    It's also important that our batches don't overlap

      >>> [item for item in pbatch]
      [8, 9, 10]
      >>> [item for item in batch]
      [11, 12, 13]
      >>> [item for item in nbatch]
      [14]

    If there is no previous or next batch, we get None:

      >>> batch = Batch(testData, 0, 10)
      >>> print batch.prev()
      None

      >>> batch = Batch(testData, len(testData) - 1, 10)
      >>> [item for item in batch]
      [14]
      >>> print batch.next()
      None

    We can also comapre two batches to see if they are or are not equal:

      >>> batch1 = Batch(testData, 0, 10)
      >>> batch2 = Batch(testData, 0, 10)
      >>> batch1 == batch2
      True
      >>> batch1 != batch2
      False

      >>> batch1 = batch1.next()
      >>> batch1 == batch2
      False
      >>> batch1 != batch2
      True

      >>> batch2 = batch2.next()
      >>> batch1 == batch2
      True
      >>> batch1 != batch2
      False

    We can also loop through the urls for all the batches using the
    batch_urls() method:

      >>> batch = Batch(testData, 0, 3)
      >>> from zope.testing.doctestunit import pprint
      >>> pprint(batch.batch_urls("base_url.html", "&extra_info=True"))
      [{'class': 'current',
        'href': 'base_url.html?batch_start=0&batch_size=3&extra_info=True',
        'num': 1},
       {'class': None,
        'href': 'base_url.html?batch_start=3&batch_size=3&extra_info=True',
        'num': 2},
       {'class': None,
        'href': 'base_url.html?batch_start=6&batch_size=3&extra_info=True',
        'num': 3},
       {'class': None,
        'href': 'base_url.html?batch_start=9&batch_size=3&extra_info=True',
        'num': 4},
       {'class': None,
        'href': 'base_url.html?batch_start=12&batch_size=3&extra_info=True',
        'num': 5}]

    If we pass the name of the batch we get it built into the url:

      >>> pprint(batch.batch_urls("base_url.html", "&extra_info=True", "b1"))
      [{'class': 'current',
        'href': 'base_url.html?batch_start.b1=0&batch_size.b1=3&extra_info=True',
        'num': 1},
       {'class': None,
        'href': 'base_url.html?batch_start.b1=3&batch_size.b1=3&extra_info=True',
        'num': 2},
       {'class': None,
        'href': 'base_url.html?batch_start.b1=6&batch_size.b1=3&extra_info=True',
        'num': 3},
       {'class': None,
        'href': 'base_url.html?batch_start.b1=9&batch_size.b1=3&extra_info=True',
        'num': 4},
       {'class': None,
        'href': 'base_url.html?batch_start.b1=12&batch_size.b1=3&extra_info=True',
        'num': 5}]


    By default, items are presented in the same order they are passed to Batch

      >>> class Foo(object):
      ...   def __init__(self, val):
      ...     self.title = val

      >>> data = [Foo('aaa'), Foo('zzz'), Foo('ccc'), Foo('mmm')]
      >>> batch = Batch(data, 0, 2)

      >>> [item.title for item in batch.list]
      ['aaa', 'zzz', 'ccc', 'mmm']

    If we pass an attribute name to the constructor we can sort our batch

      >>> batch = Batch(data, 0, 2, sort_by='title')
      >>> [item.title for item in batch.list]
      ['aaa', 'ccc', 'mmm', 'zzz']

    We can also sort dicts

      >>> dict_data = [{'n': i} for i in range(6)]
      >>> dict_data = dict_data[3:] + dict_data[:3]
      >>> print dict_data
      [{'n': 3}, {'n': 4}, {'n': 5}, {'n': 0}, {'n': 1}, {'n': 2}]

      >>> batch = Batch(dict_data, 0, 2, sort_by='n')
      >>> [item for item in batch.list]
      [{'n': 0}, {'n': 1}, {'n': 2}, {'n': 3}, {'n': 4}, {'n': 5}]


    We can also take an iterator

      >>> batch = Batch(iter([i for i in range(10)]), 0, 5)
      >>> [item for item in batch.list]
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    """

def test_suite():
    return unittest.TestSuite([
                doctest.DocTestSuite(optionflags=doctest.ELLIPSIS),
                doctest.DocTestSuite('schooltool.batching.batch'),
           ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
