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

#ifndef EVENT_ARRAY_MSGS__DECODE_H_
#define EVENT_ARRAY_MSGS__DECODE_H_

#include <stdint.h>
#include <stddef.h>

namespace event_array_msgs
{
  //
  // ------------ helper functions to decode the standard "mono" message --------
  //
  namespace mono {
    //
    // decode just x and y coordinates of event, return polarity
    //
    static inline bool decode_x_y_p(const uint8_t *packed_u8, uint16_t * x, uint16_t * y)
    {
      const uint64_t &packed = *reinterpret_cast<const uint64_t*>(packed_u8);
      *y = static_cast<uint16_t>((packed >> 48) & 0x7FFFULL);
      *x = static_cast<uint16_t>((packed >> 32) & 0xFFFFULL);
      return ((bool)(packed & ~0x7FFFFFFFFFFFFFFFULL));
    }
    
    //
    // decode time, x and y coordinates of event, return polarity
    //
    static inline bool decode_t_x_y_p(
      const uint8_t *packed_u8, uint64_t time_base, uint64_t * t, uint16_t * x, uint16_t * y)
    {
      const uint64_t &packed = *reinterpret_cast<const uint64_t*>(packed_u8);
      *y = static_cast<uint16_t>((packed >> 48) & 0x7FFFULL);
      *x = static_cast<uint16_t>((packed >> 32) & 0xFFFFULL);
      const uint32_t dt = static_cast<uint32_t>(packed & 0xFFFFFFFFULL);
      *t = time_base + dt;
      return (static_cast<bool>(packed & ~0x7FFFFFFFFFFFFFFFULL));
    }
    //
    // decode time only
    //
    static inline uint64_t decode_t(const uint8_t *packed_u8, uint64_t time_base) {
      const uint64_t &packed = *reinterpret_cast<const uint64_t*>(packed_u8);
      const uint32_t dt = static_cast<uint32_t>(packed & 0xFFFFFFFFULL);
      return (time_base + dt);
    }
    // for advancing the pointer
    const size_t bytes_per_event = 8;

  } // end of namespace mono

  //
  // ------------ helper functions to decode the standard "trigger" message --------
  //
  namespace trigger {
    //
    // decode just return polarity
    //
    static inline bool decode_p(const uint8_t *packed_u8)
    {
      const uint64_t &packed = *reinterpret_cast<const uint64_t*>(packed_u8);
      return ((bool)(packed & ~0x7FFFFFFFFFFFFFFFULL));
    }
    
    //
    // decode time of event, return polarity
    //
    static inline bool decode_t_p(
      const uint8_t *packed_u8, uint64_t time_base, uint64_t * t)
    {
      const uint64_t &packed = *reinterpret_cast<const uint64_t*>(packed_u8);
      const uint32_t dt = (uint32_t)(packed & 0xFFFFFFFFULL);
      *t = time_base + dt;
      return ((bool)(packed & ~0x7FFFFFFFFFFFFFFFULL));
    }
    // for advancing the pointer
    const size_t bytes_per_event = 8;

  } // end of namespace mono
}
#endif // EVENT_ARRAY_MSGS__DECODE_H_
