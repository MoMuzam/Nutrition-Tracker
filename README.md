Required Assets to run the program:

import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
import pandas as pd
import plotly.express as px
import datetime 


Our app is called Nutrition Tracker. The application enables users to comprehend the nutritional content of 
their daily food and beverage consumption. The team is called Code Munchers with members: Mohammed,
Sofiya, Rubdeep, and Adrian. The users of this application need to take a photo of what they are going to be consuming,
and add the photo of it through the app. Powered by Gemini API, the application employs the LLM’s image recognition technology 
to dissect the image and produce an estimation of the dietary content. The system creates automatic dietary information 
which includes calories, protein, carbohydrates and fat content for the user. The system simplifies nutrition tracking by
eliminating the need for users to look up or type in their food intake. The application functions also as a drink identification 
system. The app processes drink images to determine their calorie content and nutritional information when users photograph their beverages.
The system enables users to maintain a complete record of their daily food and drink consumption which helps them track their calorie and
nutrient consumption throughout the day. The score helps users assess the total nutritional value of their meal. Foods with higher scores
that approach 100 point value show greater healthiness because they provide their users with essential nutrients together with 
decreased harmful fat and sugar content and valuable vitamin and protein resources. Foods that receive lower scores contain high
amounts of calories together with added sugars and harmful fats and excessive sodium content. The application will show a brief 
explanation for each food rating which explains the reasons behind the score through its explanation of the ingredients and nutrients 
that contributed to the final rating. The application will show users whether their food choices become dangerous through regular consumption
because it contains excessive amounts of sugar and processed food components and harmful fats. The meal assessment will show its beneficial parts
which include high protein content and fiber and other valuable nutrients. 



