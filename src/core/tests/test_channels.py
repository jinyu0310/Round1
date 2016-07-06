# Copyright (c) 2016-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import core.serializer as serializer
import core.channels as channels


class TestChannels(unittest.TestCase):

    def testInputSerialization(self):
        slzr = serializer.StandardSerializer()
        ic = channels.InputChannel(slzr)
        test_string = 'my message'
        serialized_test_string = slzr.to_binary(test_string)

        def all_good(input_message):
            self.assertEqual(test_string[:len(input_message)], input_message)

        ic.message_updated.register(all_good)
        for b in serialized_test_string:
            ic.consume_bit(b)

    def testInputClear(self):
        slzr = serializer.StandardSerializer()
        ic = channels.InputChannel(slzr)
        test_string = 'my message'
        serialized_test_string = slzr.to_binary(test_string)
        for b in serialized_test_string:
            ic.consume_bit(b)

        def all_good(input_message):
            self.assertEqual('', input_message)

        ic.message_updated.register(all_good)
        ic.clear()

    def testOutputSerialization(self):
        slzr = serializer.StandardSerializer()
        oc = channels.OutputChannel(slzr)
        test_string = 'my message'
        serialized_test_string = slzr.to_binary(test_string)
        oc.set_message(test_string)
        for b in serialized_test_string:
            self.assertEqual(b, oc.consume_bit())

    def testConsistency(self):
        slzr = serializer.StandardSerializer()
        ic = channels.InputChannel(slzr)
        oc = channels.OutputChannel(slzr)
        test_string = 'my message'

        def all_good(input_message):
            self.assertEqual(test_string[:len(input_message)], input_message)

        oc.set_message(test_string)
        ic.message_updated.register(all_good)
        for b in oc.consume_bit():
            ic.consume_bit(b)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
