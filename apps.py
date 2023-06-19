import pandas as pd
import easyocr
from PIL import Image
import streamlit as st

import sqlalchemy
import psycopg2
from sqlalchemy import create_engine
# creating a PostgreSQL connection
conn = psycopg2.connect(
    host= 'localhost',
    user="postgres",
    password="ganga123",
    port=5432,
    database="buissnesscard"
)


gt = conn.cursor()

# gt.execute("create table collection (name varchar(25),designation varchar(30),ph_no varchar(15),web varchar(30),email_id varchar(35),address varchar(10))")
# conn.commit()

engine = create_engine("postgresql+psycopg2://postgres:ganga123@localhost/buissnesscard")


def bcard(img):
  
  reader = easyocr.Reader(['en'])
  result = reader.readtext(img)
  dict1 = {"name":[],
     "designation":[],
     "ph.no":[],
     "web":[],
     "email-id":[],
     "address":[]}



  data = []
  for i in range(len(result)):
    data.append((result[i][1]))
  
  dict1["designation"].append(data[1])
  dict1["name"].append(data[0])
  import re

  m = []
  for j in data:
    if j in (re.findall(r'[+]?\d+\W+\d+\W+\d+',j)):
       m.append(j)
    if "www" in j or ".com" in j and "@" not in j:
       dict1["web"].append(j)
    if "@" in j:
      dict1["email-id"].append(j)
    a = re.findall(r'[0-9]{6}',j)
    if len(a)==1:
      dict1['address'].append(a[0])
  
  dict1["ph.no"].append(m[0])
  df = pd.DataFrame(dict1)
  return(df)

def convert_df(df):
    
    return df.to_csv().encode('utf-8')


 
    




 


st.title("BUISSNESS CARD EXTRACTIONS")

col1, col2 = st.columns(2)
with col1:
  upload_image = st.file_uploader("UPLOAD AN IMAGE FOR EXTRACTION", type=["jpg", "jpeg", "png"])
  st.write(upload_image)
# CHECKING A IMAGE IS UPLOADED OR NOT BY VIEWING 
  if upload_image is not None:
    image = Image.open(upload_image)
    m = upload_image.name
    st.write("File Name :", upload_image.name)
    st.image(image, caption='Uploaded Business Card Image')
  

    if st.button('CLICK TO EXTRACT DATA'):
      st.write("DATA EXTRACTION FROM BUISSNESS CARD HAS BEEN INITIATED...")
      a = bcard(img = m)
      st.table(a)
      a.to_sql('extraction',engine, if_exists='replace', index=False)
    if st.button("Click To Download"):
      st.write("DETAILS EXTRACTED FROM BUISSNESS CARD AS TABLE")
      csv = convert_df(df=a)
      st.download_button(
      label="DOWNLOAD DATA AS  CSV",
      data=csv,
      file_name='businesscard.csv',
      mime='csv',)

  else:
    st.write("Please Upload card Image")
  
    # genre = st.radio( "PLEASE SELECT THE UPDATING COLUMN",
    #   ('name', 'designation', 'ph.no','web','email-id','address'))
    # if genre == 'name':
    #    title1 = st.text_input('ENTER THE NAME TO BE UPDATE')
    #    def update_name( pde ):
    #      query1 = ("UPDATE EXTRACTION SET name = %s")
    #      gt.execute(query1, (pde,))
    #      conn.commit()
    #      query2 = ("select * from EXTRACTION")
    #      gt.execute(query2)
    #      q3 = gt.fetchall()
    #      conn.commit()
    #      one = pd.DataFrame(q3,columns = ['name','designation','ph_no','web','email','address'])
    #      return one
     
    #    DD = update_name( pde = title1 )
    #    DD.to_sql('extraction',engine, if_exists='replace', index=False)
    #    st.table(a)
    #    st.write('DATA UPDATED')
      
      
        
    
   
    
      

      

# with col2:
#   if st.button('CLICK TO STORE IN DATABASE'):
    
#     output = bcard(img=upload_image.name)
#     st.write(output)
#     st.write("DATA EXTRACTION DONE")
#     output.to_sql('collections',engine, if_exists='append',index=False)
#     st.write("done")
#     query = ("select distinct * from collections")
#     gt.execute(query)
#     q1 = gt.fetchall()
#     wd = pd.DataFrame(q1,columns = ['name','designation','ph_no','web','email','address'])
#     st.table(wd)
#     st.write("DATA EXTRACTED")
#     csv = convert_df(df=wd)
#     st.download_button(
#       label="DOWNLOAD DATA AS WHOLE CSV",
#       data=csv,
#       file_name='businesscard.csv',
#       mime='csv',
#     )
#   if st.button('CLICK TO UPDATE DATABASE'):

