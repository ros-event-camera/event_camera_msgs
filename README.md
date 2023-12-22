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
format.

Description of the encodings:

- ``evt3``: raw Metavision evt3 data as it comes from the SDK.
    For the details of the encoding scheme refer to the Prophesee
    Metavision documents. 

	The ``time_base`` field is not used and its content is undefined. Recovery of
	sensor time requires decoding the data packets. For more about
	time stamps see documentation in
	[event_camera_codecs](https://github.com/ros-event-camera/event_camera_codecs).

- ``libcaer_cmp``: compressed libcaer format. The compression is similar
    to ``evt3`` but the ``time_base`` field is used to recover absolute
    sensor time. The decompression is best understood by looking at the
    source code [here](https://github.com/ros-event-camera/event_camera_codecs/blob/2b1738e45a1f6321a9ede640e052842e7beac43a/include/event_camera_codecs/libcaer_cmp_decoder.h).

- ``libcaer``: uncompressed messages in the format that libcaer
    presents it to its upper layers. The encoding takes 64bits per event and is
    similar to the ``mono`` encoding described below. This message format is generally inferior to ``libcaer_cmp``.

- ``mono``: (deprecated) event messages from the Prophesee cameras.
    Encodes on 64 bit boundaries as follows:

    | bits  | interpretation                         |
    |-------|----------------------------------------|
    | 63    | polarity: ON event = 1, OFF event = 0  |
    | 48-62 | y (15 bits)                            |
    | 32-48 | x (16 bits)                            |
    | 0-32  | dt (32 bits)                           |

    To recover the original sensor time, add the delta ``dt`` to the
	message ``time_base`` field. Both ``dt`` and ``time_base`` are
    in nanoseconds.	To recover the best estimate ROS sensor time
    stamp add ``dt`` to the ROS header stamp.

- ``trigger`` (deprecated): external trigger messages from e.g. the
    Prophesee Metavision cameras.

    | bits  | interpretation                         |
    |-------|----------------------------------------|
    | 63    | polarity: ON event = 1, OFF event = 0  |
    | 33-62 | unused (31 bits)                       |
    | 0-32  | dt (32 bits)                           |

    To recover the original sensor time add the delta ``dt`` to the
	message ``time_base`` field (in nanoseconds).
	To recover the best estimate ROS sensor time stamp add ``dt`` to the
	header stamp.


## License
This package is released under the [Apache-2 license](LICENSE).
