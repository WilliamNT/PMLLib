from typing import List
from ..types.enums import ImageSampler
from .img_constants import HIGHLY_RESTRICTIVE_NEGATIVE_PROMPT, GENERAL_NEGATIVE_PROMPT
from ..types.structs import ImageModel, ImageSize

# Optimized for speed, bad quality, unfiltered
SD_15 = ImageModel(
    _id="sd15",
    dimensions=ImageSize(512, 512),
    model="sd_v1.5_f16.ckpt",
    guidance_scale=7,
    sampler=ImageSampler.DPMPP_SDE_KARRAS,
    steps=30,
    negative_prompt=HIGHLY_RESTRICTIVE_NEGATIVE_PROMPT
)

# Balanced between speed and quality filtered
DREAMSHAPER_XL_LIGHTNING = ImageModel(
    _id="dreamxl_lightning",
    dimensions=ImageSize(640, 640),
    model="dreamshaperxl_lightning_f16.ckpt",
    guidance_scale=2,
    sampler=ImageSampler.DPMPP_SDE_KARRAS,
    steps=4,
    refiner_model="sd_xl_refiner_1.0_f16.ckpt",
)

# Optimized for quality, slow, unfiltered
AAM_XL_ANIMEMIX_V10 = ImageModel(
    _id="animexl",
    dimensions=ImageSize(768, 768),
    model="aamxlanimemix_v10_f16.ckpt",
    guidance_scale=2,
    sampler=ImageSampler.DPMPP_SDE_KARRAS,
    steps=20,
)

# Optimized for speed and quality, filtered
JUGGERNAUTXL_V8_RUNDIFFUSION = ImageModel(
    _id="jv8r",
    dimensions=ImageSize(768, 768),
    model="juggernautxl_v8rundiffusion_f16.ckpt",
    guidance_scale=7,
    sampler=ImageSampler.DPMPP_SDE_KARRAS,
    steps=15,
    refiner_model="sd_xl_refiner_1.0_f16.ckpt",
)

# Optimized for speed and quality, filtered
# Configuration based on recommended values by model author
JUGGERNAUTXL_V9_LIGHTNING = ImageModel(
    _id="jv9l",
    dimensions=ImageSize(832, 1216),
    model="juggernautxl_v9rdphoto2lightning_f16.ckpt",
    guidance_scale=2,
    sampler=ImageSampler.DPMPP_SDE_KARRAS,
    steps=5,
    negative_prompt=GENERAL_NEGATIVE_PROMPT,
    refiner_model="sd_xl_refiner_1.0_f16.ckpt",
)

# SDXL_TURBO_V1 = ImageModel(
#     _id="sdxlv1_turbo",
#     dimensions=Dimensions(768, 768),
#     model="sdxl_turbo_v1_0_fp16_f16.ckpt",
#     guidance_scale=2,
#     sampler=Sampler.DPMPP_SDE_KARRAS,
#     steps=10,
# )

# Optimized for really high quality, filtered
SDXL_BASE_V1 = ImageModel(
    _id="sdxlv1_base",
    dimensions=ImageSize(1024, 1024),
    model="sd_xl_base_1.0_f16.ckpt",
    guidance_scale=2,
    sampler=ImageSampler.DPMPP_SDE_KARRAS,
    steps=15,
    refiner_model="sd_xl_refiner_1.0_f16.ckpt",
)

SD_CASCADE = ImageModel(
    _id="sd_cascade",
    dimensions=ImageSize(768, 1153),
    model="wurstchen_3.0_stage_c_f32_f16.ckpt",
    guidance_scale=1,
    sampler=ImageSampler.DPMPP_SDE_KARRAS,
    steps=5,
)

BEST_OVERALL_MODEL = JUGGERNAUTXL_V9_LIGHTNING

MODELS: List[ImageModel] = [
    SD_15,
    DREAMSHAPER_XL_LIGHTNING,
    AAM_XL_ANIMEMIX_V10,
    JUGGERNAUTXL_V8_RUNDIFFUSION,
    SDXL_BASE_V1,
    # SDXL_TURBO_V1,
    JUGGERNAUTXL_V9_LIGHTNING,
    SD_CASCADE,
]