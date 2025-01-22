#Import libraries to open dataset and use Streamlit
import streamlit as st
import base64
import pickle
import numpy as np

#Open dataset
pipe = pickle.load(open('model/pipe_object.pkl', 'rb'))
df = pickle.load(open('model/laptop_data.pkl', 'rb'))
st.title('Laptop Price Estimation')

# Creating two column layout
left_column, right_column = st.columns(2)

# Left Column
with left_column:
    st.subheader("Basic details")
    # Company Brand
    company = st.selectbox('Brand', df['Company'].unique())

    # Laptop Type
    type = st.selectbox('Type', df['TypeName'].unique())

    # OS
    os = st.selectbox('OS', df['os'].unique())

    # Weight
    weight = st.number_input("Laptop's Weight(Kg)", min_value=0.8, max_value=4.6, value=1.8, step=0.1)

# Right Column
with right_column:
    st.subheader("Specifications")
    
    # Create a two-column layout
    left_advanced, right_advanced = st.columns(2)
    
    with left_advanced:
        # TouchScreen
        touchscreen = st.selectbox('TouchScreen', ['No', 'Yes'])

        # Display
        ips = st.selectbox('IPS', ['Yes', 'No'])

        # Screen Size
        screen_size = st.selectbox('Screen Size (Inch)', [11.6, 13.3, 14.0, 15.6, 17.3])

        # Resolution
        resolution = st.selectbox('Screen Resolution', ['1920 x 1080', '1366 x 768', '1440 x 900',
                                                        '1600 x 900', '3840 x 2160', '3200 x 1800',
                                                        '2880 x 1800', '2560 x 1600', '2560 x 1440',
                                                        '2304 x 1440'])

        # RAM
        ram = st.selectbox('RAM(GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64], index=2)

    with right_advanced:
        # CPU
        cpu = st.selectbox('CPU', df['Cpu Brand'].unique())

        # GPU
        gpu = st.selectbox('GPU', df['GpuBrand'].unique())

        # HDD
        hdd = st.selectbox('HDD(GB)', [0, 256, 512, 1024, 2048])

        # SSD
        ssd = st.selectbox('SSD(GB)', [0, 128, 256, 512, 1024])


if st.button('Predict Price'):
    # Preprocess input features
    touchscreen = int(touchscreen == 'Yes')
    ips = int(ips == 'Yes')
    X_res, Y_res = map(int, resolution.split('x'))
    ppi = ((X_res**2 + Y_res**2)**0.5) / screen_size

    # Create query array and make the prediction
    query = np.array([company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os]).reshape(1, -1)
    predicted_price = int(np.exp(pipe.predict(query)[0]))

    # Display the result
    st.title(f"\nPrice: {round(predicted_price)} EUR")


#Requirement to upload background
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


#Create background function
def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

#Apply background
set_png_as_page_bg('assets/Background.png')