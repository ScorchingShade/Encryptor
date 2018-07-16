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

import re
import os
import functools

import pkg_resources
import six
import globre

from .symbol import symbol

#------------------------------------------------------------------------------

MAXBUF = 8192

#------------------------------------------------------------------------------
class NoSuchAsset(Exception): pass


#------------------------------------------------------------------------------
class AssetGroupStream(object):
  # TODO: implement all expected file-like methods...
  def __init__(self, group):
    self.group  = group
    self.assets = iter(group)
    self._cur   = None
  def read(self, size=-1):
    ret = b'' if self._cur is None else self._cur.read(size)
    if size >= 0 and len(ret) >= size:
      return ret
    while True:
      try:
        self._cur = six.next(self.assets)
      except StopIteration:
        self._cur = None
        return ret
      ret += self._cur.read(( size - len(ret) ) if size > 0 else -1)
      if size >= 0 and len(ret) >= size:
        return ret
  def readline(self):
    if self._cur is None:
      try:
        self._cur = six.next(self.assets)
      except StopIteration:
        self._cur = None
        return b''
    while True:
      ret = self._cur.readline()
      if ret:
        return ret
      try:
        self._cur = six.next(self.assets)
      except StopIteration:
        self._cur = None
        return b''
  def chunks(self, *args, **kws):
    return chunks(self, *args, **kws)
  def close(self):
    pass
  def __iter__(self):
    while True:
      line = self.readline()
      if not line:
        return
      yield line


#------------------------------------------------------------------------------
class AssetGroup(object):
  # TODO: implement all expected file-like methods...
  def __init__(self, package, package_dir, regex, spec):
    # todo: remove `package_dir` -- it should be inferred...
    self.package = package
    self.pkgdir  = package_dir
    self.regex   = regex
    self.spec    = spec
    self._fp     = None
  def peek(self):
    for pkg, res in self.resources():
      return self
  def count(self):
    return len(self)
  def exists(self):
    try:
      self.peek()
      return True
    except NoSuchAsset:
      return False
  def resources(self):
    count = 0
    for resource in listres(self.package, self.pkgdir):
      if not self.regex.match(resource):
        continue
      count += 1
      yield (self.package, resource)
    if count <= 0:
      raise NoSuchAsset('No asset matched "%s"' % (self.spec,))
  def chunks(self, *args, **kws):
    return self._stream().chunks(*args, **kws)
  def __len__(self):
    return len(list(self.resources()))
  def __iter__(self):
    for pkg, res in self.resources():
      yield Asset(self, pkg, res)
  def stream(self):
    return AssetGroupStream(self)
  def _stream(self):
    if self._fp is None:
      self._fp = self.stream()
    return self._fp
  def read(self, size=-1):
    return self._stream().read(size)
  def readline(self):
    return self._stream().readline()


#------------------------------------------------------------------------------
class AssetStream(object):
  # TODO: implement all expected file-like methods...
  def __init__(self, stream, asset):
    self.stream = stream
    self.asset  = asset
  def read(self, size=-1):
    return self.stream.read(size)
  def readline(self):
    return self.stream.readline()
  def close(self):
    pass
  def chunks(self, *args, **kws):
    return chunks(self.stream, *args, **kws)
  def __iter__(self):
    while True:
      line = self.readline()
      if not line:
        return
      yield line


#------------------------------------------------------------------------------
class Asset(object):
  # todo: should all returned streams be "AssetStream"s that provide
  #       a .asset attribute, like TransformerStream does?
  # TODO: implement all expected file-like methods...
  def __init__(self, group, package, name):
    self.group   = group
    self.package = package
    self.name    = name
    self._fp     = None
  def __str__(self):
    return '%s:%s' % (self.package, self.name)
  def stream(self):
    return AssetStream(
      pkg_resources.resource_stream(self.package, self.name), self)
  def _stream(self):
    if self._fp is None:
      self._fp = self.stream()
    return self._fp
  def read(self, size=-1):
    return self._stream().read(size)
  def readline(self):
    return self._stream().readline()
  # compatibility with AssetGroup() API...
  def peek(self):
    if pkg_resources.resource_exists(self.package, self.name):
      return self
    raise NoSuchAsset('No asset matched "%s:%s"' % (self.package, self.name))
  def count(self):
    return len(self)
  def exists(self):
    try:
      self.peek()
      return True
    except NoSuchAsset:
      return False
  def resources(self):
    self.peek()
    yield (self.package, self.name)
  def chunks(self, *args, **kws):
    return self._stream().chunks(*args, **kws)
  def __len__(self):
    self.peek()
    return 1
  def __iter__(self):
    self.peek()
    yield self
  def __repr__(self):
    return '<asset "{}:{}">'.format(self.package, self.name)
  @property
  def filename(self):
    prov = pkg_resources.get_provider(self.package)
    if isinstance(prov, pkg_resources.ZipProvider):
      return None
    return pkg_resources.resource_filename(self.package, self.name)


defaultExclude = ('.rcs', '.svn', '.git', '.hg')

#------------------------------------------------------------------------------
def listres(pkgname, pkgdir,
            recursive=True, depthFirst=False,
            exclude=defaultExclude, showDirs=False,
            ):
  reslist = [os.path.join(pkgdir, cur)
             for cur in pkg_resources.resource_listdir(pkgname, pkgdir)
             if cur not in exclude]
  dirs = []
  for cur in sorted(reslist):
    if pkg_resources.resource_isdir(pkgname, cur):
      if showDirs:
        yield cur + '/'
      if recursive:
        if depthFirst:
          for subcur in listres(pkgname, cur):
            yield subcur
        else:
          dirs.append(cur)
    else:
      yield cur
  for cur in dirs:
    for subcur in listres(pkgname, cur):
      yield subcur

#------------------------------------------------------------------------------
def load(pattern, *args, **kw):
  '''
  Given a package asset-spec glob-pattern `pattern`, returns an
  :class:`AssetGroup` object, which in turn can act as a generator of
  :class:`Asset` objects that match the pattern.

  Example:

  .. code-block:: python

    import asset

    # concatenate all 'css' files into one string:
    css = asset.load('mypackage:static/style/**.css').read()

  '''

  spec = pattern

  if ':' not in pattern:
    raise ValueError('`pattern` must be in the format "PACKAGE:GLOB"')

  pkgname, pkgpat = pattern.split(':', 1)
  pkgdir, pattern = globre.compile(pkgpat, split_prefix=True, flags=globre.EXACT)

  if pkgdir:
    idx = pkgdir.rfind('/')
    pkgdir = pkgdir[:idx] if idx >= 0 else ''

  group = AssetGroup(pkgname, pkgdir, pattern, spec)
  if globre.iswild(pkgpat):
    return group
  return Asset(group, pkgname, pkgpat)

#------------------------------------------------------------------------------
def chunks(stream, size=None):
  '''
  Returns a generator of chunks from the `stream` with a maximum
  size of `size`. I don't know why this isn't part of core Python.

  :Parameters:

  stream : file-like object

    The stream to fetch the chunks from. Note that the stream will
    not be repositioned in any way.

  size : int | 'lines'; default: null

    If a integer, the size of the chunks to return. If the
    string ``"lines"``, then behaves the same as `file.read()`.
    If unspecified or null, defaults to the package default
    MAXBUF size (usually 8 KiB).
  '''
  if size == 'lines':
    for item in stream:
    # for item in stream.readline():
      yield item
    return
  if size is None:
    size = MAXBUF
  while True:
    buf = stream.read(size)
    if not buf:
      return
    yield buf

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
