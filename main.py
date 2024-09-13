import streamlit as st 
import pandas as pd
import plotly.express  as px 
import seaborn as sns  
import altair as alt 
from matplotlib import pyplot as plt 
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import *

# configure the page width
st.set_page_config(page_title="Home",page_icon="",layout="wide")

# load data set 
st.markdown(""" <h3 style ="color:#002b50">  IBOU'S BUSINESS ANALYTICS DASBOARD |   </h3>""", unsafe_allow_html=True)
df= pd.read_csv("sales.csv")
st.markdown("<hr style='border: 2px solid rainbow;'>", unsafe_allow_html=True)

#load  css 
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Select Date Range")
    
    # Setting the default start date as 2014
    start_date = st.date_input(label="Start Date", value=pd.to_datetime("2014-01-01"))
    end_date = st.date_input(label="End Date")
    
st.error(f"You have chosen analytics from: {start_date} to {end_date}")

# Filter date range 
df2 = df[(df["OrderDate"] >= str(start_date)) & (df["OrderDate"] <= str(end_date))]

# Filter Excel Data
with st.expander("Filter Excel Data"):
    filtered_df = dataframe_explorer(df2, case=False)
    st.dataframe(filtered_df, use_container_width=True)

a1, a2 = st.columns(2)

with a1:
    st.subheader("Product & Quantities")
    st.markdown("<hr style='border: 1px solid rainbow;'>", unsafe_allow_html=True)

    source = pd.DataFrame({
        "Quantity ($)": df2["Quantity"],
        "Product": df2["Product"],
    })
    
    bar_chart = alt.Chart(source).mark_bar().encode(
        x="sum(Quantity ($)):Q",
        y=alt.Y("Product:N", sort="-x")
    )
    
    st.altair_chart(bar_chart, use_container_width=True)   

# Metrics
with a2:
    st.subheader("Data Metrics")
    st.markdown("<hr style='border: 1px solid rainbow;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric(label="All number of Items", value=df2.Product.count(), delta="All Items")
    col2.metric(label="Sum of Product Price USD", value=f"{df2.TotalPrice.sum():,.0f}", delta=df2.TotalPrice.median())
    
    c11, c22, c33 = st.columns(3)
    c11.metric(label="Maximum Price", value=f"{df2.TotalPrice.max():,.0f}", delta="High Price")
    c22.metric(label="Minimum Price", value=f"{df2.TotalPrice.min():,.0f}", delta="Low Price")
    c33.metric(label="Price Range", value=f"{df2.TotalPrice.max() - df2.TotalPrice.min():,.0f}", delta="Price Range")
    
    # Style the metrics 
    style_metric_cards(background_color="#3344c4", border_left_color="#e6200e", border_color="#00060a")

b1, b2 = st.columns(2)

# Dot plot
with b1:
    st.subheader("Products & Total Price")
    source = df2  
    chart = alt.Chart(source).mark_circle().encode(
        x="Product",
        y="TotalPrice",
        color="Category"
    ).interactive()   
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
    
with b2:
    st.subheader("Products & UnitPrice")
    energy_source = pd.DataFrame({
        "Product": df2["Product"],
        "UnitPrice ($)": df2["UnitPrice"],
        "Date": df2["OrderDate"],
    })
    bar_chart = alt.Chart(energy_source).mark_bar().encode(
        x="month(Date):O",
        y="sum(UnitPrice ($))",
        color="Product:N"
    )
    st.altair_chart(bar_chart, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    st.subheader("Product & UnitPrice")
    
    # Set default selection for Product & UnitPrice as "Category"
    feature_x = st.selectbox("Select X, qualitative data", df2.select_dtypes("object").columns, index=df2.columns.get_loc("Category"))
    feature_y = st.selectbox("Select Y, quantitative data", df2.select_dtypes("number").columns)
    
    fig, ax = plt.subplots()
    sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue=df2.Product, ax=ax)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Espèces")
    st.pyplot(fig)
                    
with c2:
    st.subheader("Features by Frequency")
    
    # Set default selection for Features by Frequency as "Category"
    feature = st.selectbox('Select only Qualitative Data', df2.select_dtypes("object").columns, index=df2.columns.get_loc("Category"))
    
    fig, ax = plt.subplots()
    ax.hist(df2[feature], bins=20)
    ax.set_title(f'Histogram of {feature}')
    ax.set_xlabel(feature)
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
