import re

class CropWeightSelector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {"default": ""}),
                "triggerwords": ("STRING", {"default": "michipeklo,chrishnsk,renehundertpfund,mikegasparik"}),

                # Weight set
                "weight_closeup": ("FLOAT", {"default": 0.50, "step": 0.01}),
                "weight_medium": ("FLOAT", {"default": 0.50, "step": 0.01}),
                "weight_wide": ("FLOAT", {"default": 0.50, "step": 0.01}),
                # Start set
                "start_at_closeup": ("FLOAT", {"default": 0.00, "step": 0.01}),
                "start_at_medium": ("FLOAT", {"default": 0.00, "step": 0.01}),
                "start_at_wide": ("FLOAT", {"default": 0.00, "step": 0.01}),
                # End set
                "end_at_closeup": ("FLOAT", {"default": 1.00, "step": 0.01}),
                "end_at_medium": ("FLOAT", {"default": 1.00, "step": 0.01}),
                "end_at_wide": ("FLOAT", {"default": 1.00, "step": 0.01}),
                # Denoise set
                "denoise_closeup": ("FLOAT", {"default": 0.20, "step": 0.01}),
                "denoise_medium": ("FLOAT", {"default": 0.20, "step": 0.01}),
                "denoise_wide": ("FLOAT", {"default": 0.20, "step": 0.01}),

                "clear_string": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = (
        "FLOAT",  # matched_weight
        "FLOAT",  # matched_start
        "FLOAT",  # matched_end
        "FLOAT",  # matched_denoise
        "STRING", # cleaned_string
        "STRING", # matched_keyword
        "STRING"  # image_url
    )

    RETURN_NAMES = (
        "matched_weight",
        "matched_start",
        "matched_end",
        "matched_denoise",
        "cleaned_string",
        "matched_keyword",
        "image_url"
    )

    FUNCTION = "select_crop_values"
    CATEGORY = "Custom"

    def select_crop_values(
        self,
        input_string,
        triggerwords,
        weight_closeup, weight_medium, weight_wide,
        start_at_closeup, start_at_medium, start_at_wide,
        end_at_closeup, end_at_medium, end_at_wide, 
        denoise_closeup, denoise_medium, denoise_wide,
        clear_string
    ):
        input_string = input_string.strip()
        lowered = input_string.lower()
        cleaned_string = input_string

        matched_weight = 0.0
        matched_start = 0.0
        matched_end = 1.0
        matched_denoise = 0.0
        matched_keyword = ""
        image_url = ""

        # Crop matching
        match_map = {
            "crop:medium": {
                "weight": weight_medium,
                "start": start_at_medium,
                "end": end_at_medium,
                "denoise": denoise_medium
            },
            "crop:wide": {
                "weight": weight_wide,
                "start": start_at_wide,
                "end": end_at_wide,
                "denoise": denoise_wide
            },
            "crop:closeup": {
                "weight": weight_closeup,
                "start": start_at_closeup,
                "end": end_at_closeup,
                "denoise": denoise_closeup
            }
        }

        for key, values in match_map.items():
            pattern = re.compile(re.escape(key), re.IGNORECASE)
            if pattern.search(lowered):
                matched_weight = round(values["weight"], 2)
                matched_start = round(values["start"], 2)
                matched_end = round(values["end"], 2)
                matched_denoise = round(values["denoise"], 2)
                cleaned_string = pattern.sub("", cleaned_string).strip()
                break

        # Keyword match to generate image URL
        keyword_list = [kw.strip().lower() for kw in triggerwords.split(",") if kw.strip()]
        for kw in keyword_list:
            if re.search(rf"\b{re.escape(kw)}\b", lowered):
                matched_keyword = kw
                image_url = f"https://qikbljxzzfgjkurwndun.supabase.co/storage/v1/object/public/generated-images/resources/faces/{kw}.jpg"
                break

        if clear_string:
            cleaned_string = ""

        return (
            matched_weight,
            matched_start,
            matched_end,
            matched_denoise,
            cleaned_string,
            matched_keyword,
            image_url
        )


NODE_CLASS_MAPPINGS = {
    "CropWeightSelector": CropWeightSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CropWeightSelector": "🎯 Crop Weight Selector"
}
