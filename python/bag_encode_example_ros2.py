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
example python encoding to rosbag
Some of the rosbag writing code was taken from:
https://docs.ros.org/en/galactic/Tutorials/Ros2bag/Recording-A-Bag-From-Your-Own-Node-Python.html
"""

import rclpy
import rclpy.serialization
from rclpy.time import Time
from rclpy.clock import ClockType
import rosbag2_py
import argparse
import builtin_interfaces
from event_array_msgs.msg import EventArray
import numpy as np


def write_bag(args, event_msgs):
    print(f'writing {len(event_msgs)} msgs to bag: ', args.bag)
    writer = rosbag2_py.SequentialWriter()
    storage_options = rosbag2_py._storage.StorageOptions(
            uri=args.bag,  storage_id='sqlite3')
    converter_options = rosbag2_py._storage.ConverterOptions('', '')
    writer.open(storage_options, converter_options)
    topic_info = rosbag2_py._storage.TopicMetadata(
        name=args.topic, type='event_array_msgs/msg/EventArray',
        serialization_format='cdr')
    writer.create_topic(topic_info)
    print('finished writing!')

    for msg in event_msgs:
        t = Time.from_msg(msg.header.stamp)
        writer.write(args.topic,
                     rclpy.serialization.serialize_message(msg), t.nanoseconds)


def make_stamp(msg_num, dt_nsec):
    NANO = 1000000000
    years = 2021 - 1969
    t = Time(nanoseconds=(365 * 24 * 3600 * years * NANO +
                          dt_nsec * msg_num), clock_type=ClockType.ROS_TIME)
    t_msg = builtin_interfaces.msg.Time()
    t_msg.nanosec = t.nanoseconds % NANO
    t_msg.sec = t.nanoseconds // NANO
    return t_msg


def make_events(num_events, dt, width, height):
    """make_events produces test events"""
    # ts = time stamps relative to time base, must fit within 32 bits!
    r = range(num_events)
    raw_ts = np.array(r).astype(np.uint64) * dt
    ts = np.bitwise_and(raw_ts, 0xFFFFFFFF)
    # event coordinates near middle of image
    x = (np.array(r).astype(np.uint64) + width // 2) % width
    y = (np.array(r).astype(np.uint64) + height // 2) % height
    # generate alternating OFF and ON events
    p = np.where(np.array(r) % 2 == 0, 0, 1).astype(np.uint64)
    #
    # now pack all of them
    #
    packed = np.bitwise_or.reduce(
        (ts, np.left_shift(y, 48), np.left_shift(x, 32), np.left_shift(p, 63)))
#    print('packed bin: ')
#    for i in range(num_events):
#        print("{:64b}".format(packed[i]))
    return packed.tobytes()
    
    
def make_messages():
    messages = []
    events_per_msg = 50
    dt = 1000 # time between events in nanoseconds
    for msg_num in range(2):
        msg = EventArray()
        msg.header.frame_id = "event_cam"
        msg.header.stamp = make_stamp(msg_num, dt * events_per_msg)
        msg.encoding = 'mono'
        msg.is_bigendian = False
        msg.width = 640
        msg.height = 480
        msg.seq = msg_num
        msg.time_base = msg.header.stamp.nanosec
        msg.events = make_events(events_per_msg, dt, msg.width, msg.height)
        messages.append(msg)
        
    return messages


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='read and decode events from bag.')
    parser.add_argument('--bag', '-b', action='store', default='test_bag',
                        required=False, help='name of bag file to write')
    parser.add_argument('--topic', help='Event topic to write',
                        default='/event_camera/events', type=str)
    write_bag(parser.parse_args(), make_messages())
