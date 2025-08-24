import streamlit as st
import pandas as pd
from Graphing_and_plotting_stratos_data_4 import plot_selected_files

st.set_page_config(page_title="Flight Data Comparator", layout="centered")
st.title("Flight vs Simulation Data Comparator")

# Define standard column mapping schema
STANDARD_COLUMN_MAP = {
    'time': {
        'stratos': 'time',
        'ras': 'Time (sec)',
        'unit': 'Time (s)'
    },
    'altitude': {
        'stratos': 'altitude',
        'ras': 'Altitude (ft)',
        'unit': 'Altitude (ft)'
    },
    'speed': {
        'stratos': 'speed',
        'ras': 'Velocity (ft/sec)',
        'unit': 'Speed (ft/s)'
    },
    'acceleration': {
        'stratos': 'acceleration',
        'ras': 'Accel (ft/sec^2)',
        'unit': 'Total Acceleration (ft/s²)'
    },
    'vertical_acceleration': {
        'stratos': 'accel_z',
        'ras': 'Accel-V (ft/sec^2)',
        'unit': 'Vertical Acceleration (ft/s²)'
    },
    'horizontal_acceleration': {
        'stratos': 'accel_x',
        'ras': 'Accel-H (ft/sec^2)',
        'unit': 'Horizontal Acceleration (ft/s²)'
    },
    'pitch': {
        'stratos': 'gyro_pitch',
        'ras': 'Pitch Attitude (deg)',
        'unit': 'Pitch (deg)'
    },
    'distance': {
        'stratos': 'pad_dist',
        'ras': 'Distance (ft)',
        'unit': 'Distance (ft)'
    }
}

# Step 1: Upload actual flight data file
actual_file = st.file_uploader("Upload actual flight data CSV", type="csv")

# Step 2: Upload folder of simulation CSV files
sim_folder = st.file_uploader("Upload simulation CSVs", type="csv", accept_multiple_files=True)

if actual_file and sim_folder:
    actual_df = pd.read_csv(actual_file)

    sim_dfs = {}
    for sim_file in sim_folder:
        df = pd.read_csv(sim_file)
        sim_dfs[sim_file.name] = df

    # Step 3: Select which sim files to include
    st.subheader("Select simulation files to compare")
    selected_sim_dfs = {}
    for name, df in sim_dfs.items():
        if st.checkbox(name, value=True):
            selected_sim_dfs[name] = df

    if selected_sim_dfs:
        # Step 4: Filter to only keys where actual + all sims have columns
        column_map = {}
        for key, mapping in STANDARD_COLUMN_MAP.items():
            actual_col = mapping["stratos"]
            sim_col = mapping["ras"]

            if actual_col in actual_df.columns and all(sim_col in df.columns for df in selected_sim_dfs.values()):
                column_map[key] = {
                    "actual": actual_col,
                    "sims": {name: sim_col for name in selected_sim_dfs},
                    "unit": mapping["unit"]
                }

        if column_map:
            available_columns = list(column_map.keys())

            st.subheader("Plot Parameters")
            x_col = st.selectbox("Select X-axis", available_columns, index=0)
            y_col = st.selectbox("Select Y-axis", available_columns, index=1 if len(available_columns) > 1 else 0)

            # Step 5: Plot together or separate
            plot_together = st.checkbox("Graph all on one plot", value=True)

            if x_col and y_col:
                figs = plot_selected_files(actual_df, selected_sim_dfs, x_col, y_col, plot_together)

                if isinstance(figs, list):
                    for fig in figs:
                        st.pyplot(fig)
                else:
                    st.pyplot(figs)