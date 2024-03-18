import streamlit as st
from PIL import Image
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import re

model = load_model('C:/Users/jhaga/OneDrive/Desktop/fr-project/Fruit_Vegetable_Recognition/venv/FV.h5')

labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango', 'Orange',
          'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']

st.title("CALOTRACK : Food calories Estimator and Classification")
st.session_state["cal_goal"] = st.text_input('Enter the calories goal', value= "300")
progress_bar = 0
pr_bar = st.progress(progress_bar, "Calories progress")
st.session_state["cur_cal"] = 0
container = st.container(border=True)
container.write("--FOOD-- : --CALORIES--")

if "cal_goal" not in st.session_state:
    st.session_state["cal_goal"] = st.text_input('Enter the calories goal')

if "cur_cal" not in st.session_state:
    st.session_state["cur_cal"] = 0


if "calo_list" not in st.session_state:
    st.session_state["calo_list"] = []



def fetch_calories(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        st.error("Can't able to fetch the Calories")
        print(e)


def prepare_image(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()


def run():

    weight = st.text_input('Enter the Weight in grams', value="100")
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, use_column_width=False)
        # save_image_path = './upload_images/' + img_file.name
        save_image_path = 'C:/Users/jhaga/OneDrive/Desktop/fr-project/Fruit_Vegetable_Recognition/venv/upload_images/' + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result = prepare_image(save_image_path)
            if result in vegetables:
                st.info('**Category : Vegetables**')
            else:
                st.info('**Category : Fruit**')
            st.success("**Predicted : " + result + '**')
            cal = fetch_calories(result)
            fcal = re.split(' ', cal)[0]
            tcal = (int(fcal) * int(weight))/100
            if cal:
                st.warning('Calories : ' + str(tcal))


            st.session_state["cur_cal"] = st.session_state["cur_cal"] + tcal
            st.session_state["calo_list"].append(result + " : " + str(tcal))
            st.write(st.session_state["cur_cal"])
            if int((st.session_state["cur_cal"]/float(st.session_state["cal_goal"]))*100) >= 100:
                st.error("Calories Goal attained !! 💥❤️")
            else:
                pr_bar.progress(int((st.session_state["cur_cal"]/float(st.session_state["cal_goal"]))*100))


for i, t in enumerate(st.session_state["calo_list"]):
    container.write(f"{i + 1}. {t}")


run()