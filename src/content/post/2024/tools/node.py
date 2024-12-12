import requests
import numpy as np
from PIL import Image
from io import BytesIO
import torch


class CF_sdxl_base_1_0:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Default prompt", "multiline": True}),
                "negative_prompt": ("STRING", {"default": "Default prompt", "multiline": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("生成图像",)
    FUNCTION = "test"
    CATEGORY = "CF_AI"

    def test(self, prompt, negative_prompt):
        headers = {
            'Authorization': 'Bearer jiCI-5e_-MeQ3miJ2ZjuvlQkrmnlQa-5tYYSYiC1',
            'Content-Type': 'application/json',
        }
        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt
        }

        response = requests.post(
            "https://api.cloudflare.com/client/v4/accounts/7dc2a18e8751b868923b1731d9e6c062/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            # 获取图片
            image_data = response.content
            # 将解码后的二进制数据转换为Image对象
            i = Image.open(BytesIO(image_data))
            # 转换图像到RGB模式
            image= i.convert("RGB")
            # 将PIL Image转换为numpy数组，并归一化到0-1范围
            image_np = np.array(image).astype(np.float32) / 255.0
            # 将numpy数组转换为torch张量，并增加一个维度以匹配batch大小
            image_np = torch.from_numpy(image_np)[None,]
            return (image_np,)
        else:
            raise Exception(f"Failed to generate image: {response.text}")

class CF_sdxl_lightning:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Default prompt", "multiline": True}),
                "negative_prompt": ("STRING", {"default": "Default prompt", "multiline": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("生成图像",)
    FUNCTION = "test"
    CATEGORY = "CF_AI"

    def test(self, prompt, negative_prompt):
        headers = {
            'Authorization': 'Bearer jiCI-5e_-MeQ3miJ2ZjuvlQkrmnlQa-5tYYSYiC1',
            'Content-Type': 'application/json',
        }
        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt
        }

        response = requests.post(
            "https://api.cloudflare.com/client/v4/accounts/7dc2a18e8751b868923b1731d9e6c062/ai/run/@cf/bytedance/stable-diffusion-xl-lightning",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            # 获取图片
            image_data = response.content
            # 将解码后的二进制数据转换为Image对象
            i = Image.open(BytesIO(image_data))
            # 转换图像到RGB模式
            image= i.convert("RGB")
            # 将PIL Image转换为numpy数组，并归一化到0-1范围
            image_np = np.array(image).astype(np.float32) / 255.0
            # 将numpy数组转换为torch张量，并增加一个维度以匹配batch大小
            image_np = torch.from_numpy(image_np)[None,]
            return (image_np,)
        else:
            raise Exception(f"Failed to generate image: {response.text}")

class CF_dreamshaper_8_lcm:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Default prompt", "multiline": True}),
                "negative_prompt": ("STRING", {"default": "Default prompt", "multiline": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("生成图像",)
    FUNCTION = "test"
    CATEGORY = "CF_AI"

    def test(self, prompt, negative_prompt):
        headers = {
            'Authorization': 'Bearer jiCI-5e_-MeQ3miJ2ZjuvlQkrmnlQa-5tYYSYiC1',
            'Content-Type': 'application/json',
        }
        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt
        }

        response = requests.post(
            "https://api.cloudflare.com/client/v4/accounts/7dc2a18e8751b868923b1731d9e6c062/ai/run/@cf/lykon/dreamshaper-8-lcm",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            # 获取图片
            image_data = response.content
            # 将解码后的二进制数据转换为Image对象
            i = Image.open(BytesIO(image_data))
            # 转换图像到RGB模式
            image= i.convert("RGB")
            # 将PIL Image转换为numpy数组，并归一化到0-1范围
            image_np = np.array(image).astype(np.float32) / 255.0
            # 将numpy数组转换为torch张量，并增加一个维度以匹配batch大小
            image_np = torch.from_numpy(image_np)[None,]
            return (image_np,)
        else:
            raise Exception(f"Failed to generate image: {response.text}")

class CF_llama_3_1_8b_instruct:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Default prompt", "multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("生成回答",)
    FUNCTION = "test"
    CATEGORY = "CF_AI"

    def test(self, prompt):
        headers = {
            'Authorization': 'Bearer jiCI-5e_-MeQ3miJ2ZjuvlQkrmnlQa-5tYYSYiC1',
            'Content-Type': 'application/json',
        }
        data = {
            "prompt": prompt
        }

        response = requests.post(
            "https://api.cloudflare.com/client/v4/accounts/7dc2a18e8751b868923b1731d9e6c062/ai/run/@cf/meta/llama-3.1-8b-instruct",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            # Parse the JSON response
            parsed_json = response.json()
            
            # Extract the 'response' field
            response_text = parsed_json['result']['response']
            return (response_text,)
        else:
            raise Exception(f"Failed to generate text: {response.text}")



# 节点映射保持不变
NODE_CLASS_MAPPINGS = {
    "CF_sdxl_base_1_0": CF_sdxl_base_1_0,
    "CF_sdxl_lightning": CF_sdxl_lightning,
    "CF_dreamshaper_8_lcm": CF_dreamshaper_8_lcm,
    "CF_llama_3_1_8b_instruct": CF_llama_3_1_8b_instruct
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CF_sdxl_base_1_0": "CF sdxl base 1.0",
    "CF_sdxl_lightning": "CF sdxl lightning",
    "CF_dreamshaper_8_lcm": "CF dreamshaper 8 lcm",
    "CF_llama_3_1_8b_instruct": "CF llama 3.1 8b instruct"
}