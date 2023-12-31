# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 20:40:46 2023

@author: hp
"""


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter


def proceed_world_bank_data_clean_and_transpose(filename):
    """
    Read the World Bank data from a CSV file, clean and transpose it.
    
    Args:
    - filename (str): Path to the CSV file containing World Bank data.
    
    Returns:
    - world_bank_data (DataFrame): Cleaned World Bank data.
    - transpose (DataFrame): Transposed World Bank data.
    """
    world_bank_data = pd.read_csv(filename).iloc[: -10]
    world_bank_data.drop(columns=['Country Code','Series Code','1990 [YR1990]', 
        '2014 [YR2014]', '2015 [YR2015]','2016 [YR2016]', '2017 [YR2017]', 
        '2018 [YR2018]','2019 [YR2019]', '2020 [YR2020]', '2021 [YR2021]', 
        '2022 [YR2022]'], inplace=True)
    world_bank_data.columns = [col.split(' ')[0] for col in 
                               world_bank_data.columns]
    transpose = world_bank_data.T
    transpose.columns = transpose.iloc[0]
    transpose = transpose.iloc[1:]
    transpose = transpose[transpose.index.str.isnumeric()]
    transpose.index = pd.to_numeric(transpose.index)
    transpose['Years'] = transpose.index
    return world_bank_data, transpose

def evaluate_summary_statistics(selected_data):
    """
    Evalute summary statistics for selected data.
    
    Args:
    - selected_data (DataFrame): Data for which summary statistics are 
    calculated.
    
    Returns:
    - summary_statistics (DataFrame): Summary statistics for the selected data.
    """
    summary_statistics = selected_data.groupby(['Series']).describe()
    return summary_statistics

def skew(data):
    """
    Calculate skewness for the given data.
    
    Args:
    - data (DataFrame): Data for which skewness is calculated.
    
    Returns:
    - skew_values (Series): Skewness values for the data.
    """
    skew_values = data.skew()
    print('Skew value:', skew_values)
    return skew_values

def kurt(data):
    """
    Calculate kurtosis for the given data.
    
    Args:
    - data (DataFrame): Data for which kurtosis is calculated.
    
    Returns:
    - kurt_values (Series): Kurtosis values for the data.
    """
    kurt_values = data.kurt()
    print('Kurt value:', kurt_values)
    return kurt_values

def selected_data_stats(selected_data):
    """
    Calculate mean, median, and standard deviation for selected data.
    
    Args:
    - selected_data (DataFrame): Data for which statistics are calculated.
    
    Returns:
    - mean_value (float): Mean value of the selected data.
    - median_value (float): Median value of the selected data.
    - std_dev_value (float): Standard deviation of the selected data.
    """
    selected_data['2001'] = pd.to_numeric(selected_data['2001'],
                                          errors='coerce')
    mean_value = np.mean(selected_data['2001'])
    median_value = np.median(selected_data['2001'])
    std_dev_value = np.std(selected_data['2001'])
    print('Mean value:', mean_value)
    print('Median value:', median_value)
    print('Standard Deviation:', std_dev_value)
    return mean_value, median_value, std_dev_value


def picture_correlation(selected_data, selected_years):
    """
    Plot a correlation heatmap for selected data.
    
    Args:
    - selected_data (DataFrame): Data for which correlation is calculated.
    - selected_years (list of str): Years for which correlation is analyzed.
    """

    indicator_corr = selected_data.pivot_table(index='Country',
                                    columns='Series', values=selected_years)
    correlation_matrix = indicator_corr.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='BuPu', fmt='.2f')
    plt.title('Correlation Heatmap between Indicators')
    plt.xlabel('Series')
    plt.ylabel('Series')
    plt.show()

def plot_agricultural_and_cereal(data, title_agricultural, title_cereal):
    """
    Plot bar graphs for agricultural land and cereal yield data.
    
    Args:
    - data (DataFrame): Data containing agricultural and 
    cereal yield information.
    
    - title_agricultural (str): Title for the agricultural land plot.
    - title_cereal (str): Title for the cereal yield plot.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    
    bar_width = 0.09
    years = ['1998', '1999', '2000', '2001', '2002']
    
    colors_agricultural = ['blue', 'green', 'orange', 'red', 'purple']
    colors_cereal = ['cyan', 'magenta', 'yellow', 'black', 'pink']
    
    # Agricultural Land Plot
    agricultural_land = data[data['Series'] == 'Agricultural land (sq. km)']
    agricultural_land = agricultural_land.sort_values(by='2001',
                                                      ascending=True)
    countries_agricultural = np.arange(len(agricultural_land['Country']))
    
    for i, year in enumerate(years):
        ax1.bar(countries_agricultural + i * bar_width,
                agricultural_land[year], color=colors_agricultural[i],
                width=bar_width, edgecolor='k', label=year)
    
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Agricultural Land (sq. km)')
    ax1.set_title(title_agricultural)
    ax1.legend()
    ax1.set_xticks(countries_agricultural + bar_width * len(years) / 2)
    ax1.set_xticklabels(agricultural_land['Country'])

    # Cereal Yield Plot
    cereal_yield = data[data['Series'] == 'Cereal yield (kg per hectare)']
    cereal_yield = cereal_yield.sort_values(by='2001', ascending=True)
    countries_cereal = np.arange(len(cereal_yield['Country']))
    
    for i, year in enumerate(years):
        ax2.bar(countries_cereal + i * bar_width, cereal_yield[year],
                color=colors_cereal[i], width=bar_width,
                edgecolor='k', label=year)
    
    ax2.set_xlabel('Country')
    ax2.set_ylabel('Cereal yield (kg per hectare)')
    ax2.set_title(title_cereal)
    ax2.legend()
    ax2.set_xticks(countries_cereal + bar_width * len(years) / 2)
    ax2.set_xticklabels(cereal_yield['Country'])
    plt.tight_layout()
    plt.show()


def lineplot_Urban_population_and_Methane_emissions(world_bank_data):
    """
    Plot line graphs for urban population and methane emissions data.
    
    Args:
    - world_bank_data (DataFrame): Data containing urban population 
    and methane emissions information.
    """
    Years = ['2001', '2002', '2003', '2004']

    # expression Urban Population data
    Urban_population = world_bank_data[world_bank_data[
        'Series'] == 'Urban population']
    Urban_population.set_index('Country', inplace=True)

    # expression Methane Emissions data
    Methane_emissions = world_bank_data[world_bank_data[
        'Series'] == 'Methane emissions (% change from 1990)']
    Methane_emissions.set_index('Country', inplace=True)

    # Urban Population plot
    plt.figure(figsize=(12, 6))
    plt.plot(Urban_population.loc["Japan", Years],marker='D', label="Japan")
    plt.plot(Urban_population.loc["Kenya", Years],marker='D', label="Kenya")
    plt.plot(Urban_population.loc["Finland", Years],marker='D',label="Finland")
    plt.plot(Urban_population.loc["Italy", Years],marker='D', label="Italy")
    plt.xlabel("Year")
    plt.ylabel("Urban Population")
    plt.title("Urban Population across Countries")
    plt.legend()
    plt.grid()
    plt.show()

    # Methane Emissions plot
    plt.figure(figsize=(12, 6))
    plt.plot(Methane_emissions.loc["Japan", Years], marker='>', color='cyan', 
             label="Japan")
    plt.plot(Methane_emissions.loc["Kenya", Years], marker='>', color='yellow',
             label="Kenya")
    plt.plot(Methane_emissions.loc["Finland", Years], marker='>',color='black', 
             label="Finland")
    plt.plot(Methane_emissions.loc["Italy", Years], marker='>',color='magenta', 
             label="Italy")
    
    plt.xlabel("Year")
    plt.ylabel("Methane Emissions (% change from 1990)")
    plt.title("Methane Emissions")
    plt.legend(loc=4)
    y_ticks = plt.gca().get_yticks()
    plt.gca().set_yticks(sorted(y_ticks))
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
    plt.grid()
    plt.show()

# file path for World bank data
filename = r"C:\Users\hp\Desktop\World Bank Data - Series - Metadata.csv"

#Indicators from the world bank data
indicators = ['Agricultural land (sq. km)', 'Cereal yield (kg per hectare)',
              'Urban population', 'Methane emissions (% change from 1990)']

#Selected indicators from the world bank data
selec_indicators = ['Agricultural land (sq. km)',
                    'Cereal yield (kg per hectare)']

selected_years = ['2001']

# Call the function for world bank data
world_bank_data,transpose=proceed_world_bank_data_clean_and_transpose(filename)

selected_data = world_bank_data[world_bank_data['Country'].isin(
    selec_indicators)]

selected_data = world_bank_data[world_bank_data['Series'].isin(
    indicators)]

# Call the function for summary statistics
summary_statistics = evaluate_summary_statistics(selected_data)

# Call the function for skew and kurt
skew(summary_statistics)
kurt(summary_statistics)

# Call the function for selected data stats
selected_data_stats(selected_data)

# Call the function for picture correlation
picture_correlation(selected_data, selected_years)


indicator_stats = selected_data.groupby('Series').describe()

# Call the function for Agricultural Land and Cereal Yield
plot_agricultural_and_cereal(world_bank_data, 
     'Agricultural Land across Countries', 'Cereal yield across Countries')

# Call the function for Urban population and Methane emissions
lineplot_Urban_population_and_Methane_emissions(world_bank_data)