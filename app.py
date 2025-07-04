# streamlit_app.py
import streamlit as st

import matplotlib
import shutil

shutil.rmtree(matplotlib.get_cachedir(), ignore_errors=True)

# japanize_matplotlib を削除
# import japanize_matplotlib

# from matplotlib import rcParams
# rcParams['font.family'] = 'IPAexGothic'  # 日本語用フォントがシステムにある場合
# rcParams['font.family'] = ['Noto Sans CJK JP', 'sans-serif']

import os
from matplotlib import rcParams, font_manager

# フォントパスを指定して読み込み
# font_path = "fonts/ipaexg.ttf"
# font_prop = font_manager.FontProperties(fname=font_path)
# rcParams['font.family'] = font_prop.get_name()

font_path = "fonts/ipaexg.ttf"
if os.path.exists(font_path):
    font_prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = font_prop.get_name()
else:
    # フォールバック（英語フォント）
    st.warning("日本語フォントが見つかりません。代替フォントを使用します。")
    rcParams['font.family'] = 'sans-serif'

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
uploaded_file1 = st.file_uploader("Image 1をアップロード", type=["jpg", "jpeg", "png"], key="1")
uploaded_file2 = st.file_uploader("Image 2をアップロード", type=["jpg", "jpeg", "png"], key="2")

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
        
        # 画像ファイル名を取得してタイトルに反映
        name1 = uploaded_file1.name if uploaded_file1 else "Image 1"
        name2 = uploaded_file2.name if uploaded_file2 else "Image 2"        
        ax_images.imshow(combined_img)
        ax_images.set_title("Left: Image 1    Right: Image 2")
        # ax_images.set_title(f'Left: Image 1 ({name1})  Right: Image 2 ({name2})')

        # 下段：ヒストグラム
        ax_hist = fig.add_subplot(gs[1])
        ax_hist.plot(hist1_r, color='red', label='Image 1 Red', alpha=0.7)
        ax_hist.plot(hist1_g, color='green', label='Image 1 Green', alpha=0.7)
        ax_hist.plot(hist1_b, color='blue', label='Image 1 Blue', alpha=0.7)
        ax_hist.plot(hist2_r, color='darkred', linestyle='--', label='Image 2 Red', alpha=0.7)
        ax_hist.plot(hist2_g, color='darkgreen', linestyle='--', label='Image 2 Green', alpha=0.7)
        ax_hist.plot(hist2_b, color='darkblue', linestyle='--', label='Image 2 Blue', alpha=0.7)
        ax_hist.set_title("Combined RGB Histograms")
        ax_hist.set_xlabel("Pixel Value")
        ax_hist.set_ylabel("Frequency")
        ax_hist.grid(True)
        ax_hist.legend()

        st.pyplot(fig)
    else:
        st.warning("画像の読み込みに失敗しました。")
