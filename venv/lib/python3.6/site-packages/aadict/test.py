# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@uberdev.org>
# date: 2013/10/19
# copy: (C) Copyright 2013-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import unittest, pickle

from aadict import aadict

#------------------------------------------------------------------------------
class TestAadict(unittest.TestCase):

  #----------------------------------------------------------------------------
  def test_base(self):
    d = aadict(foo='bar', zig=87)
    self.assertEqual(d.foo, 'bar')
    self.assertEqual(d['foo'], 'bar')

  #----------------------------------------------------------------------------
  def test_chaining_update(self):
    d = aadict(foo='bar', zig=87)
    d2 = aadict(x='y').update(d).omit('zig')
    self.assertEqual(d2.x, 'y')
    self.assertEqual(d2.foo, 'bar')
    self.assertIsNone(d2.zig)

  #----------------------------------------------------------------------------
  def test_chaining_clear(self):
    d = aadict(foo='bar', zig=87).clear().update(zag='zug')
    self.assertEqual(d, {'zag': 'zug'})

  #----------------------------------------------------------------------------
  def test_convert(self):
    d = aadict.d2ar(dict(foo=dict(bar='zig')))
    self.assertEqual(d.foo.bar, 'zig')
    d = aadict.d2a(dict(foo=dict(bar='zig')))
    with self.assertRaises(AttributeError):
      zig = d.foo.bar
      self.fail('AttributeError should have been raised')

  #----------------------------------------------------------------------------
  def test_pickle(self):
    d = aadict(foo='bar', zig=87)
    d2 = pickle.loads(pickle.dumps(d))
    self.assertTrue(isinstance(d2, aadict))
    self.assertEqual(d2, d)
    self.assertEqual(d2['foo'], 'bar')
    self.assertEqual(d2.foo, 'bar')

  #----------------------------------------------------------------------------
  def test_dir(self):
    d1 = dict()
    d2 = aadict(foo='bar', zig=87)
    ignore = set(['__weakref__', '__module__', '__dict2aadict__', '__dict__'])
    self.assertEqual(
      set(sorted(dir(d2))) - ignore,
      set(sorted(dir(d1) + [
        '__getattr__', '__setattr__', '__delattr__', '__dir__',
        'pick', 'omit', 'd2a', 'd2ar',
        'foo', 'zig',
        ])) - ignore)

  #----------------------------------------------------------------------------
  def test_ctor_cloneupdate(self):
    d1 = aadict(foo='bar', zig=87)
    d2 = aadict(d1, zig=99, zag='zog')
    self.assertEqual(d1, dict(foo='bar', zig=87))
    self.assertEqual(d2, dict(foo='bar', zig=99, zag='zog'))


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
