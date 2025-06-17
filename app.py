# streamlit_app.py
import streamlit as st
import japanize_matplotlib
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from matplotlib.gridspec import GridSpec
import io

st.title("画像のRGBヒストグラム比較")

def get_rgb_histograms(img_file):
    try:
        img = Image.open(img_file).convert("RGB")
        img_array = np.array(img)

        hist_r = np.histogram(img_array[:, :, 0], bins=256, range=(0, 256))[0]
        hist_g = np.histogram(img_array[:, :, 1], bins=256, range=(0, 256))[0]
        hist_b = np.histogram(img_array[:, :, 2], bins=256, range=(0, 256))[0]

        return hist_r, hist_g, hist_b, img
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return None, None, None, None

# アップロード
uploaded_file1 = st.file_uploader("画像1をアップロード", type=["jpg", "jpeg", "png"], key="1")
uploaded_file2 = st.file_uploader("画像2をアップロード", type=["jpg", "jpeg", "png"], key="2")

if uploaded_file1 and uploaded_file2:
    hist1_r, hist1_g, hist1_b, img1 = get_rgb_histograms(uploaded_file1)
    hist2_r, hist2_g, hist2_b, img2 = get_rgb_histograms(uploaded_file2)

    if img1 and img2:
        # 画像リサイズと連結
        img1 = img1.resize((int(img1.width * 300 / img1.height), 300))
        img2 = img2.resize((int(img2.width * 300 / img2.height), 300))
        combined_img = Image.new('RGB', (img1.width + img2.width, 300))
        combined_img.paste(img1, (0, 0))
        combined_img.paste(img2, (img1.width, 0))

        fig = plt.figure(figsize=(15, 8))
        gs = GridSpec(2, 1, height_ratios=[1, 1.2])

        # 上段：画像表示
        ax_images = fig.add_subplot(gs[0])
        ax_images.axis('off')
        ax_images.imshow(combined_img)
        ax_images.set_title("左：画像1　右：画像2")

        # 下段：ヒストグラム
        ax_hist = fig.add_subplot(gs[1])
        ax_hist.plot(hist1_r, color='red', label='画像1 Red', alpha=0.7)
        ax_hist.plot(hist1_g, color='green', label='画像1 Green', alpha=0.7)
        ax_hist.plot(hist1_b, color='blue', label='画像1 Blue', alpha=0.7)
        ax_hist.plot(hist2_r, color='darkred', linestyle='--', label='画像2 Red', alpha=0.7)
        ax_hist.plot(hist2_g, color='darkgreen', linestyle='--', label='画像2 Green', alpha=0.7)
        ax_hist.plot(hist2_b, color='darkblue', linestyle='--', label='画像2 Blue', alpha=0.7)
        ax_hist.set_title("RGBヒストグラム比較")
        ax_hist.set_xlabel("ピクセル値")
        ax_hist.set_ylabel("頻度")
        ax_hist.grid(True)
        ax_hist.legend()

        st.pyplot(fig)
    else:
        st.warning("画像の読み込みに失敗しました。")
