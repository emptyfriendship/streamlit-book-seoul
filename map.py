# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:41:03 2024

@author: 213
"""

import streamlit as st
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
import plotly.express as px

import matplotlib.font_manager as fm
import os

def load_font():
    try:
        path = os.path.join('fonts', 'H2MJRE.ttf')
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Font file not found at {path}")
        return fm.FontProperties(fname=path, size=12)
    except Exception as e:
        st.error(f"Error loading font: {e}")
        return fm.FontProperties(size=12)

def mapMatplotlib(merge_df):
    fontprop = load_font()

    # 서브플롯 생성
    fig, ax = plt.subplots(ncols=2, sharey=True, figsize=(15, 10))
    
    # 2월 데이터 플로팅
    merge_df[merge_df['month'] == 2].plot(ax=ax[0], column='mean', cmap='Pastel1', legend=False, alpha=0.9, edgecolor='gray')
    
    # 3월 데이터 플로팅
    merge_df[merge_df['month'] == 3].plot(ax=ax[1], column='mean', cmap='Pastel1', legend=False, alpha=0.9, edgecolor='gray')

    # 컬러바
    patch_col = ax[0].collections[0]
    cb = fig.colorbar(patch_col, ax=ax, shrink=0.5)
    
    # 2월 지도 주석
    for i, row in merge_df[merge_df['month'] == 2].iterrows():
        ax[0].annotate(row['SIG_KOR_NM'], xy=(row['lon'], row['lat']), xytext=(-7, 2),
                       textcoords='offset points', fontsize=8, color='black', fontproperties=fontprop)
    
    # 3월 지도 주석
    for i, row in merge_df[merge_df['month'] == 3].iterrows():
        ax[1].annotate(row['SIG_KOR_NM'], xy=(row['lon'], row['lat']), xytext=(-7, 2),
                       textcoords='offset points', fontsize=8, color='black', fontproperties=fontprop)

    # 제목 설정
    ax[0].set_title('2024-2월 아파트 평균(만원)', fontproperties=fontprop)
    ax[1].set_title('2024-3월 아파트 평균(만원)', fontproperties=fontprop)
    
    # 축 제거
    ax[0].set_axis_off()
    ax[1].set_axis_off()
    
    # 플롯 표시
    st.pyplot(fig)
    
def showMap(total_df):
    st.markdown("### 병합 데이터 확인 \n" "- 컬럼명 확인")
    
    # 지리 데이터 로드 및 준비
    seoul_gpd = gpd.read_file("seoul_sig.geojson.gpkg")
    seoul_gpd = seoul_gpd.set_crs(epsg='5178', allow_override=True)
    seoul_gpd['center_point'] = seoul_gpd['geometry'].geometry.centroid
    seoul_gpd['geometry'] = seoul_gpd['geometry'].to_crs(epsg=4326)
    seoul_gpd['center_point'] = seoul_gpd['center_point'].to_crs(epsg=4326)
    seoul_gpd['lon'] = seoul_gpd['center_point'].map(lambda x: x.xy[0][0])
    seoul_gpd['lat'] = seoul_gpd['center_point'].map(lambda x: x.xy[1][0])
    seoul_gpd = seoul_gpd.rename(columns={"SIG_CD": "SGG_CD"})
    
    # 거래 데이터 준비
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format="%Y-%m-%d")
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    total_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]
    total_df = total_df[['DEAL_YMD', 'month', 'SGG_CD', 'SGG_NM', 'OBJ_AMT', 'HOUSE_TYPE']].reset_index(drop=True)
    
    # 거래 데이터 요약
    summary_df = total_df.groupby(['SGG_CD', 'month'])['OBJ_AMT'].agg(['mean', 'std', 'size']).reset_index()
    summary_df['SGG_CD'] = summary_df['SGG_CD'].astype(str)
    
    # 지리 데이터와 거래 데이터 병합
    merge_df = seoul_gpd.merge(summary_df, on='SGG_CD')
    
    # 병합 데이터 샘플 표시
    st.markdown("- 일부 데이터만 확인")
    st.write(merge_df[['SIG_KOR_NM', 'geometry', 'mean']].head(3))
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 지도 생성 및 표시
    st.markdown("### Matplotlib Style")
    mapMatplotlib(merge_df)
