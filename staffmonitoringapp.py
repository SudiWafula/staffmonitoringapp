#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import ipywidgets as widgets
from ipywidgets import interact
import warnings  
from ipywidgets import interactive
# Suppress warnings
warnings.filterwarnings('ignore')


# In[2]:


# Load data for the first dashboard
kit_sop_df = pd.read_csv('trainingKIT.csv', encoding='latin1')
kit_sop_df['DATE'] = pd.to_datetime(kit_sop_df['DATE'])
kit_sop_df['Year'] = kit_sop_df['DATE'].dt.year
kit_sop_df['Month'] = kit_sop_df['DATE'].dt.strftime('%Y-%b')
kit_sop_df['Custom_Week'] = kit_sop_df['DATE'].apply(
    lambda x: (x - pd.DateOffset(days=(x.weekday() - 3) % 7)).strftime('%Y-%U'))

def filter_kit_data(period, selected_month=None, selected_year=None, selected_week=None, position=None):
    filtered_df = kit_sop_df
    if period == 'Year' and selected_year:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    elif period == 'Month' and selected_month:
        filtered_df = filtered_df[filtered_df['Month'] == selected_month]
    elif period == 'Week' and selected_week:
        filtered_df = filtered_df[filtered_df['Custom_Week'] == selected_week]
    if position:
        filtered_df = filtered_df[filtered_df['EMPLOYEE POSITION'] == position]
    return filtered_df

# Load data for the second dashboard
asl_sop_df = pd.read_csv('trainingASL.csv', encoding='latin1')
asl_sop_df['DATE'] = pd.to_datetime(asl_sop_df['DATE'])
asl_sop_df['Year'] = asl_sop_df['DATE'].dt.year
asl_sop_df['Month'] = asl_sop_df['DATE'].dt.strftime('%Y-%b')
asl_sop_df['Custom_Week'] = asl_sop_df['DATE'].apply(
    lambda x: (x - pd.DateOffset(days=(x.weekday() - 3) % 7)).strftime('%Y-%U'))

def filter_asl_data(period, selected_month=None, selected_year=None, selected_week=None, position=None):
    filtered_df = asl_sop_df
    if period == 'Year' and selected_year:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    elif period == 'Month' and selected_month:
        filtered_df = filtered_df[filtered_df['Month'] == selected_month]
    elif period == 'Week' and selected_week:
        filtered_df = filtered_df[filtered_df['Custom_Week'] == selected_week]
    if position:
        filtered_df = filtered_df[filtered_df['EMPLOYEE POSITION'] == position]
    return filtered_df

# Streamlit App Layout
st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("Filters")

# Sidebar - Kitting Section
st.sidebar.subheader("Kitting Section")
kitting_default = st.sidebar.checkbox("Default View (Overall Comparison)", key="kit_default")
kitting_position = None
if not kitting_default:
    kitting_position = st.sidebar.selectbox(
        "Select Employee Position (Kitting)", 
        options=kit_sop_df['EMPLOYEE POSITION'].unique(),
        index=0
    )

# Sidebar - Assembly Section
st.sidebar.subheader("Assembly Section")
assembly_default = st.sidebar.checkbox("Default View (Overall Comparison)", key="asl_default")
assembly_position = None
if not assembly_default:
    assembly_position = st.sidebar.selectbox(
        "Select Employee Position (Assembly)", 
        options=asl_sop_df['EMPLOYEE POSITION'].unique(),
        index=0
    )

# Main Content
st.title("Staff Training Dashboard")

# Use columns for side-by-side dashboards
col1, col2 = st.columns(2)

# First dashboard in col1
with col1:
    st.header("KIT SOP Training")
    period_selector_kit = st.selectbox('Select Period (KIT)', options=['Year', 'Month', 'Week'], index=0, key='kit_period')
    selected_year_kit = selected_month_kit = selected_week_kit = None
    if period_selector_kit == 'Year' and not kitting_default:
        selected_year_kit = st.selectbox('Select Year', sorted(kit_sop_df['Year'].unique()), key='kit_year', index=0)
    elif period_selector_kit == 'Month' and not kitting_default:
        selected_month_kit = st.selectbox('Select Month', sorted(kit_sop_df['Month'].unique()), key='kit_month', index=0)
    elif period_selector_kit == 'Week' and not kitting_default:
        selected_week_kit = st.selectbox('Select Week', sorted(kit_sop_df['Custom_Week'].unique()), key='kit_week', index=0)

    filtered_kit_data = filter_kit_data(
        period_selector_kit, selected_month_kit, selected_year_kit, selected_week_kit, kitting_position
    ) if not kitting_default else kit_sop_df
    st.plotly_chart(px.bar(filtered_kit_data, x="KIT SOP TRAINED", color="KIT SOP TRAINED",
                           title=f"KIT SOP TRAINED Distribution by {period_selector_kit}",
                           color_discrete_sequence=["green"]))
    st.dataframe(filtered_kit_data)

# Second dashboard in col2
with col2:
    st.header("ASL SOP Training")
    period_selector_asl = st.selectbox('Select Period (ASL)', options=['Year', 'Month', 'Week'], index=0, key='asl_period')
    selected_year_asl = selected_month_asl = selected_week_asl = None
    if period_selector_asl == 'Year' and not assembly_default:
        selected_year_asl = st.selectbox('Select Year', sorted(asl_sop_df['Year'].unique()), key='asl_year', index=0)
    elif period_selector_asl == 'Month' and not assembly_default:
        selected_month_asl = st.selectbox('Select Month', sorted(asl_sop_df['Month'].unique()), key='asl_month', index=0)
    elif period_selector_asl == 'Week' and not assembly_default:
        selected_week_asl = st.selectbox('Select Week', sorted(asl_sop_df['Custom_Week'].unique()), key='asl_week', index=0)

    filtered_asl_data = filter_asl_data(
        period_selector_asl, selected_month_asl, selected_year_asl, selected_week_asl, assembly_position
    ) if not assembly_default else asl_sop_df
    st.plotly_chart(px.bar(filtered_asl_data, x="ASL SOP TRAINED", color="ASL SOP TRAINED",
                           title=f"ASL SOP TRAINED Distribution by {period_selector_asl}",
                           color_discrete_sequence=["yellow"]))
    st.dataframe(filtered_asl_data)

