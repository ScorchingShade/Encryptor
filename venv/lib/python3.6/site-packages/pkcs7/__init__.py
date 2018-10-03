#!/usr/bin/env python

import os
import sys

__version__ = "0.1.2"
__version_info__ = ( 0, 1, 2)


class PKCS7Encoder(object):
    '''
    RFC 2315: PKCS#7 page 21
    Some content-encryption algorithms assume the
    input length is a multiple of k octets, where k > 1, and
    let the application define a method for handling inputs
    whose lengths are not a multiple of k octets. For such
    algorithms, the method shall be to pad the input at the
    trailing end with k - (l mod k) octets all having value k -
    (l mod k), where l is the length of the input. In other
    words, the input is padded at the trailing end with one of
    the following strings:
             01 -- if l mod k = k-1
            02 02 -- if l mod k = k-2
                        .
                        .
                        .
          k k ... k k -- if l mod k = 0
    The padding can be removed unambiguously since all input is
    padded and no padding string is a suffix of another. This
    padding method is well-defined if and only if k < 256;
    methods for larger k are an open issue for further study.
    but we have the value
    '''
    def __init__(self, k=16):
        assert(k <= 256)
        assert(k > 1)
        self.__klen = k

    ## @param text The padded text for which the padding is to be removed.
    # @exception ValueError Raised when the input padding is missing or corrupt.
    def decode(self, text):
        dectext = ''
        if (len(text) % self.__klen) != 0:
            raise Exception('text not %d align'%(self.__klen))
        lastch = ord(text[-1])
        if lastch <= self.__klen and lastch != 0 :
            trimlen = lastch
            textlen = len(text)
            for i in range(lastch):
                if ord(text[textlen - i - 1]) != lastch:
                    trimlen = 0
                    break
            if trimlen == 0:
                dectext = text
            else:
                dectext = text[:(textlen-trimlen)]
        else:
            dectext = text
        return dectext

    def get_bytes(self,text):
        outbytes = []
        for c in text:
            outbytes.append(ord(c))
        return outbytes

    def get_text(self,inbytes):
        s = ''
        for i in inbytes:
            s += chr((i % 256))
        return s

    def __encode_inner(self,text):
        '''
        Pad an input string according to PKCS#7
        if the real text is bits same ,just expand the text
        '''
        totallen = len(text)
        passlen = 0
        enctext = ''
        if (len(text) % self.__klen) != 0:
            enctext = text
            leftlen = self.__klen - (len(text) % self.__klen)
            lastch = chr(leftlen)
            enctext += lastch * leftlen
        else:
            lastch = ord(text[-1])
            if lastch <= self.__klen and lastch != 0:
                trimlen = self.__klen
                textlen = len(text)
                for i in range(lastch):
                    if lastch != ord(text[(textlen-i-1)]):
                        trimlen = 0
                        break
                if trimlen == 0:
                    enctext = text
                else:
                    enctext = text
                    enctext += chr(self.__klen) * self.__klen
            else:
                enctext = text

        return enctext

    ## @param text The text to encode.
    def encode(self, text):
        return self.__encode_inner(text)


