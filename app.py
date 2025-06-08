import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
from inference_sdk import InferenceHTTPClient


st.set_page_config(page_title="Upload Fish Image", page_icon="🐟")
st.title("🐟 Fish Image Uploader")

uploaded_file = st.file_uploader("Upload fish image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Preview", use_column_width=True)

    # Đọc và chuyển ảnh thành base64
    image = Image.open(uploaded_file)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    if st.button("📤 Gửi ảnh đến n8n"):
        #Lưu url webhook n8n
        webhook_url = "https://phuongnghi.app.n8n.cloud/webhook-test/123"

        #Tạo kqua model của thằng Robo
        CLIENT = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key="SEDMOs9Km3JrHERSTQXQ"
        )
        result=CLIENT.infer(img_base64, model_id = "fish-disease-t6b03/1")

        response = requests.post(webhook_url, json={
            "filename": uploaded_file.name,
            "image_base64": img_base64,
            "result":result
        })

        if response.status_code == 200:
            st.text(response.text)
            st.success("✅ Ảnh đã được gửi đến n8n!")
        else:
            st.error(f"❌ Gửi thất bại.Ma loi: {response.status_code}")