from transformers import DalleBartProcessor, DalleBartForConditionalGeneration
import torch
from PIL import Image
import requests
from io import BytesIO

# Load the model and processor
processor = DalleBartProcessor.from_pretrained("flax-community/dalle-mini")
model = DalleBartForConditionalGeneration.from_pretrained("flax-community/dalle-mini").to('cuda')

# Function to generate images from text
def generate_image_from_text(prompt):
    inputs = processor([prompt], return_tensors="pt").to('cuda')
    with torch.no_grad():
        outputs = model.generate(**inputs)
    image_tensor = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    return image_tensor

# Example prompt
prompt = "A scenic view of mountains during sunset"
generated_image = generate_image_from_text(prompt)

# Convert tensor to image and save it
image = Image.open(BytesIO(generated_image))
image.save("generated_image.png")
