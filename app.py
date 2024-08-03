import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout='wide',page_title='Indian Startup Analysis')

df=pd.read_csv('startup_clean.csv')

st.sidebar.title('INDIAN Startup Fundings')

option=st.sidebar.selectbox('SELECT',['Overall Analysis','Startups','Investors'])

df['date']=pd.to_datetime(df['date'],errors='coerce')


df['year']=df['date'].dt.year



def investor_details(investor):
    st.title(investor)

    ### load the recent 5 investements of investor
    last_5_invest=df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount in Cr']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_5_invest,width=900)

    col1, col2 = st.columns(2)
    with col1:
        ## biggest investments
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount in Cr'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount in Cr'].sum().head(10)
        st.subheader('Top Sector Investments')
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f")

        st.pyplot(fig1)


    col3,col4=st.columns(2)

    with col3:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount in Cr'].sum().sort_values(ascending=False).head(6)
        st.subheader('Top Investment City')
        fig3, ax3 = plt.subplots()
        ax3.bar(city_series.index, city_series.values)

        st.pyplot(fig3)


    with col4:
        stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount in Cr'].sum().head(10)
        st.subheader('Round in Investment')
        fig4, ax4 = plt.subplots()
        ax4.pie(stage_series, labels=stage_series.index, autopct="%0.01f")

        st.pyplot(fig4)


    col5,col6=st.columns(2)

    with col5:
         st.subheader('Year Of Year Investments')
         year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount in Cr'].sum()
         fig5, ax5 = plt.subplots()
         ax5.plot(year_series.index,year_series.values)

         st.pyplot(fig5)

    with col6:
         st.subheader('Similar Investors')




def load_overall_analysis():
    st.title("Overall Analysis")

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        total=df['amount in Cr'].sum()

        st.metric('Total(approx)',str(round(total))+'Cr')

    with col2:
        #maximum amount infused in startup
        max_amount=df.groupby('startup')['amount in Cr'].max().sort_values(ascending=False).head(1).values[0]
        st.metric("Maximum",str(max_amount)+' Cr')


    with col3:
        average = df.groupby('startup')['amount in Cr'].sum().mean()

        st.metric('Average', str(round(average)) + ' Cr')

    with col4:
        num_startup=df['startup'].nunique()

        st.metric('Funded Startup', str(num_startup))


    st.header("Month On Month Graph")

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df=df.groupby(['year','month'])['amount in Cr'].sum().reset_index()
    else:
        temp_df=df.groupby(['year','month'])['amount in Cr'].count().reset_index()

    temp_df['x_axis']=temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    figg,axx=plt.subplots(figsize=(12, 6))   ## to increase size of plot
    axx.plot(temp_df['x_axis'],temp_df['amount in Cr'])
    axx.tick_params(axis='x', rotation=90,pad=10)


    st.pyplot(figg)







if option=='Startups':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startups Details')
elif option=='Investors':
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investors Details')
    if btn2:
        investor_details(selected_investor)
else:
    st.title("Overall Analysis")
    load_overall_analysis()