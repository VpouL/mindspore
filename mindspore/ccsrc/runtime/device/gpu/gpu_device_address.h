/**
 * Copyright 2019 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef MINDSPORE_CCSRC_RUNTIME_DEVICE_GPU_GPU_DEVICE_ADDRESS_H_
#define MINDSPORE_CCSRC_RUNTIME_DEVICE_GPU_GPU_DEVICE_ADDRESS_H_

#include <string>
#include <vector>
#include "runtime/device/device_address.h"

namespace mindspore {
namespace device {
namespace gpu {
class GPUDeviceAddress : public DeviceAddress {
 public:
  GPUDeviceAddress(void *ptr, size_t size) : DeviceAddress(ptr, size) {}
  GPUDeviceAddress(void *ptr, size_t size, const string &format, TypeId type_id)
      : DeviceAddress(ptr, size, format, type_id) {}
  ~GPUDeviceAddress() override;

  bool SyncDeviceToHost(const std::vector<int> &shape, size_t size, TypeId type, void *host_ptr) const override;
  bool SyncHostToDevice(const std::vector<int> &shape, size_t size, TypeId type, const void *host_ptr) const override;
  void set_status(DeviceAddressStatus status) { status_ = status; }
  DeviceAddressStatus status() const { return status_; }
  DeviceAddressType DeviceType() const override { return DeviceAddressType::kGPU; }

 private:
  DeviceAddressStatus status_{DeviceAddressStatus::kInDevice};
};
}  // namespace gpu
}  // namespace device
}  // namespace mindspore

#endif  // MINDSPORE_CCSRC_RUNTIME_DEVICE_GPU_GPU_DEVICE_ADDRESS_H_
