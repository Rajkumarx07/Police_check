import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(page_title="SecureCheck Dashboard", layout="wide")
st.title("🚓 SecureCheck - Police Post Log Dashboard")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="TS"
)
mycursor = mydb.cursor(dictionary=True)
mycursor.execute("SELECT * FROM traffic_stops")
df = pd.DataFrame(mycursor.fetchall())

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Home","Overview","Queries","Prediction"])

if page == "Home":
    st.markdown("""
    ### 🔐 SecureCheck: Police Post Log Dashboard

    Welcome to **SecureCheck**, a powerful and intuitive dashboard designed to assist law enforcement agencies in tracking and analyzing police post activity.  
    This system allows you to:

    - View total traffic stops, arrests, searches, and drug-related incidents.
    - Explore patterns in violations and enforcement using interactive visualizations.
    - Gain insights for data-driven policing and resource planning.

    Stay secure. Stay accountable. ✅
    """)

elif page == "Overview":
    st.subheader("Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Stops", len(df))
    col2.metric("Total Arrests", df['is_arrested'].sum())
    col3.metric("Drug-Related Stops", df['drugs_related_stop'].sum())
    col4.metric("Searches Conducted", df['search_conducted'].sum())

    st.subheader("Full Dataset")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("📊 Insights")

    daily_arrests = df[df['is_arrested'] == 1].groupby('stop_date').size().reset_index(name='arrest_count')
    linechart = px.line(daily_arrests, x='stop_date', y='arrest_count', title='Daily Arrest Count Over Time')
    st.plotly_chart(linechart)
    
    country_stats = df.groupby('country_name').agg(
    total_stops=('is_arrested', 'count'),
    total_arrests=('is_arrested', 'sum')
    ).reset_index()

    country_stats['arrest_rate'] = (country_stats['total_arrests'] / country_stats['total_stops']) * 100

    top_countries = country_stats.sort_values(by='arrest_rate', ascending=False).head(10)
    Pie = px.pie(
    top_countries,
    names='country_name',
    values='arrest_rate',
    title='Top Countries by Arrest Rate (%)',
    hole=0.4,
    hover_data=['total_arrests', 'total_stops']
    )
    st.plotly_chart(Pie)

    
    gender_drugs = df.groupby('driver_gender')['drugs_related_stop'].sum().reset_index()

    Bar = px.bar(
    gender_drugs,
    x='driver_gender',
    y='drugs_related_stop',
    color='driver_gender',
    title='Drug-Related Stops by Driver Gender',
    labels={'drugs_related_stop': 'Drug-Related Stops', 'driver_gender': 'Driver Gender'}
    )
    st.plotly_chart(Bar)

elif page == "Queries":
    st.subheader("🔎 Query Explorer")

    queries = [
        "1. Top 10 vehicles in drug-related stops",
        "2. Most frequently searched vehicles",
        "3. Age group with highest arrest rate",
        "4. Gender distribution by country",
        "5. Race-Gender combo with highest search rate",
        "6. Time of day with most stops",
        "7. Avg stop duration per violation",
        "8. Are night stops more likely to lead to arrests?",
        "9. Violations associated with search or arrest",
        "10. Common violations for drivers under 25",
        "11. Violations rarely resulting in search or arrest",
        "12. Countries with highest drug stop rate",
        "13. Arrest rate by country & violation",
        "14. Country with most searches conducted",
        "15. Yearly stops/arrests by country",
        "16. Violation trends by age and race",
        "17. Time-based stop analysis",
        "18. Violations with high search/arrest counts",
        "19. Demographics by country",
        "20. Top 5 violations with highest arrest rates"
    ]

    selected_query = st.selectbox("Choose a query to run:", queries)
    if st.button("Run Query"):
        sql = ""

        if selected_query == "1. Top 10 vehicles in drug-related stops":
            sql = """
            SELECT vehicle_number, COUNT(*) AS drug_related_count
            FROM traffic_stops
            WHERE drugs_related_stop = 1
            GROUP BY vehicle_number
            ORDER BY drug_related_count DESC
            LIMIT 10
            """

        elif selected_query == "2. Most frequently searched vehicles":
            sql = """
            SELECT vehicle_number, COUNT(*) AS search_count
            FROM traffic_stops
            WHERE search_conducted = 1
            GROUP BY vehicle_number
            ORDER BY search_count DESC
            LIMIT 10
            """

        elif selected_query == "3. Age group with highest arrest rate":
            sql = """
            SELECT 
                CASE
                    WHEN driver_age < 18 THEN '<18'
                    WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN driver_age BETWEEN 36 AND 50 THEN '36-50'
                    ELSE '50+'
                END AS age_group,
                COUNT(*) AS total,
                SUM(is_arrested) AS arrested,
                (SUM(is_arrested) / COUNT(*)) * 100 AS arrest_rate
            FROM traffic_stops
            GROUP BY age_group
            ORDER BY arrest_rate DESC
            """

        elif selected_query == "4. Gender distribution by country":
            sql = """
            SELECT country_name, driver_gender, COUNT(*) AS count
            FROM traffic_stops
            GROUP BY country_name, driver_gender
            """

        elif selected_query == "5. Race-Gender combo with highest search rate":
            sql = """
            SELECT driver_race, driver_gender, 
                   COUNT(*) AS total, 
                   SUM(search_conducted) AS searched,
                   (SUM(search_conducted)/COUNT(*)) * 100 AS search_rate
            FROM traffic_stops
            GROUP BY driver_race, driver_gender
            ORDER BY search_rate DESC
            LIMIT 1
            """

        elif selected_query == "6. Time of day with most stops":
            sql = """
            SELECT HOUR(stop_time) AS hour_of_day, COUNT(*) AS stop_count
            FROM traffic_stops
            GROUP BY hour_of_day
            ORDER BY hour_of_day
            """

        elif selected_query == "7. Avg stop duration per violation":
            sql = """
            SELECT violation, stop_duration, COUNT(*) AS count
            FROM traffic_stops
            GROUP BY violation, stop_duration
            """

        elif selected_query == "8. Are night stops more likely to lead to arrests?":
            sql = """
            SELECT 
                CASE 
                    WHEN HOUR(stop_time) < 6 OR HOUR(stop_time) > 20 THEN 'Night'
                    ELSE 'Day'
                END AS time_period,
                COUNT(*) AS total_stops,
                SUM(is_arrested) AS total_arrests,
                (SUM(is_arrested)/COUNT(*)) * 100 AS arrest_rate
            FROM traffic_stops
            GROUP BY time_period
            """

        elif selected_query == "9. Violations associated with search or arrest":
            sql = """
            SELECT violation, 
                   SUM(search_conducted) AS total_searched,
                   SUM(is_arrested) AS total_arrested
            FROM traffic_stops
            GROUP BY violation
            """

        elif selected_query == "10. Common violations for drivers under 25":
            sql = """
            SELECT violation, COUNT(*) AS count
            FROM traffic_stops
            WHERE driver_age < 25
            GROUP BY violation
            ORDER BY count DESC
            LIMIT 10
            """

        elif selected_query == "11. Violations rarely resulting in search or arrest":
            sql = """
            SELECT violation,
                   AVG(search_conducted) AS search_rate,
                   AVG(is_arrested) AS arrest_rate
            FROM traffic_stops
            GROUP BY violation
            HAVING search_rate < 0.05 AND arrest_rate < 0.05
            """

        elif selected_query == "12. Countries with highest drug stop rate":
            sql = """
            SELECT country_name,
                   COUNT(*) AS total_stops,
                   SUM(drugs_related_stop) AS drug_stops,
                   (SUM(drugs_related_stop)/COUNT(*)) * 100 AS drug_stop_rate
            FROM traffic_stops
            GROUP BY country_name
            ORDER BY drug_stop_rate DESC
            LIMIT 10
            """

        elif selected_query == "13. Arrest rate by country & violation":
            sql = """
            SELECT country_name, violation,
                   COUNT(*) AS total_stops,
                   SUM(is_arrested) AS total_arrests,
                   (SUM(is_arrested)/COUNT(*)) * 100 AS arrest_rate
            FROM traffic_stops
            GROUP BY country_name, violation
            """

        elif selected_query == "14. Country with most searches conducted":
            sql = """
            SELECT country_name, COUNT(*) AS search_count
            FROM traffic_stops
            WHERE search_conducted = 1
            GROUP BY country_name
            ORDER BY search_count DESC
            LIMIT 1
            """

        elif selected_query == "15. Yearly stops/arrests by country":
            sql = """
            SELECT country_name, YEAR(stop_date) AS year,
                   COUNT(*) AS total_stops,
                   SUM(is_arrested) AS total_arrests
            FROM traffic_stops
            GROUP BY country_name, year
            ORDER BY year
            """

        elif selected_query == "16. Violation trends by age and race":
            sql = """
            SELECT driver_age, driver_race, violation, COUNT(*) AS count
            FROM traffic_stops
            GROUP BY driver_age, driver_race, violation
            """

        elif selected_query == "17. Time-based stop analysis":
            sql = """
            SELECT YEAR(stop_date) AS year, 
                   MONTH(stop_date) AS month,
                   HOUR(stop_time) AS hour,
                   COUNT(*) AS stop_count
            FROM traffic_stops
            GROUP BY year, month, hour
            ORDER BY year, month, hour
            """

        elif selected_query == "18. Violations with high search/arrest counts":
            sql = """
            SELECT violation,
                   COUNT(*) AS total,
                   SUM(search_conducted) AS search_count,
                   SUM(is_arrested) AS arrest_count
            FROM traffic_stops
            GROUP BY violation
            ORDER BY search_count DESC, arrest_count DESC
            LIMIT 10
            """

        elif selected_query == "19. Demographics by country":
            sql = """
            SELECT country_name,
                   AVG(driver_age) AS avg_age,
                   COUNT(*) AS total_stops,
                   SUM(is_arrested) AS arrest_count
            FROM traffic_stops
            GROUP BY country_name
            """

        elif selected_query == "20. Top 5 violations with highest arrest rates":
            sql = """
            SELECT violation,
                   COUNT(*) AS total,
                   SUM(is_arrested) AS arrested,
                   (SUM(is_arrested)/COUNT(*)) * 100 AS arrest_rate
            FROM traffic_stops
            GROUP BY violation
            ORDER BY arrest_rate DESC
            LIMIT 5
            """

        if sql:
            mycursor.execute(sql)
            result = pd.DataFrame(mycursor.fetchall())
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("Query not found.")
    
elif page == "Prediction":
    st.subheader("Reference Dataset")
    st.dataframe(df, use_container_width=True)
    st.markdown("___")
    st.markdown("Built with ❤️ for Law Enforcement by SecureCheck")
    st.header("🧠 Custom Natural Language Filter")

    st.markdown("Fill in the details below to get a natural language prediction of the stop outcome based on existing data.")

    st.header("📝 Log New Police Stop & Predict Outcome and Violation")


    with st.form("new_log_form"):
        stop_date = st.date_input("🗓️ Date of Stop")
        stop_time = st.time_input("⏱️ Time of Stop")
        country_name = st.selectbox("📍 Country Name" , ["Canada" , "India" , "USA"])
        driver_gender = st.selectbox("🚻 Driver Gender", ["male", "female"])
        driver_age = st.number_input("🎂 Driver Age", min_value=16, max_value=100, value=27)
        search_options = {"Yes" : 1 , "No" : 0} 
        search_conducted = st.selectbox("🔍 Was a Search Conducted?",  list(search_options.keys()))
        drug_options = {"Yes" : 1 , "No" : 0}
        drugs_related_stop = st.selectbox("💊 Was it Drug Related?", list(drug_options.keys()))
        stop_duration = st.selectbox("⏳ Stop Duration", ['0-15 Min', '16-30 Min', '30+ Min'])  # You can replace this with dynamic data
        vehicle_number = st.text_input("🚗 Vehicle Number")
        timestamp = pd.Timestamp.now()

        search_conducted_val = search_options[search_conducted]
        drugs_related_stop_val = drug_options[drugs_related_stop]

        submitted = st.form_submit_button("🔎 Predict Stop Outcome & Violation")

    if submitted:
        filtered_data = df[
        (df['country_name'] == country_name) &
        (df['driver_gender'] == driver_gender) &
        (df['driver_age'] == driver_age) &
        (df['search_conducted'] == search_conducted_val) &
        (df['stop_duration'] == stop_duration) &
        (df['drugs_related_stop'] == drugs_related_stop_val)
        ]

        if not filtered_data.empty:
            predicted_outcome = filtered_data['stop_outcome'].mode()[0]
            predicted_violation = filtered_data['violation'].mode()[0]
        else:
            predicted_outcome = "warning"  # Default
            predicted_violation = "speeding"  # Default

        search_text = "a search was conducted" if search_conducted_val else "no search was conducted"
        drug_text = "was drug-related" if drugs_related_stop_val else "was not drug-related"  

        st.markdown(f"""
        ### 📄 **Prediction Summary**

        - **Predicted Violation:** `{predicted_violation}`
        - **Predicted Stop Outcome:** `{predicted_outcome}`

        📌 A {driver_age}-year-old {driver_gender} driver in **{country_name}** was stopped at **{stop_time.strftime('%I:%M %p')}** on **{stop_date}**.
        The stop {search_text}, and it {drug_text}.  
        ⏳ **Stop Duration**: `{stop_duration}`  
        🚗 **Vehicle Number**: `{vehicle_number}`
        """)