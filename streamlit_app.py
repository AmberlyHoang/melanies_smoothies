# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# https://docs.streamlit.io/develop/api-reference/widgets/st.text_input
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# removing select box
#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fruit is:", option)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect
ingredients_list = st.multiselect(
    "Choose up to five ingredients:",
    my_dataframe,
    max_selections=5
)

# also use 4 spaces to indent in python
# if ingredients_list is not null: then do everything below this line that is indented. 
if ingredients_list:
    #st.write("You selected:", ingredients_list)
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    # converting list to a string
    ingredients_string = ''

    # for loop block
    # for each fruit_chosen in ingredients_list multiselect box: do everything below this line that is indented.
    for fruit_chosen in ingredients_list:
        # += operator means "add this to what is already in the variable" so each time the FOR Loop is repeated, a new fruit name is appended to the existing string. 
        ingredients_string += fruit_chosen + ' ' 
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """' ) """

    #st.write(my_insert_stmt)
    #st.stop()

    #if ingredients_string:
    #    session.sql(my_insert_stmt).collect()
        
    #    st.success('Your Smoothie is ordered!', icon="✅")
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
