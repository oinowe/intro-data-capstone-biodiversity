#!/usr/bin/python
"""
Author: Oscar Inowe
Copyright: 2018, Data Analysis Intensive"
Email: osinam14@gmail.com
Status: Finished
Software: PyCharm Community Edition
Style Guide: PEP-8
Notes: Prints used for testing and visualization of data
"""

from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency
import pandas as pd


def plot_data(data):
    plt.figure(figsize=(10, 4))
    ax = plt.subplot()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.bar(range(len(data)),
            data.scientific_name.values, color="#3F5D7D")
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data.conservation_status.values)
    plt.ylabel('Number of Species')
    plt.title('Conservation Status by Species')
    plt.savefig("conservation.png")
    plt.show()


def plot_observations_data(observation_data):
    plt.figure(figsize=(16, 4))
    ax = plt.subplot()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.bar(range(len(observation_data)),
            observation_data.observations.values, color="#3F5D7D")
    ax.set_xticks(range(len(observation_data)))
    ax.set_xticklabels(observation_data.park_name.values)
    plt.ylabel('Number of Observations')
    plt.title('Observations of Sheep per Week')
    plt.savefig("observations.png")
    plt.show()


def pie_observations_data(observation_data):
    labels = ['Bryce', 'Great Smoky Mountains', 'Yellowstone', 'Yosemite']

    # colors
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    explode = (0.05, 0.05, 0.05, 0.05)

    plt.figure(figsize=(10, 8))
    ax = plt.subplot()
    plt.pie(observation_data.observations, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90,
            pctdistance=0.85, explode=explode)
    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    plt.tight_layout()
    plt.savefig("observations_pie.png")
    plt.show()


def biodiversity():
    species = pd.read_csv('species_info.csv')

    # Information to display
    # print species.head() # Head
    # print species.groupby('category').category.count() # Categories
    # print species.scientific_name.nunique() # Distinct Species
    # print species.category.unique() # Values of category
    # print species.conservation_status.unique() # Values of conservation_status

    """
    The column conservation_status has several possible values:
    Species of Concern: declining or appear to be in need of conservation
    Threatened: vulnerable to endangerment in the near future
    Endangered: seriously at risk of extinction
    In Recovery: formerly Endangered, but currently neither in danger of extinction throughout all or a significant portion of its range
    """

    species.fillna('No Intervention', inplace=True)  # Fill NaN values
    protection_counts = species.groupby('conservation_status').scientific_name.count().reset_index().sort_values(
        by='scientific_name')
    # print protection_counts

    plot_data(protection_counts)

    #
    species['is_protected'] = species.conservation_status != 'No Intervention'
    # print species

    category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()
    category_pivot = category_counts.pivot(columns='is_protected', index='category',
                                           values='scientific_name').reset_index()
    category_pivot.columns = ['category', 'not_protected', 'protected']  # Rename columns
    category_pivot['percent_protected'] = category_pivot.protected / (
                category_pivot.protected + category_pivot.not_protected)
    # print category_pivot

    # Chi Squared Test
    #  -- category -- protected -- not protected
    #     Mammal   --     30    --      146
    #     Bird     --     75    --      413
    contingency = [[30, 146],
                   [75, 413]]

    chi2, pval, dof, expected = chi2_contingency(contingency)
    # print "Not significant < 0.05", pval # Not significant Difference < 0.05

    # Chi Squared Test
    #  -- category -- protected -- not protected
    #     Mammal   --     30    --      146
    #     Reptile  --     5     --      73

    contingency = [[30, 146],
                   [5, 73]]
    chi2, pval, dof, expected = chi2_contingency(contingency)
    # print "Significant > 0.05", pval # Significant Difference > 0.05

    ################
    # OBSERVATIONS #
    ################

    observations = pd.read_csv('observations.csv')
    species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
    # species.head()

    #
    # print species[species.is_sheep]
    sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
    # print sheep_species

    #
    sheep_observations = observations.merge(sheep_species)
    # print sheep_observations

    #
    obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
    # print obs_by_park

    plot_observations_data(obs_by_park)
    pie_observations_data(obs_by_park)

    # minimum = 100.0 * 0.05 / 0.15
    # base = 15
    size_per_variant = 510  # According to https://www.optimizely.com/sample-size-calculator/?conversion=15&effect=33.33&significance=90
    print "Weeks to observe in Bryce National Park:", float(size_per_variant) / float(obs_by_park.observations[0])
    print "Weeks to observe in Yellowstone:", float(size_per_variant) / float(obs_by_park.observations[2])


if __name__ == '__main__':
    print "Codeacademy Intensive - Oscar Inowe - Final Project (Biodiversity)"
    biodiversity()
