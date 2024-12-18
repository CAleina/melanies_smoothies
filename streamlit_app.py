# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_cup = st.text_input("What name should we put on the Smoothie?")
st.write("The name that will appear on the Smoothie is", name_on_cup)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect('Choose up to 6 ingredients:',
                                    my_dataframe,
                                    max_selections = 6)

if ingredient_list:

    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders (ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+name_on_cup+"""')"""
    
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_cup+'!', icon="✅")

