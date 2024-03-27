import matplotlib.pyplot as plt
import numpy as np
import torch
class MakeImageByMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",)


            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "test"

    CATEGORY = "guaishou"

    def test(self, image , mask):
        # 扩展蒙版至与图像相同的尺寸
        if len(mask.shape) != 3:
            # 添加一个维度为1
            mask = mask.unsqueeze(0)
        mask_expanded = mask.unsqueeze(-1).expand(-1, -1, -1, 3)

        # 应用蒙版
        masked_image = image * mask_expanded

        # 检查蒙版是否正确应用
        mask_bool = mask_expanded[..., 0] > 0

        # 计算边界框
        # 这里直接使用原始 mask 计算边界，因为扩展后的 mask_expanded 用于生成 masked_image
        rows = torch.any(mask[0] > 0, dim=1)
        cols = torch.any(mask[0] > 0, dim=0)

        ymin, ymax = torch.where(rows)[0][[0, -1]]
        xmin, xmax = torch.where(cols)[0][[0, -1]]

        # 裁剪图片
        cropped_image = masked_image[:, ymin:ymax + 1, xmin:xmax + 1, :]

        # 检查裁剪后的图片
        print("Cropped image shape:", cropped_image.shape)

        return (cropped_image,)

    # A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
class ImageAddImageByMask():
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_a": ("IMAGE",),
                "image_b": ("IMAGE",),
                "mask": ("MASK",)

            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "test"

    CATEGORY = "guaishou"

    def test(self, image_a,image_b, mask):
        # 创建一个与image_a大小相同的背景，初期设置为全黑（或全透明）
        # 假设我们这里使用全黑背景，如果需要处理透明度，则需要调整
        background = torch.zeros_like(image_a)
        if len(mask.shape) != 3:
            # 添加一个维度为1
            mask = mask.unsqueeze(0)
        # 计算蒙版的边界框
        rows = torch.any(mask[0] > 0, dim=1)
        cols = torch.any(mask[0] > 0, dim=0)

        ymin, ymax = torch.where(rows)[0][[0, -1]]
        xmin, xmax = torch.where(cols)[0][[0, -1]]




        # 将image_b放置到background的适当位置
        # 注意：这里假设image_b已经是适合蒙版内容的大小
        background[0, ymin:ymin+image_b[0].size()[0], xmin:xmin +image_b[0].size()[1], :] = image_b[0]

        # 现在background含有image_b的内容，可以将其与image_a融合
        # 如果需要处理透明度，这里可以添加透明度的处理逻辑
        # 这里简单地将background直接赋值给image_a的对应位置
        # image_a[0, ymin:ymax + 1, xmin:xmax + 1, :] = background[0, ymin:ymax + 1, xmin:xmax + 1, :]
        # 将 mask 从 [1, 768, 768] 扩展到 [1, 768, 768, 1]
        mask_unsqueezed = mask.unsqueeze(-1)

        # 将 mask 扩展到三个颜色通道 [1, 768, 768, 3]
        mask_expanded = mask_unsqueezed.expand(-1, -1, -1, 3)

        # 使用 mask 选择需要从 background 替换的像素
        # mask_expanded 为 1 的位置将选择 background 的像素，否则选择 image_a 的像素
        # image_a_modified = torch.where(mask_expanded ==1, background, image_a)
        image_a_modified = mask_expanded * background + (1 - mask_expanded) * image_a
        return (image_a_modified,)


NODE_CLASS_MAPPINGS = {
    "MakeImageByMask": MakeImageByMask,
    "ImageAddImageByMask":ImageAddImageByMask
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "MakeImageByMask": "MakeImageByMask",
    "ImageAddImageByMask":"ImageAddImageByMask"
}
