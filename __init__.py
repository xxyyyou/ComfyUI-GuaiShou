from .guaishou import MakeImageByMask,ImageAddImageByMask

NODE_CLASS_MAPPINGS = { "MakeImageByMask": MakeImageByMask,
                        "ImageAddImageByMask":ImageAddImageByMask}

NODE_DISPLAY_NAME_MAPPINGS = { "MakeImageByMask": "MakeImageByMask" ,
                               "ImageAddImageByMask":"ImageAddImageByMask"}

all = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']