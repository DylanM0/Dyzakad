#!/usr/bin/env python
# coding: utf-8

# In[10]:


import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module






def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)


def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = '상위_%s' % n
    return percentile_



st.set_page_config(page_title='Excel로 올려서 컷을 다운받자')
st.title('엑셀로 등급컷을 만들어볼까나? 📈')
st.subheader('Feed me with your Excel file')

uploaded_file = st.file_uploader('XLSX 형식의 파일을 올려주세요', type='xlsx')
if uploaded_file:
    st.markdown('전형명, 모집단위(코드포함), 등록여부, 산출등급')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)
    
    df.columns=['전형명','모집단위','등록여부','산출등급']
    
    choice = df['전형명'].unique()
    
    
    choice_column = st.selectbox('선택해주세요',choice, )    
    
    
    df1 = df[df['전형명'] == choice_column]
    
    
    
    dfc = df1.groupby(['모집단위'])['산출등급'].agg([np.max,np.mean, percentile(70),percentile(80),percentile(90),np.min])
    
    
    
       
    
  
    
    
    
    
    
    

    # -- GROUP DATAFRAME
#     output_columns = ['Sales', 'Profit']
#     df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()


    # -- DOWNLOAD SECTION
     st.subheader('Downloads:')
     generate_excel_download_link(dfc)
#     generate_html_download_link(m)






