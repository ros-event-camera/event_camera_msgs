# ROS package with array messages for event based cameras

This package has definitions for ROS / ROS2 messages created by event based vision
sensors. The events are kept in a compact binary format to avoid slow
serialization and deserialization. They can be decoded with the help
of the
[event_array_codecs](https://github.com/berndpfrommer/event_array_codecs)
package, visualized with the
[event_array_viewer](https://github.com/berndpfrommer/event_array_viewer)
and converted to other message formats using
[event_array_tools](https://github.com/berndpfrommer/event_array_tools).


## Encoding schemes

- ``evt3``: raw Metavision evt3 data as it comes from the SDK.
    For decoding refer to Prophesee Metavision documents.

	The content of the ``time_base`` field is undefined. Recovery of
	sensor time requires decoding the data packets.

- ``mono`` (deprecated): messages from monochrome cameras such as the DVS and
	Prophesee Metavision cameras with ON and OFF events on
	Encodes on 64 bit boundaries as follows:

    | bits  | interpretation                         |
    |-------|----------------------------------------|
    | 63    | polarity: ON event = 1, OFF event = 0  |
    | 48-62 | y (15 bits)                            |
    | 32-48 | x (16 bits)                            |
    | 0-32  | dt (32 bits)                           |

    To recover the original sensor time, add the delta ``dt`` to the
	message ``time_base`` field.
	To recover the best estimate ROS sensor time stamp, add ``dt`` to the
	header stamp.

- ``trigger`` (deprecated): external trigger messages from e.g. the
    Prophesee Metavision cameras.

    | bits  | interpretation                         |
    |-------|----------------------------------------|
    | 63    | polarity: ON event = 1, OFF event = 0  |
    | 33-62 | unused (31 bits)                       |
    | 0-32  | dt (32 bits)                           |

    To recover the original sensor time, add the delta ``dt`` to the
	message ``time_base`` field.
	To recover the best estimate ROS sensor time stamp, add ``dt`` to the
	header stamp.

For encoding and decoding look at the sources in
[event_array_codecs](https://github.com/berndpfrommer/event_array_codecs)
and 
[event_array_tools](https://github.com/berndpfrommer/event_array_tools).


## License
This package is released under the [Apache-2 license](LICENSE).
