from jufo_pptx_script.templater.Template import Template
from jufo_pptx_script.templater.TemplateApplier import ImageParseResult
from pptx.slide import Slide
import io
from jufo_pptx_script.easypresentation.EasyPresentation import EasyPresentation
from PIL import Image
from pptx.shapes.placeholder import SlidePlaceholder, PicturePlaceholder
from pptx.shapes.autoshape import Shape as AutoShape
from typing import Any
import sys
import tqdm


def _clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


class EasySlide:

    def __init__(self, slide: Slide, pptx: EasyPresentation):
        self.__slide = slide
        self.__pptx = pptx

    def apply_template(self, template: Template, data: Any):

        for shape in self.__slide.shapes:
            if isinstance(shape, AutoShape):
                self.__update_text_placeholder(data, shape.text, shape, template)

        for i, pl in enumerate(self.__slide.placeholders):
            # Gets the placeholder text (Which is not accessible otherwise)
            text = self.__slide.slide_layout.placeholders[i].text

            if isinstance(pl, SlidePlaceholder):
                self.__update_text_placeholder(data, text, pl, template)
            if isinstance(pl, PicturePlaceholder):
                self.__update_image_placeholder(data, text, pl, template)

    # region Internal template apply mechanism

    @property
    def _image_cache(self):
        return self.__pptx._image_cache

    def _load_image(self, request: ImageParseResult):
        cache = self.__pptx._image_cache

        img_bytes = cache.get(request.raw) if cache is not None else None

        if img_bytes is None:
            img = Image.open(request.result)

            # Scales the image if required
            if request.scale is not None:
                # Checks for a percentage scale
                if type(request.scale) is int:
                    request.scale = _clamp(request.scale, 1, 100)
                    img = img.resize((int(img.width * request.scale / 100), int(img.height * request.scale / 100)))
                # It's a pixel scale
                else:
                    request.scale = (
                        _clamp(request.scale[0], 1, 99999),
                        _clamp(request.scale[1], 1, 99999)
                    )

                    img = img.resize(request.scale)

            img_bytes = io.BytesIO()
            img.save(img_bytes, img.format if img.format is not None else "jpeg")

            if cache is not None:
                cache[request.raw] = img_bytes

        img_bytes.seek(0)
        return img_bytes

    def __update_text_placeholder(self, data: Any, raw_text: str,
                                  element: SlidePlaceholder or AutoShape, template: Template):
        res = self.__pptx._template.parse(template, data, raw_text)

        # Parses the text and applies it to the placeholder
        element.text = res

    def __update_image_placeholder(self, data: Any, raw_text: str,
                                   placeholder: PicturePlaceholder, template: Template):
        # Resolves any templates inside the image infos
        res = self.__pptx._template.parse_with_image_properties(template, data, raw_text)

        try:
            img_as_bytes = self._load_image(res)
            placeholder.insert_picture(img_as_bytes)
        except FileNotFoundError:
            print(f"\rImage at '{res.result}' was not found, skipping...",file=sys.stderr)
        except Exception as err:
            raise ValueError(f"Image at '{res.result}' couldn't be loaded: {err}")


    # endregion
