# deep_researcher/tools/google_vision_ocr_agent.py

from google.cloud import vision
from pdf2image import convert_from_path
from PIL import Image
import io
import os

class GoogleVisionOCRAgent:
    def __init__(self, language_hints=["en", "ru", "uk"]):
        self.client = vision.ImageAnnotatorClient()
        self.language_hints = language_hints

    def _prepare_image(self, file_path: str):
        if file_path.lower().endswith(".pdf"):
            images = convert_from_path(file_path, dpi=300)
            return images  # List[Image]
        else:
            return [Image.open(file_path)]

    def _image_to_bytes(self, image: Image.Image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    def process_file(self, file_path: str):
        images = self._prepare_image(file_path)
        all_pages = []

        for i, image in enumerate(images):
            image_bytes = self._image_to_bytes(image)
            vision_image = vision.Image(content=image_bytes)

            response = self.client.document_text_detection(
                image=vision_image,
                image_context={"language_hints": self.language_hints}
            )

            page_result = {
                "page": i + 1,
                "text": response.full_text_annotation.text,
                "blocks": [],
            }

            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    block_text = ""
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            word_text = "".join([symbol.text for symbol in word.symbols])
                            block_text += word_text + " "
                    block_info = {
                        "text": block_text.strip(),
                        "bounding_box": [(v.x, v.y) for v in block.bounding_box.vertices],
                        "confidence": block.confidence
                    }
                    page_result["blocks"].append(block_info)

            all_pages.append(page_result)

        return {
            "filename": os.path.basename(file_path),
            "pages": all_pages
        }