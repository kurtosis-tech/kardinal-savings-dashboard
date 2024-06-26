import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

T2_MICRO_COST = 0.0116
T2_SMALL_COST = 0.023
T2_MEDIUM_COST = 0.0464
WORKING_HOURS_PER_MONTH = 173.2 # Average Monthly Working Hours: 40 hours/week×4.33 weeks/month=173.2 hours/month

st.title("Kardinal Cash Saving Dashboard")
st.header("Replace your Remote Dev Sandboxes")

loom_video_url = "https://www.loom.com/embed/14338fb1ed114e10b7ab2d8f02c3afd6?sid=d6fe2403-9084-4722-9e47-e8d5f0b64ad4"

# Embedding the Loom video
components.iframe(src=loom_video_url, width=640, height=356)

st.divider()

st.subheader("Put in your orgs numbers to see cost savings")

def cost_per_hour_rendering(cost_per_hour):
    if (cost_per_hour == T2_MICRO_COST):
        return "1 vCPU, 1GB RAM (t2 micro)"
    elif (cost_per_hour == T2_SMALL_COST):
        return "1 vCPU, 2GB RAM (t2 small)"
    elif (cost_per_hour == T2_MEDIUM_COST):
        return "2 vCPU, 4GB RAM (t2 medium)"

config_container = st.container(border=True)

col1, col2, col3 = st.columns(3)
with col1:
    num_engineers = config_container.number_input("Number of engineers in your org using dev sandboxes: ", value=60)
with col2:
    num_services = config_container.number_input("Number of stateless microservices in your architecture: ", value=20)
with col3:    
    resource_usage_per_service = config_container.selectbox("Average resource requirement per service:",
            (0.0116, 0.023, 0.0464), format_func=cost_per_hour_rendering, index=1)

def calculate_cost_before(num_engineers, num_services, cost_per_service_hour):
    num_services_before = num_engineers * num_services
    return num_services_before * cost_per_service_hour

def calculate_cost_kardinal(num_engineers, num_services, cost_per_service_hour):
    num_services_kardinal = num_engineers + num_services
    return num_services_kardinal * cost_per_service_hour

def calculate_savings(num_engineers, num_services, cost_per_service_hour):
    return calculate_cost_before(num_engineers, num_services, cost_per_service_hour) - calculate_cost_kardinal(num_engineers, num_services, cost_per_service_hour)

st.divider()

cost_before = calculate_cost_before(num_engineers, num_services, resource_usage_per_service)
cost_after = calculate_cost_kardinal(num_engineers, num_services, resource_usage_per_service)

before_col, after_col = st.columns(2)

with before_col:
    before_container = st.container(border=True)
    before_container.subheader("Your Stateless Cloud Cost Before")
    cost_before = calculate_cost_before(num_engineers, num_services, resource_usage_per_service)
    before_container.metric("Your cost before per hour (stateless services)",
              f"${cost_before:,.2f}")
    before_container.metric("Your cost before per month (stateless services)",
              f"${cost_before * WORKING_HOURS_PER_MONTH:,.2f}")

with after_col:
    after_container = st.container(border=True)
    after_container.subheader("Your Stateless Cloud Cost After")
    cost_after = calculate_cost_kardinal(num_engineers, num_services, resource_usage_per_service)
    after_container.metric("Your cost after per hour (stateless services)",
              f"${cost_after:,.2f}")
    after_container.metric("Your cost after per month (stateless services)",
              f"${cost_after * WORKING_HOURS_PER_MONTH:,.2f}")

st.divider()

st.header("Your Cost Savings")

percentage_savings = (cost_before - cost_after)/cost_before

st.metric("You saved (percentage of previous cloud costs):", f"{percentage_savings:,.0%}")

savings_per_hour = calculate_savings(num_engineers, num_services, resource_usage_per_service)
savings_per_month = savings_per_hour * WORKING_HOURS_PER_MONTH
st.metric("Cost Saving Per Month, assuming your current dev sandboxes are only up 8hrs/day Mon-Fri.", f"${savings_per_month:,.2f}")