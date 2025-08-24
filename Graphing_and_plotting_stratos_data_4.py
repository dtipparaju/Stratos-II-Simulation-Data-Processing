def plot_selected_files(actual_data, selected_files, x_axis, y_axis, plot_together=True):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    # Convert actual_data units from metric to imperial for matching with RAS Aero files
    if 'altitude' in actual_data.columns:
        actual_data['altitude'] = actual_data['altitude'] * 3.28084  
    if 'speed' in actual_data.columns:
        actual_data['speed'] = actual_data['speed'] * 3.28084  
    if 'acceleration' in actual_data.columns:
        actual_data['acceleration'] = actual_data['acceleration'] * 3.28084  
    if 'accel_z' in actual_data.columns:
        actual_data['accel_z'] = actual_data['accel_z'] * 3.28084
    if 'accel_x' in actual_data.columns:
        actual_data['accel_x'] = actual_data['accel_x'] * 3.28084
    if 'distance' in actual_data.columns:
        actual_data['distance'] = actual_data['distance'] * 3.28084

    column_map = {
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

    if x_axis not in column_map or y_axis not in column_map:
        print("Invalid axis variable.")
        return

    actual_data_x = column_map[x_axis]['stratos']
    actual_data_y = column_map[y_axis]['stratos']
    ras_x = column_map[x_axis]['ras']
    ras_y = column_map[y_axis]['ras']
    x_label = column_map[x_axis]['unit']
    y_label = column_map[y_axis]['unit']

    figures = []

    if plot_together:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(actual_data[actual_data_x], actual_data[actual_data_y], label='Actual Flight Data', color='black')
        for file_name, df in selected_files.items():
            ax.plot(df[ras_x], df[ras_y], label=file_name, linestyle='--')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(f"{y_label} vs {x_label}")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()
        figures.append(fig)
    else:
        for file_name, df in selected_files.items():
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(actual_data[actual_data_x], actual_data[actual_data_y], label='Actual Flight Data', color='black')
            ax.plot(df[ras_x], df[ras_y], label=file_name, linestyle='--')
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(f"{y_label} vs {x_label} - {file_name}")
            ax.legend()
            ax.grid(True)
            fig.tight_layout()
            figures.append(fig)

    return figures if not plot_together else figures[0]


