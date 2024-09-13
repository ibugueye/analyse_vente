# import librairies 

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
st.markdown(""" <h3 style ="color:#002b50">  IBOU'S BUSINESS ANALYTICS DASBOARD | Python   </h3>""", unsafe_allow_html=True)
df= pd.read_csv("sales.csv")
st.markdown("<hr style='border: 2px solid rainbow;'>", unsafe_allow_html=True)




#load  css 


with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


# side bar
#st.sidebar.image("")

#sidebar date picker
with st.sidebar:
    st.title("Select Date Range")
    start_date = st.date_input(label="Start Date")
    
with st.sidebar:
    end_date = st.date_input(label= "End Date")
# provide a message forr selected date range
st.error("You have choosen analytics from : "+str(start_date) +" to "+ str(end_date))

# Filter date rabde 
df2 =df[(df["OrderDate"]>= str(start_date)) & (df["OrderDate"] <= str(end_date))]

# st.dataframe(df2,use_container_width=True)

with st.expander("Filter Excel Data"):
    filtered_df = dataframe_explorer(df2, case=False)
    st.dataframe(filtered_df, use_container_width=True)
    

a1, a2 = st.columns(2)

with a1:
    st.subheader("Product & Quantities")
    st.markdown("<hr style='border: 1px solid rainbow;'>", unsafe_allow_html=True)

    source =pd.DataFrame({
        "Quantity ($)": df2["Quantity"],
        "Product" : df2["Product"],
    })
    bar_chart = alt.Chart(source).mark_bar().encode(
         x ="sum(Quantity ($)):Q",
         
         y= alt.Y("Product:N", sort="-x")
    )
    
    
    st.altair_chart(bar_chart,use_container_width=True)   
    
# metrics 
with a2:
    st.subheader("Data Metrics")
    #st.markdown("<hr style='border: 1px solid rainbow;'>", unsafe_allow_html=True)
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2 = st.columns(2)
    col1.metric(label = "All number of Items", value =df2.Product.count(),delta="All Items")
    col2.metric(label="Sum of Product Price USD",value=f"{df2.TotalPrice.sum():,.0f}",delta=df2.TotalPrice.median())
    
    
    c11,c22,c33 = st.columns(3)
    c11.metric(label="Maximum Price",value=f"{df2.TotalPrice.max():,.0f}",delta="Hight Price")
    c22.metric(label="Minimim Price",value=f"{df2.TotalPrice.min():,.0f}",delta="Low Price")
    c33.metric(label="Price Range",value=f"{df2.TotalPrice.max()-df2.TotalPrice.min() :,.0f}",delta="Price Range")
    #  Style the metrics 
    style_metric_cards(background_color="56A923", border_left_color="#e6200e",border_color="#00060a",)

    
b1,b2= st.columns(2)
    
#dot plot
with b1:
        st.subheader("Products & Total Price ")
        #st.markdown("<hr style='border: 1px solid rainbow;'>", unsafe_allow_html=True)
        source=df2  
        chart=alt.Chart(source).mark_circle().encode(
            x="Product",
            y="TotalPrice",
            color="Category"            
        ).interactive()   
            
        st.altair_chart(chart, theme="streamlit",use_container_width=True)
    
with b2:
    st.subheader("Products & UnitPrice ")
    #st.markdown("<hr style='border: 1px solid rainbow;'>", unsafe_allow_html=True)
    energy_source = pd.DataFrame({
        "Product": df2["Product"],
        "UnitPrice ($)":df2["UnitPrice"],
        "Date": df2["OrderDate"],
    })
    bar_chart=alt.Chart(energy_source).mark_bar().encode(
        x="month(Date):O",
        y="sum(UnitPrice ($))", 
        color ="Product:N"
    )
    
    
    st.altair_chart(bar_chart,use_container_width=True)
      
 
 
 
 
c1,c2 =st.columns(2)
with c1:
    st.subheader("Product & UnitPrice")
   # st.markdown("<hr style='border: 1px solid rainbow;'>", unsafe_allow_html=True)
    feature_x = st.selectbox("select X, qualitative data",df2.select_dtypes("object").columns )
    feature_y = st.selectbox("select Y, quantitative data", df2.select_dtypes("number").columns)
    
    fig,ax=plt.subplots()
    sns.scatterplot(data = df2, x=feature_x, y=feature_y, hue=df2.Product,ax=ax)
    st.pyplot(fig)
                    
    
with c2:
      st.subheader("Features by Frequency")
     # st.markdown("<hr style='border: 1px solid rainbow;'>", unsafe_allow_html=True)
      feature = st.selectbox('Select only Qualitative Data',df2.select_dtypes("object").columns )
      fig,ax= plt.subplots()
      ax.hist(df2[feature], bins=20)
      
      ax.set_title(f'Histogram of {feature}')
      ax.set_xlabel(feature)
      ax.set_ylabel('Frequency')
      st.pyplot(fig)
      
      
      
