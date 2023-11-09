# ROS package with messages for event based cameras

This package has definitions for ROS / ROS2 messages created by event based vision
sensors. The events are kept in a compact binary format to avoid slow
serialization and deserialization during recording.

Event camera messages can be  visualized with the
[event_camera_renderer](https://github.com/ros-event-camera/event_camera_renderer)
and converted to other message formats using
[event_camera_tools](https://github.com/ros-event-camera/event_camera_tools).


For encoding and decoding of messages in C++ look at 
[event_camera_codecs](https://github.com/ros-event-camera/event_camera_codecs). The 
[event_camera_py](https://github.com/ros-event-camera/event_camera_py)
package provides a module for fast and convenient loading of events in python.


## Messages

### EventPacket

The EventPacket message contains a packet (array) of events in binary
format. Several different encoding formats are supported, but use of
the older, deprecated ones is strongly discouraged.

Description of the encodings:

- ``evt3``: raw Metavision evt3 data as it comes from the SDK.
    For the details of the encoding scheme refer to the Prophesee
    Metavision documents. 

	The ``time_base`` field is not used and its content is undefined. Recovery of
	sensor time requires decoding the data packets. For more about
	time stamps see documentation in
	[event_camera_codecs](https://github.com/ros-event-camera/event_camera_codecs).


- ``mono`` (deprecated): messages from monochrome cameras such as the DVS and
	Prophesee Metavision cameras. Encodes on 64 bit boundaries as follows:

    | bits  | interpretation                         |
    |-------|----------------------------------------|
    | 63    | polarity: ON event = 1, OFF event = 0  |
    | 48-62 | y (15 bits)                            |
    | 32-48 | x (16 bits)                            |
    | 0-32  | dt (32 bits)                           |

    To recover the original sensor time, add the delta ``dt`` to the
	message ``time_base`` field.
	To recover the best estimate ROS sensor time stamp add ``dt`` to the
	header stamp.

- ``trigger`` (deprecated): external trigger messages from e.g. the
    Prophesee Metavision cameras.

    | bits  | interpretation                         |
    |-------|----------------------------------------|
    | 63    | polarity: ON event = 1, OFF event = 0  |
    | 33-62 | unused (31 bits)                       |
    | 0-32  | dt (32 bits)                           |

    To recover the original sensor time add the delta ``dt`` to the
	message ``time_base`` field.
	To recover the best estimate ROS sensor time stamp add ``dt`` to the
	header stamp.


## License
This package is released under the [Apache-2 license](LICENSE).
