# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@uberdev.org>
# date: 2013/09/22
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

import pkg_resources, inspect, six

from .isstr import isstr

#------------------------------------------------------------------------------
def version(package, default=None):
  try:
    return pkg_resources.get_distribution(package).version
  except:
    return default

#------------------------------------------------------------------------------
def symbol(spec):
  if not isstr(spec):
    return spec
  if ':' in spec:
    spec, attr = spec.split(':', 1)
    return getattr(symbol(spec), attr)
  spec = spec.split('.')
  used = spec.pop(0)
  found = __import__(used)
  for cur in spec:
    used += '.' + cur
    try:
      found = getattr(found, cur)
    except AttributeError:
      __import__(used)
      found = getattr(found, cur)
  return found

#------------------------------------------------------------------------------
def caller(ignore=None):
  if ignore is None:
    ignore = []
  elif isinstance(ignore, basestring):
    ignore = [ignore]
  else:
    ignore = ignore[:]
  stack = inspect.stack()
  record = None
  one = False
  try:
    for record in stack:
      if not record or not record[0]:
        continue
      mod = inspect.getmodule(record[0])
      if not mod:
        continue
      mod = getattr(mod, '__package__', None) or getattr(mod, '__name__', None)
      if mod == 'asset' or mod.startswith('asset.'):
        continue
      if not one:
        # we've finally hit the module that actually called `caller`:
        # ignore it, since we need to return the caller's caller.
        one = True
        continue
      if mod not in ignore:
        return mod
    return None
  finally:
    del record
    del stack

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
