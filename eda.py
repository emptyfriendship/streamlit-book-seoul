# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:29:05 2024

@author: 213
"""

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from viz import showViz
from statistic import showStat
from map import showMap

def home() :
    st.markdown("### Visualization 개요 \n"
                "- 가구당 평균 가격 추이 \n"
                "- 가구당 거래 건수 추세 \n"
                "- 지역별 평균 가격 막대 그래프 \n")
    st.markdown("### Statistics 개요 \n")
    st.markdown("### Map 개요 \n")

def run_eda_home(total_df) :
    st.markdown("### 탐색적 자료 분석 개요 \n"
                "탐색적 자료 분석 페이지 입니다."
                "여기에 포함하고 싶은 내용을 넣을 수 있습니다.")
    
    selected = option_menu(None, ['Home', 'Visualization', 'Statistics', 'Map'],
                           icons=['house', 'bar-chart', 'file-spreadsheet', 'map'],
                           menu_icon='cast', default_index=0, orientation='horizontal',
                           styles={
                               'container' : {
                                               'padding' : '0!important',
                                               'background-color' : '#808080'},
                               'icon' :      {
                                               'color' : 'orange',
                                               'font-size' : '25px'},
                               'nav-link' :  {
                                               'font-size' : '15px',
                                               'text-align' : 'left',
                                               'margin' : '0px',
                                               '--hover-color' : '#eee'},
                               'nav-link-selected' : {
                                               'background-color' : 'green'}
                               })
    if selected == 'Home' :
        home()
    elif selected == 'Visualization' :
        showViz(total_df)
    elif selected == 'Statistics' :
        showStat(total_df)
    elif selected == 'Map' :
        showMap(total_df)
    else:
        st.warning('Wrong')
