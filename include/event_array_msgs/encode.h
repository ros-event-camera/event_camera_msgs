// -*-c++-*--------------------------------------------------------------------
// Copyright 2021 Bernd Pfrommer <bernd.pfrommer@gmail.com>
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef EVENT_ARRAY_MSGS__ENCODE_H_
#define EVENT_ARRAY_MSGS__ENCODE_H_

#include <stdint.h>

namespace event_array_msgs
{
  //
  // ------------ helper functions to decode the standard "mono" message --------
  //
  namespace mono {
    static inline void encode(uint64_t *packed, bool p, uint16_t x, uint16_t y, uint32_t dt) {
      *packed = static_cast<uint64_t>(p) << 63 | static_cast<uint64_t>(y) << 48 |
        static_cast<uint64_t>(x) << 32 | static_cast<uint64_t>(dt);
    }
  } // end of namespace mono
}
#endif // EVENT_ARRAY_MSGS__ENCODE_H_
