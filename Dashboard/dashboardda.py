import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

#product_df = pd.read_csv('product_count_df.csv')
product_df = pd.read_csv('product_count_english_df.csv')
revenue_df = pd.read_csv('revenue_by_day_df.csv')
items_orders_df = pd.read_csv("items_orders.csv")
orders_customers_df = pd.read_csv("orders_customers.csv")

st.set_page_config(layout="wide")

# Ensuring that the 'order_approved_at' column has the 'datetime' data type
revenue_df['order_approved_at'] = pd.to_datetime(revenue_df['order_approved_at'])


# Creating a date range component for use in the sidebar
min_date = revenue_df['order_approved_at'].min()
max_date = revenue_df['order_approved_at'].max()

with st.sidebar:
    # Creating a slider to determine the time range
    start_date, end_date = st.date_input(label=':blue[Rentang Waktu]',
                                         min_value=min_date,
                                         max_value=max_date,
                                         value=[min_date, max_date],
                                         )

main_df = revenue_df[(revenue_df['order_approved_at'] >= str(start_date))
                     & (revenue_df['order_approved_at'] <= str(end_date))]


st.title("Proyek Data Analis: E-Commerce Public Dataset")

#Jumlah Penjualan Harian
st.subheader('Penjualan Harian')

col1, col2 = st.columns(2)

with col1:
    total_orders = main_df.total_order.sum()
    st.metric('Total Penjualan', value=total_orders)

with col2:
    total_revenue = format_currency(main_df.total_revenue.sum(), "$BRL", locale='ES_CO')
    st.metric('Total Pendapatan', value=total_revenue)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(revenue_df['order_approved_at'], revenue_df['total_order'], marker='s', linewidth=3, color='#FA968F')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.set_title('Total Pendapatan 2016/07 - 2018/07', fontsize=30)
st.pyplot(fig)

#Kategori Produk berdasarkan Jumlah Penjualan
st.subheader('Kategori Produk dengan Performa Terbaik dan Terburuk berdasarkan Jumlah Penjualan')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25, 8))
colors = ["#FA968F", "#2795F5", "#2795F5", "#2795F5", "#2795F5"]

sns.barplot(x='total_order', y='product_category_name_english',
            data=product_df.groupby('product_category_name_english').total_order.nunique().sort_values(ascending=False).reset_index().head(5),
            palette=colors, ax=ax[0])
ax[0].set_ylabel('Kategori Produk', fontsize=16)
ax[0].set_xlabel('Jumlah Order', fontsize=16)
ax[0].set_title('Produk dengan Jumlah Penjualan Terbaik', fontsize=25)
ax[0].tick_params(axis='y', labelsize=20)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x='total_order', y='product_category_name_english',
            data=product_df.groupby('product_category_name_english').total_order.nunique().sort_values(ascending=True).reset_index().head(5),
            palette=colors, ax=ax[1])
ax[1].set_ylabel('Kategori Produk', fontsize=16)
ax[1].set_xlabel('Jumlah Order', fontsize=16)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].yaxis.set_label_position('right')
ax[1].set_title('Produk dengan Jumlah Penjualan Terburuk', fontsize=25)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis='x', labelsize=20)

plt.suptitle('Produk dengan Jumlah Penjualan Terbaik dan Terburuk berdasarkan kategori', fontsize=30)
st.pyplot(fig)

#Customers Demografi
st.subheader('Customers Demografi')

def create_bycity_df(df):
    bycity_df = orders_customers_df.groupby("customer_city").customer_id.nunique().reset_index().sort_values(by='customer_id', ascending=False).head(5)
    bycity_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

    return bycity_df

def create_bystate_df(df):
    bystate_df = orders_customers_df.groupby("customer_state").customer_id.nunique().reset_index().sort_values(by='customer_id', ascending=False).head(5)
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

    return bystate_df

bycity_df =create_bycity_df(main_df)
bystate_df =create_bystate_df(main_df)

fig, ax = plt.subplots(ncols=1, figsize=(15, 5))
colors = ["#FA968F", "#2795F5", "#2795F5", "#2795F5", "#2795F5"]

sns.barplot(x="customer_count", y="customer_city",
            data=bycity_df.sort_values(by="customer_count", ascending=False),
            palette=colors)
ax.set_ylabel('City Name', fontsize=12)
ax.set_xlabel('Customer Count', fontsize=12)
ax.set_title('Jumlah Customer Berdasarkan City', fontsize=18)
ax.tick_params(axis='y', labelsize=14)

sns.barplot(x="customer_count", y="customer_state",
            data=bystate_df.sort_values(by="customer_count", ascending=False),
            palette=colors)
ax.set_ylabel('State Name', fontsize=12)
ax.set_xlabel('Customer Count', fontsize=12)
ax.set_title('Jumlah Customer Berdasarkan State', fontsize=18)
ax.tick_params(axis='y', labelsize=14)

plt.suptitle('Jumlah Customer Berdasarkan City dan State', fontsize=30)
st.pyplot(fig)

hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            #footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
