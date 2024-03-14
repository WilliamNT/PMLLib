API_BASE = "http://127.0.0.1:7860"
TXT2IMG_ENDPOINT = "/sdapi/v1/txt2img"

HIGHLY_RESTRICTIVE_NEGATIVE_PROMPT = """
bad quality, worst quality, low resolution, worst resolution,
compressed, jpg, jpeg artifacts, lowres, pixelated, censor, censored

beginer, noob, watermark, username, signature,

low contract, too high contrast, oversaturated, undersaturated,
overexposed, underexposed, overedited, poorly edited, badly edited,
photoshopped, cropped, out of frame, out of focus, noise, noisy, pixelated, 

nude, nudity, ((nsfw)), exposed genitalia, exposed butt, exposed female breasts,
child, children, kid, kids, minors, underage, porn, pornography, oversexualized,
soft porn, onlyfans, fansly playboy, thicc, thick, unrealistic female features,
unrealistic male features, penis, vagina, rule34, e621, xxx, sex, racist, gore,
death, accident, corpse, dead body, terrorism, execution, brutality, not safe for work,
murder, killing, war crime, nazi, communist,

poorly drawn, stolen artwork, bad anatomy, distorted body parts, disfigured body parts,
too many body parts, ai generated, dalle, dall-e, stable diffusion, midjourney, morbid,
mutilated, mutation, deformed face, ugly face, bad face, deformed iris, deformed pupils,
deformed eyes, bad eyes, bad teeth, deformed teeth, deformed lips, text, logo,
"""

GENERAL_NEGATIVE_PROMPT = """
bad quality, low resolution, compression artifacts, censor, censored,

watermark, username, signature,

badly edited, over edited, out of frame, out of focus, amateur quality,

((nsfw)), (((underage))), nudity, pornography, (exposed genitalia:1.4),

bad drawing, bad anatomy, unrealistic body breasts, unrealistic butt, distorted,
disfigured, deformed, ugly, bad face, text, logo,
"""

MAX_SEED_LENGTH = 10