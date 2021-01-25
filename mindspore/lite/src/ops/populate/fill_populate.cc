/**
 * Copyright 2019-2021 Huawei Technologies Co., Ltd
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
#include "src/ops/populate/populate_register.h"
#include "nnacl/fp32/fill_fp32.h"

namespace mindspore {
namespace lite {
namespace {
OpParameter *PopulateFillParameter(const void *prim) {
  FillParameter *fill_param = reinterpret_cast<FillParameter *>(malloc(sizeof(FillParameter)));
  if (fill_param == nullptr) {
    MS_LOG(ERROR) << "malloc FillParameter failed.";
    return nullptr;
  }
  memset(fill_param, 0, sizeof(FillParameter));
  auto primitive = static_cast<const schema::Primitive *>(prim);
  fill_param->op_parameter_.type_ = primitive->value_type();
  return reinterpret_cast<OpParameter *>(fill_param);
}
}  // namespace

Registry g_fillParameterRegistry(schema::PrimitiveType_Fill, PopulateFillParameter, SCHEMA_CUR);

}  // namespace lite
}  // namespace mindspore
