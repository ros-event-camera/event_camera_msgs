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
some code snippets for rosbag reading were taken from
https://github.com/ros2/rosbag2/blob/master/rosbag2_py/test/test_sequential_reader.py
"""

import time
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import rosbag2_py
import argparse
import numpy as np
from rclpy.time import Time


def get_rosbag_options(path, serialization_format='cdr'):
    storage_options = rosbag2_py.StorageOptions(uri=path, storage_id='sqlite3')

    converter_options = rosbag2_py.ConverterOptions(
        input_serialization_format=serialization_format,
        output_serialization_format=serialization_format)

    return storage_options, converter_options


def read_bag(args):
    debug_print = True
    bag_path = str(args.bag)
    storage_options, converter_options = get_rosbag_options(bag_path)

    reader = rosbag2_py.SequentialReader()
    print(f'reading bag {args.bag}')
    reader.open(storage_options, converter_options)

    topic_types = reader.get_all_topics_and_types()

    type_map = {topic_types[i].name: topic_types[i].type
                for i in range(len(topic_types))}

    storage_filter = rosbag2_py.StorageFilter(topics=[args.topic])
    reader.set_filter(storage_filter)

    t0 = None
    start_time = time.time()
    num_events = 0
    num_msgs = 0

    while reader.has_next():
        (topic, data, t_rec) = reader.read_next()
        msg_type = get_message(type_map[topic])
        msg = deserialize_message(data, msg_type)
        time_base = msg.time_base if args.use_sensor_time else \
            Time.from_msg(msg.header.stamp).nanoseconds
        # unpack all events in the message
        packed = np.frombuffer(msg.events, dtype=np.uint64)
        y = np.bitwise_and(
            np.right_shift(packed, 48), 0x7FFF).astype(np.uint16)
        x = np.bitwise_and(
            np.right_shift(packed, 32), 0xFFFF).astype(np.uint16)
        t = np.bitwise_and(packed, 0xFFFFFFFF) + time_base
        p = np.right_shift(packed, 63).astype(np.uint16)
        if not t0:
            t0 = Time.from_msg(msg.header.stamp).nanoseconds
        t_adj = t if args.use_sensor_time else (t - t0)
        a = np.stack((t_adj * 1e-9, x, y, p), axis=-1)
        if debug_print:
            print('---- message:')
            print(a)
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
