import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import warnings

warnings.filterwarnings("ignore")

# Set page configuration
st.set_page_config(
    page_title="Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

# Title and file upload
st.title(":bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Choose a file", type=["csv", "xlsx"])

# Load data
if fl is not None:
    filename = fl.name
    st.write(f"File name: {filename}")
    df = pd.read_csv(filename)
else:
    df = pd.read_excel("Sample - Superstore.xls")

# Date filtering
col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

# Sidebar filters
st.sidebar.header("Choose your filter: ")

# Region filter
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# State filter
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# City filter
city = st.sidebar.multiselect("Pick the City", df3["City"].unique())

# Filtering based on Region, State, and City
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df3["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df3["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

# Visualizations
# Category wise Sales
category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()
cl1,cl2 = st.columns((2))
with cl1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

# Region wise Sales
with cl2:   
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig.update_traces(text=filtered_df["Region"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# Data Exploration
# Category View Data
with st.columns((2))[0]:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                            help='Click here to download the data as a CSV file')

# Region View Data
with st.columns((2))[1]:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

# Monthly Sales Visualization
filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M').astype(str)
st.subheader("Monthly Sales")
linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"], as_index=False)["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x="month_year", y="Sales", template="gridon", labels={"month_year": "Month", "Sales": "Sales"},
               height=500, width=1000)
st.plotly_chart(fig2, use_container_width=True)

# Monthly View Data
with st.expander("Monthly_ViewData"):
    st.write(linechart.style.background_gradient(cmap="Oranges"))
    csv = linechart.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", data=csv, file_name="Monthly.csv", mime="text/csv",
                       help='Click here to download the data as a CSV file')

# Hierarchical View of Sales using TreeMap
st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values="Sales", color="Sub-Category",)
fig3.update_layout(margin=dict(t=50, l=25, r=25, b=25), height=800, width=650)
st.plotly_chart(fig3, use_container_width=True)

# Segment-wise and Category-wise Pie Charts
chart1, chart2 = st.columns(2)
with chart1:
    st.subheader("Segment wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Segment", hole=0.5, template="plotly_dark")
    fig.update_traces(text=filtered_df["Segment"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("Category wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Category", hole=0.5, template="plotly_dark")
    fig.update_traces(text=filtered_df["Category"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

# Month wise Sub-Category Sales Summary
with st.expander('Summary Table'):
    df_sample = df[0:5][['Region', 'State', 'City', 'Category', 'Sales', 'Profit', 'Quantity']]
    fig = ff.create_table(df_sample, colorscale='cividis')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('Month wise Sub-Category Sales Summary')
    filtered_df['month'] = filtered_df['Order Date'].dt.month_name()
    sub_category_year = pd.pivot_table(filtered_df, values='Sales', index=['Sub-Category'], columns='month')
    st.write(sub_category_year.style.background_gradient(cmap="Oranges"))

# Scatter Plot
data1 = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity")
data1['layout'].update(template='plotly_dark',
                       title='Relationship between Sales and Profit',
                       titlefont=dict(family="Arial", size=24),
                       xaxis=dict(title="Sales", titlefont=dict(size=18)),
                       yaxis=dict(title="Profit", titlefont=dict(size=18)))
st.plotly_chart(data1, use_container_width=True)

# View Data
with st.expander("View Data"):
    st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

# Download Original Data
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Data", data=csv, file_name="Superstore.csv", mime="text/csv")
