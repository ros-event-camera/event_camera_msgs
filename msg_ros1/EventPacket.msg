# This message contains a packet of camera events

Header header     # standard ROS header
uint32 height     # image height
uint32 width      # image width

uint64 seq        # sequence number to detect lost messages
uint64 time_base  # event ros time = time_base + decoded event_time
string encoding   # the encoding scheme to use
bool is_bigendian # true if machine stores in big endian format

uint8[] events
