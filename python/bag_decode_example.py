#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Copyright 2022 Bernd Pfrommer <bernd.pfrommer@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
"""
example python decoding from rosbag
decoding courtesy of Ken Chaney 2022
"""

import rosbag
import argparse
import numpy as np
import time


def read_bag(args):
    print(f'reading bag {args.bag}')
    bag = rosbag.Bag(args.bag)
    t0 = None
    start_time = time.time()
    num_events = 0
    num_msgs = 0
    for topic, msg, t_rec in bag.read_messages(topics=[args.topic]):
        time_base = msg.time_base \
            if args.use_sensor_time else msg.header.stamp.to_nsec()
        # unpack all events in the message
        packed = np.frombuffer(msg.events, dtype=np.uint64)
        y = np.bitwise_and(
            np.right_shift(packed, 48), 0x7FFF).astype(np.uint16)
        x = np.bitwise_and(
            np.right_shift(packed, 32), 0xFFFF).astype(np.uint16)
        t = np.bitwise_and(packed, 0xFFFFFFFF) + time_base
        p = np.right_shift(packed, 63).astype(np.uint16)
        if not t0:
            t0 = msg.header.stamp.to_nsec()
        t_adj = t if args.use_sensor_time else (t - t0)
        a = np.stack((t_adj * 1e-9, x, y, p), axis=-1)
        # print(a)
        num_events += t.shape[0]
        num_msgs += 1
    dt = time.time() - start_time
    print(f'processed {num_msgs / dt} msgs/s, {num_events * 1e-6 / dt} Mev/s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='read and decode events from bag.')
    parser.add_argument('--bag', '-b', action='store', default=None,
                        required=True, help='bag file to read events from')
    parser.add_argument('--topic', help='Event topic to read',
                        default='/event_camera/events', type=str)
    parser.add_argument('--use_sensor_time', dest='use_sensor_time',
                        action='store_true')
    parser.add_argument('--dont_use_sensor_time', dest='use_sensor_time',
                        action='store_false')
    parser.set_defaults(use_sensor_time=False)
    read_bag(parser.parse_args());
