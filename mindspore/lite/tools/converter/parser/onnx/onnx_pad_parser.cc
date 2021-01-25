/**
 * Copyright 2020 Huawei Technologies Co., Ltd
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

#include "tools/converter/parser/onnx/onnx_pad_parser.h"
#include <memory>
#include <vector>
#include "ops/fusion/pad_fusion.h"

namespace mindspore {
namespace lite {
ops::PrimitiveC *OnnxPadParser::Parse(const onnx::GraphProto &onnx_graph, const onnx::NodeProto &onnx_node) {
  auto primitive_c = new (std::nothrow) ops::PadFusion;
  if (primitive_c == nullptr) {
    MS_LOG(ERROR) << "new PadFusion failed";
    return nullptr;
  }

  mindspore::PaddingMode paddingMode;
  for (const auto &onnx_node_attr : onnx_node.attribute()) {
    const auto &attribute_name = onnx_node_attr.name();
    if (attribute_name == "pads") {
      const int size = onnx_node_attr.ints_size();
      std::vector<std::vector<int64_t>> paddings(size / 2, std::vector<int64_t>(2, 0));
      // begin1, begin2, begin3... end1, end2, end3... to
      // begin1, end1, begin2, end2, begin3, end3...
      for (int i = 0; i < size / 2; i++) {
        paddings[i][0] = static_cast<int64_t>(onnx_node_attr.ints(i));
        paddings[i][1] = static_cast<int64_t>(onnx_node_attr.ints(i + size / 2));
      }
      primitive_c->set_paddings(paddings);

      std::vector<std::vector<int32_t>> pads(size / 2, std::vector<int32_t>(2, 0));
      for (int i = 0; i < size / 2; i++) {
        pads[i][0] = static_cast<int32_t>(onnx_node_attr.ints(i));
        pads[i][1] = static_cast<int32_t>(onnx_node_attr.ints(i + size / 2));
      }
      primitive_c->AddAttr("pads", MakeValue(pads));
    } else if (attribute_name == "mode") {
      const auto &mode = onnx_node_attr.s();
      if (mode == "constant") {
        paddingMode = mindspore::PaddingMode::CONSTANT;
      } else if (mode == "reflect") {
        paddingMode = mindspore::PaddingMode::REFLECT;
      } else if (mode == "edge") {
        paddingMode = mindspore::PaddingMode::SYMMETRIC;
      }
      primitive_c->set_padding_mode(paddingMode);
    }
  }

  return primitive_c;
}

OnnxNodeRegistrar g_onnxPadParser("Pad", new OnnxPadParser());
}  // namespace lite
}  // namespace mindspore
