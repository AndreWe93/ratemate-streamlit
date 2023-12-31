from wordcloud import WordCloud
import matplotlib.pyplot as plt

import streamlit as st
import requests
import gmaps
import googlemaps
import pydeck as pdk

api_key = "AIzaSyBH2zXte15didv6k_rGf4dOqx4iw4scS8k"




page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://img.freepik.com/free-photo/top-view-christmas-decoration-with-copy-space_23-2148317986.jpg?w=2000&t=st=1701978701~exp=1701979301~hmac=59d6b096a2aef96adbd3dd69e793a4b768db782d37e297f3780a406b99baf196");
  background-size: cover;
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)



def show_google_map(place_id=None, api_key=None):
    if place_id and api_key:
        url = f"https://www.google.com/maps/embed/v1/place?key={api_key}&q=place_id:{place_id}&zoom=15"
        st.markdown(f'<iframe width="700" height="450" frameborder="0" style="border:0" src="{url}" allowfullscreen></iframe>', unsafe_allow_html=True)
    else:
        st.write("")



st.markdown("""<h1 style='color: #FF6347;'>RateMate</h1>""", unsafe_allow_html=True)


# st.markdown("""<p style='color: #6B8E23;'> Get your personal rating for the restaurant of your choice</p>"""
#             , unsafe_allow_html=True)
# st.markdown(""" """,
#             unsafe_allow_html=True)



gmaps = googlemaps.Client(key=api_key)

st.markdown("""<h1 style='color: #6B8E23;'>1. </h1>""", unsafe_allow_html=True)

dash1= st.container()

with dash1:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("<h4 style='text-align: center; color: grey ;'>Specify your preferences</h4>", unsafe_allow_html=True)

    with col5:
        price_review_weightage = st.slider("PRICE", 0.0, 1.0, 0.5)

    with col2:
        food_review_weightage = st.slider("FOOD", 0.0, 1.0, 0.5)

    with col3:
        service_review_weightage = st.slider("SERVICE", 0.0, 1.0, 0.5)

    with col4:
        ambience_review_weightage = st.slider("AMBIENCE", 0.0, 1.0, 0.5)


@st.cache_data(ttl=500)
def find_restaurant(place_name):
    places = gmaps.places(query=place_name, type='restaurant')

    if places['results']:
        restaurant = places['results'][0]
        return restaurant
    else:
        return None



@st.cache_data(ttl=300)
def results_for_restorant(restaurant_name, search_button):
    results = []
    url = None
    place_id = None
    lon = None

    if search_button:
        places = gmaps.places(query=restaurant_name, type='restaurant')
        #st.write(restaurant_name)
        restaurant = places['results'][0]
        if restaurant:
            results.append(f" {restaurant['name']}")
            results.append(f"Address: {restaurant['formatted_address']}")
            results.append(f"Google rating: {restaurant.get('rating', 'No rating')}")
            place_id = restaurant['place_id']
            google_maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            url = google_maps_url
            lat = restaurant['geometry']['location']['lat']
            lon = restaurant['geometry']['location']['lng']
        else:
            results.append("No restaurant found")
    return url, results, place_id

st.markdown("""<h1 style='color: #6B8E23;'>2. </h1>""", unsafe_allow_html=True)
st.markdown("<h4 style=' margin-bottom: -45px; color: grey ;'>Enter restaurant:</h4>", unsafe_allow_html=True)
restaurant_name = st.text_input("", "Restaurant")
search_button = st.button("Find")



url, results, place_id = results_for_restorant(restaurant_name, search_button)
for result in results:
    st.markdown(f"<p style='color:  #6B8E23;'>{result}</p>", unsafe_allow_html=True)
st.markdown(
    """<h6 style='color: grey;'>❗️ If this is not the restaurant you are looking for,
    please specify the search string, e.g. by entering a street.</h6>""",
    unsafe_allow_html=True
)


# local_guides_review_weightage = st.checkbox('Review only from local guides')

st.markdown("""<h1 style='color: #6B8E23;'>3. </h1>""", unsafe_allow_html=True)

search_button2 = st.button("Get Score")


# the selected value is returned by st.slider
# checkbox for local guides
if search_button2:
    st.snow()
    st.markdown('✅ Great, <u>**this restaurant**</u> has been chosen:', unsafe_allow_html=True)
    st.session_state.is_enter_pressed = False

    restaurant_name = find_restaurant(restaurant_name)
    url, results, place_id = results_for_restorant(restaurant_name['name'], search_button2)
    st.markdown(f"<h1 style='color: grey;'>{results[0]}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: grey;'>{results[1]}</p>", unsafe_allow_html=True)

    st.markdown(f"<h2 style='color: grey;'>{results[2]}</h2>", unsafe_allow_html=True)


    with st.spinner('😎 Please wait for it...'):

        # st.markdown("<h4 style='text-align: center; color: #6B8E23;'>PREDICTING</h4>", unsafe_allow_html=True)

        params = {
            'url': url,
            'price_review_weightage': price_review_weightage,
            'food_review_weightage': food_review_weightage,
            'service_review_weightage': service_review_weightage,
            'ambience_review_weightage': ambience_review_weightage,
            #'local_guides_review_weightage': local_guides_review_weightage
        }

        ratemate_api_url = 'https://ratemate-z2kqlvo2ta-ew.a.run.app/personal_score'
        response = requests.get(ratemate_api_url, params=params)

        # original_score = response.json()
        your_personal_score = response.json()["personal_score"]
        top_1_review = response.json()["top_1"]
        top_2_review = response.json()["top_2"]
        top_3_review = response.json()["top_3"]
        sub_price = response.json()["sub_price"]
        sub_service = response.json()["sub_service"]
        sub_atmosphere = response.json()["sub_atmosphere"]
        sub_food = response.json()["sub_food"]
        wordcloud_input = response.json()["wordcloud_input"]
        dist_price = response.json()["dist_price"]
        dist_service = response.json()["dist_service"]
        dist_atmosphere = response.json()["dist_atmosphere"]
        dist_food = response.json()["dist_food"]

        st.divider()

        #st.success("Prediction Complete!")
        #st.markdown("""<h1 style='color: #6B8E23;'>4. </h1>""", unsafe_allow_html=True)

        st.markdown(f"<h1 style='color: #6B8E23;'>⭐️ Your personal score is: {your_personal_score} ⭐️</h1>", unsafe_allow_html=True)

        # with st.expander("TOP REVIEWS"):

        #     st.markdown(f"<h6 style='color: grey;'>Top 1:</h6> {top_1_review}", unsafe_allow_html=True)
        #     st.markdown(f"<h6 style='color: grey;'>Top 2:</h6> {top_2_review}", unsafe_allow_html=True)
        #     st.markdown(f"<h6 style='color: grey;'>Top 3:</h6> {top_3_review}", unsafe_allow_html=True)

        dash2= st.container()
        with dash2:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h3 style='text-align: center; color: grey;'>Sub ratings:</h3>", unsafe_allow_html=True)


                categories = ['price', 'service', 'ambience', 'food']
                values = [sub_price, sub_service, sub_atmosphere, sub_food]

                fig, ax = plt.subplots()
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)
                ax.bar(categories, values, color='#228B22', alpha=0.6)

                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.set_ylim(3, 5)

                st.pyplot(fig)

            with col2:


                st.markdown("<h3 style='text-align: center; color: grey;'>Topic relevance:</h3>", unsafe_allow_html=True)

                labels = ['price', 'service', 'ambience', 'food']
                colors = ['#FFD700', '#FF4500', '#C0C0C0', '#228B22']
                sizes = [dist_price, dist_service, dist_atmosphere, dist_food]
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=70, textprops={'fontsize': 6})

                ax1.axis('equal')
                fig1.set_size_inches(2, 2)
                fig1.patch.set_alpha(0)
                st.pyplot(fig1)

        st.markdown(f"""
                <details>
                <summary style='color: #6B8E23; font-size: 24px; font-weight: bold;'>TOP REVIEWS</summary>
                <ul style='list-style-type: none; padding-left: 20px;'>
                    <p>&nbsp;</p>
                    <li><span style='color: #6B8E23;font-weight: bold; font-size: 18px;'>• Top 1: </span>{top_1_review}</li>
                    <p>&nbsp;</p>
                    <li><span style='color: #6B8E23;font-weight: bold; font-size: 18px;'>• Top 2: </span>{top_2_review}</li>
                    <p>&nbsp;</p>
                    <li><span style='color: #6B8E23;font-weight: bold; font-size: 18px;'>• Top 3: </span>{top_3_review}</li>
                </ul>
                </details>
                """, unsafe_allow_html=True)


        st.markdown("")
        st.markdown("")

        wordcloud = WordCloud(max_words=10000, min_font_size=10, height=800, width=1600,
                background_color="white", colormap="viridis").generate(wordcloud_input)

        # Display the word cloud using Matplotlib
        fig = plt.figure(figsize=(20,20))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(fig)


show_google_map(place_id, api_key)
