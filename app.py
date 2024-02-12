import streamlit as st
from PIL import Image
import textwrap
import google.generativeai as genai
import io


def configure_google_api():
    genai.configure(api_key="yourapikey")  # Replace with your actual API key

    generation_config = {
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    return model

# Function to process the image and get the model response
def process_image(image_bytes):
    model = configure_google_api()
    
    image_parts = [{
        "mime_type": "image/jpeg",
        "data": image_bytes
    }]
    
    prompt_parts = [
        "Accurately identify the food item in the image and provide an appropriate and recipe consistent with your analysis. Give traditional methods of cooking for the given food item. ",
        image_parts[0],
        " \n",
    ]
    
    response = model.generate_content(prompt_parts)
    return response.text

def main():
    st.image('gemini.webp', use_column_width=True)
    st.title('Recipe Generator Using Gemini')
    st.write("This app uses the Gemini Pro Vision model to generate a recipe based on an image of a food item.")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("")
        st.write("Identifying...")

        # Convert PIL image to bytes for processing
        buf = io.BytesIO()
        image.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        
        # Get model response
        try:
            result_text = process_image(byte_im)
            st.markdown(textwrap.indent(result_text, '> ', predicate=lambda _: True))
        except Exception as e:
            st.error(f"Error processing image: {e}")

if __name__ == "__main__":
    main()
