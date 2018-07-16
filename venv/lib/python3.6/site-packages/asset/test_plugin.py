# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@metagriffin.net>
# date: 2016/01/03
# copy: (C) Copyright 2016-EOT metagriffin -- see LICENSE.txt
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

import unittest

from aadict import aadict

import asset

#------------------------------------------------------------------------------
class TestPlugins(unittest.TestCase):

  maxDiff = None

  @staticmethod
  @asset.plugin('test-group', 'test-name')
  def method(): pass

  #----------------------------------------------------------------------------
  def test_plugin_sorting_intra(self):
    from .plugin import _sort_plugins
    self.assertEqual(
      list(_sort_plugins('myext', [
        aadict(name='foo', after=None, before=None, order=8, replace=False, final=True),
        aadict(name='foo', after=None, before=None, order=2, replace=False, final=False),
        aadict(name='foo', after=None, before=None, order=9, replace=False, final=False),
        aadict(name='foo', after=None, before=None, order=5, replace=True,  final=False),
      ])), [
        aadict(name='foo', after=None, before=None, order=5, replace=True,  final=False),
        aadict(name='foo', after=None, before=None, order=8, replace=False, final=True),
      ])

  #----------------------------------------------------------------------------
  def test_plugin_sorting_inter(self):
    from .plugin import _sort_plugins
    self.assertEqual(
      list(_sort_plugins('myext', [
        aadict(name='a', after=None,  before=None, order=8, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=9, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='a', after='b',   before=None, order=5, replace=False, final=True),
        aadict(name='c', after=None,  before='a',  order=0, replace=False, final=False),
      ])), [
        aadict(name='b', after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='c', after=None,  before='a',  order=0, replace=False, final=False),
        aadict(name='a', after='b',   before=None, order=5, replace=False, final=True),
      ])

  #----------------------------------------------------------------------------
  def test_plugin_sorting_spec_valid(self):
    from .plugin import _sort_plugins
    self.assertEqual(
      list(_sort_plugins('myext', [
        aadict(name='a', after=None,  before=None, order=8, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=9, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='a', after='b',   before=None, order=5, replace=False, final=True),
        aadict(name='c', after=None,  before='a',  order=0, replace=False, final=False),
      ], 'c,b,a')), [
        aadict(name='c', after=None,  before='a',  order=0, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='a', after='b',   before=None, order=5, replace=False, final=True),
      ])
    self.assertEqual(
      list(_sort_plugins('myext', [
        aadict(name='a', after=None,  before=None, order=8, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=9, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='a', after='b',   before=None, order=5, replace=False, final=True),
        aadict(name='c', after=None,  before='a',  order=0, replace=False, final=False),
      ], '-c')), [
        aadict(name='b', after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='a', after='b',   before=None, order=5, replace=False, final=True),
      ])

  #----------------------------------------------------------------------------
  def test_plugin_sorting_spec_invalid(self):
    from .plugin import _sort_plugins
    with self.assertRaises(TypeError) as cm:
      list(_sort_plugins('myext', [
        aadict(name='a', after=None,  before=None, order=8, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=9, replace=False, final=False),
        aadict(name='b', after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='a', after='b',   before=None, order=5, replace=False, final=True),
        aadict(name='c', after=None,  before='a',  order=0, replace=False, final=False),
      ], '-c,-b'))
    self.assertEqual(
      str(cm.exception),
      "myext plugin type 'a' specified unavailable 'after' dependency 'b'")

  #----------------------------------------------------------------------------
  def test_plugin_sorting_unavailable(self):
    from .plugin import _sort_plugins
    with self.assertRaises(TypeError) as cm:
      list(_sort_plugins('myext', [
        aadict(name='bar', after='foo', before=None, order=0, replace=False, final=False),
      ]))
    self.assertEqual(
      str(cm.exception),
      "myext plugin type 'bar' specified unavailable 'after' dependency 'foo'")
    with self.assertRaises(TypeError) as cm:
      list(_sort_plugins('myext', [
        aadict(name='bar', after=None, before='foo', order=0, replace=False, final=False),
      ]))
    self.assertEqual(
      str(cm.exception),
      "myext plugin type 'bar' specified unavailable 'before' dependency 'foo'")
    with self.assertRaises(TypeError) as cm:
      list(_sort_plugins('myext', [
        aadict(name='foo', after=None, before='bar', order=0, replace=False, final=False),
        aadict(name='bar', after=None, before='foo', order=0, replace=False, final=False),
      ]))
    self.assertEqual(
      str(cm.exception),
      "myext has cyclical dependencies in plugins ['bar', 'foo']")

  #----------------------------------------------------------------------------
  def test_plugin_spec_valid(self):
    import re
    from .plugin import _parse_spec
    self.assertEqual(_parse_spec(None), ())
    self.assertEqual(_parse_spec('*'), ())
    self.assertEqual(_parse_spec('-foo,+bar'), (aadict(op='-', target='foo'), aadict(op='+', target='bar')))
    self.assertEqual(_parse_spec('-foo,-bar'), (aadict(op='-', target='foo'), aadict(op='-', target='bar')))
    self.assertEqual(_parse_spec(' - foo, - bar'), (aadict(op='-', target='foo'), aadict(op='-', target='bar')))
    self.assertEqual(_parse_spec(' - foo - bar '), (aadict(op='-', target='foo'), aadict(op='-', target='bar')))
    self.assertEqual(_parse_spec('foo,?bar'), (aadict(op=' ', target='foo'), aadict(op='?', target='bar')))
    self.assertEqual(_parse_spec('foo,?bar'), (aadict(op=' ', target='foo'), aadict(op='?', target='bar')))
    self.assertEqual(
      _parse_spec('/(foo|bar)/'),
      (aadict(op='/', target=re.compile('(foo|bar)')),))
    self.assertEqual(
      _parse_spec('+zig,/(foo|bar)/'),
      (aadict(op='+', target='zig'), aadict(op='/', target=re.compile('(foo|bar)'))))
    self.assertEqual(
      _parse_spec('/zig,/(foo|bar)/'),
      (aadict(op='/', target=re.compile('zig,/(foo|bar)')),))

  #----------------------------------------------------------------------------
  def test_plugin_spec_invalid(self):
    from .plugin import _parse_spec
    with self.assertRaises(ValueError) as cm:
      _parse_spec('foo,-bar')
    self.assertEqual(
      str(cm.exception),
      "invalid mixing of relative (['-']) and absolute ([' ']) prefixes in plugin specification")
    with self.assertRaises(ValueError) as cm:
      _parse_spec('-foo,bar')
    self.assertEqual(
      str(cm.exception),
      "invalid mixing of relative (['-']) and absolute ([' ']) prefixes in plugin specification")
    with self.assertRaises(ValueError) as cm:
      _parse_spec('-foo,?bar')
    self.assertEqual(
      str(cm.exception),
      "invalid mixing of relative (['-']) and absolute (['?']) prefixes in plugin specification")
    with self.assertRaises(ValueError) as cm:
      _parse_spec('/foo')
    self.assertEqual(
      str(cm.exception),
      'regex plugin loading expression must start and end with "/"')

  #----------------------------------------------------------------------------
  def test_plugin_spec_match(self):
    from .plugin import _parse_spec, _match_spec
    self.assertTrue(_match_spec(_parse_spec('*'), 'foo'))
    self.assertTrue(_match_spec(_parse_spec('/foo/'), 'foo'))
    self.assertFalse(_match_spec(_parse_spec('/foo/'), 'bar'))
    self.assertTrue(_match_spec(_parse_spec('/(foo|bar)/'), 'foo'))
    self.assertTrue(_match_spec(_parse_spec('/(foo|bar)/'), 'bar'))
    self.assertTrue(_match_spec(_parse_spec('foo,?bar'), 'foo'))
    self.assertTrue(_match_spec(_parse_spec('foo,?bar'), 'bar'))
    self.assertTrue(_match_spec(_parse_spec('-foo'), 'bar'))
    self.assertFalse(_match_spec(_parse_spec('-foo'), 'foo'))
    self.assertFalse(_match_spec(_parse_spec('foo,?bar'), 'zog'))
    self.assertTrue(_match_spec(_parse_spec('+foo'), 'foo'))
    self.assertTrue(_match_spec(_parse_spec('+foo'), 'bar'))

  #----------------------------------------------------------------------------
  def test_plugin_asset_load(self):
    from .plugin import plugins, _load_asset_plugin
    self.assertEqual(
      _load_asset_plugin(aadict(target='asset.test_plugin.TestPlugins.method')).handle,
      self.method)
    plugs = list(plugins('test-group', 'asset.test_plugin.TestPlugins.method'))
    self.assertEqual(
      [plin.handle for plin in plugs],
      [self.method])
    with self.assertRaises(ValueError) as cm:
      list(plugins('test-group', 'asset.test_plugin.TestPlugins.no_such_method'))
    self.assertEqual(
      str(cm.exception),
      "could not load plugin 'asset.test_plugin.TestPlugins.no_such_method'")

  #----------------------------------------------------------------------------
  def test_plugin_asset_mixed(self):
    from .plugin import _sort_plugins
    self.assertEqual(
      list(_sort_plugins('myext', [
        aadict(name='a',   after=None,  before=None, order=8, replace=False, final=False),
        aadict(name='b',   after=None,  before=None, order=9, replace=False, final=False),
        aadict(name='b',   after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='a',   after='b',   before=None, order=5, replace=False, final=True),
        aadict(name='c',   after=None,  before='b',  order=0, replace=False, final=False),
        aadict(name='d.e', after='b',   before='a',  order=0, replace=False, final=False),
      ], '+d.e')), [
        aadict(name='c',   after=None,  before='b',  order=0, replace=False, final=False),
        aadict(name='b',   after=None,  before=None, order=2, replace=False, final=True),
        aadict(name='d.e', after='b',   before='a',  order=0, replace=False, final=False),
        aadict(name='a',   after='b',   before=None, order=5, replace=False, final=True),
      ])

  #----------------------------------------------------------------------------
  def test_plugin_decorator(self):
    from .plugin import plugin
    @plugin('asset.example', 'foo', before='bar')
    def my_foo_plugin(): pass
    @plugin('asset.example', 'bar', after='foo', order=3, replace=True, final=True)
    def my_bar_plugin(): pass
    self.assertEqual(my_foo_plugin.plugin_group, 'asset.example')
    self.assertEqual(my_foo_plugin.plugin_name, 'foo')
    self.assertEqual(my_foo_plugin.before, 'bar')
    self.assertFalse(hasattr(my_foo_plugin, 'after'))
    self.assertFalse(hasattr(my_foo_plugin, 'order'))
    self.assertFalse(hasattr(my_foo_plugin, 'replace'))
    self.assertFalse(hasattr(my_foo_plugin, 'final'))
    self.assertEqual(my_bar_plugin.plugin_group, 'asset.example')
    self.assertEqual(my_bar_plugin.plugin_name, 'bar')
    self.assertEqual(my_bar_plugin.after, 'foo')
    self.assertFalse(hasattr(my_bar_plugin, 'before'))
    self.assertEqual(my_bar_plugin.order, 3)
    self.assertEqual(my_bar_plugin.replace, True)
    self.assertEqual(my_bar_plugin.final, True)

  #----------------------------------------------------------------------------
  def test_plugin_can_declare_name(self):
    pset = asset.plugins(
      'test-group', 'asset.test_plugin.TestPlugins.method')
    self.assertEqual(pset.plugins[0].name, 'test-name')

#------------------------------------------------------------------------------
class TestPluginSet(unittest.TestCase):

  maxDiff = None

  @staticmethod
  def increment(value, counter=None, **kw):
    if counter:
      counter()
    if 'abort' in kw and value == kw['abort']:
      return None
    if value is None:
      return None
    return value + 1

  @staticmethod
  @asset.plugin('test-group', 'decrement')
  def decrement(value):
    return value - 1

  #----------------------------------------------------------------------------
  def test_filter_empty(self):
    self.assertEqual(
      'foo',
      asset.PluginSet('group', None, []).filter('foo'))

  #----------------------------------------------------------------------------
  def test_handle_empty(self):
    with self.assertRaises(ValueError) as cm:
      asset.PluginSet('group', None, []).handle('foo')
    self.assertEqual(
      str(cm.exception), "No plugins available in group 'group'")

  #----------------------------------------------------------------------------
  def test_filter_aborts(self):
    count = dict(value=0)
    def counter():
      count['value'] = count['value'] + 1
    pset = asset.plugins(
      'test-group', ','.join(['asset.test_plugin.TestPluginSet.increment'] * 5))
    self.assertEqual(pset.filter(0, abort=2, counter=counter), None)
    self.assertEqual(count['value'], 3)

  #----------------------------------------------------------------------------
  def test_handle_perseveres(self):
    count = dict(value=0)
    def counter():
      count['value'] = count['value'] + 1
    pset = asset.plugins(
      'test-group', ','.join(['asset.test_plugin.TestPluginSet.increment'] * 5))
    self.assertEqual(pset.handle(0, abort=2, counter=counter), None)
    self.assertEqual(count['value'], 5)

  #----------------------------------------------------------------------------
  def test_select(self):
    pset = asset.plugins(
      'test-group', ','.join([
          'asset.test_plugin.TestPluginSet.increment',
          'asset.test_plugin.TestPluginSet.decrement']))
    pset2 = pset.select('decrement')
    self.assertEqual(
      [p.handle for p in pset.plugins], [self.increment, self.decrement])
    self.assertEqual(
      [p.handle for p in pset2.plugins], [self.decrement])

  #----------------------------------------------------------------------------
  def test_repr(self):
    self.assertEqual(
      repr(asset.plugins(
          'test-group', 'asset.test_plugin.TestPluginSet.decrement')),
      "<PluginSet group='test-group' plugins=['decrement']>")


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
