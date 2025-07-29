import streamlit as st
from PIL import Image, ImageEnhance
import io, zipfile

st.title("🏠 Batch Real Estate Watermarker")

st.write("Upload a photo and your agency’s logo. Get a watermarked image instantly — no storage, just download.")

uploaded_images = st.file_uploader("Upload main images (JPEG,JPG,PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
logo_file = st.file_uploader("Upload watermark logo (JPEG,JPG,PNG)", type=["jpg", "jpeg", "png"])

if uploaded_images and logo_file:
    logo = Image.open(logo_file).convert("RGBA")
    alpha = logo.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.4)
    logo.putalpha(alpha)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for image_file in uploaded_images:
            image = Image.open(image_file).convert("RGBA")

            # Resize logo relative to image
            logo_copy = logo.copy()
            logo_size = min(image.size) // 2
            logo_copy.thumbnail((logo_size, logo_size), Image.LANCZOS)

            x = (image.width - logo_copy.width) // 2
            y = (image.height - logo_copy.height) // 2

            result = image.copy()
            result.paste(logo_copy, (x, y), logo_copy)

            st.image(result, caption=f"Preview: {image_file.name}", use_container_width=True)

            img_bytes = io.BytesIO()
            result.convert("RGB").save(img_bytes, format="JPEG")
            img_bytes.seek(0)

            zip_file.writestr(f"watermarked_{image_file.name}", img_bytes.read())

    zip_buffer.seek(0)
    st.download_button("Download All Watermarked Images (ZIP)", zip_buffer.getvalue(),
                       file_name="watermarked_images.zip", mime="application/zip")
    
