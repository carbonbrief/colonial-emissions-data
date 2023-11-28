The data behind the CarbonBrief article: [Revealed: Colonial rule nearly doubles UK's historical contribution to climate change](https://www.carbonbrief.org/revealed-how-colonial-rule-radically-shifts-historical-responsibility-for-climate-change/)

The main file to run is "colonial-emissions-2023-clean", which is a Jupyter notebook.
This Jupyter notebook processes the data in the input folder "input-clean" to produce the outputs in the output folder "output-clean".
The Jupyter notebook uses some additional functions which are defined in "functions.py". The required python packages are listed in "requirements.txt".

The .csv outputs from the notebook are the following, and include the data to plot all the graphics in the article:
- __article_summary_table_2023__: summary data for all countries above population 1 million in 2023, as shown in the summary table that is in the article
- __full_summary_table_2023__: additional summary data for all countries above population 1 million in 2023, including split of fossil and land emissions
- __full_year_emissions_summary_table_1850_2023__: yearly emissions data for all countries from 1850 to 2023, including when countries were independent and/or controlled
- __plot_carbon_budget__: numbers used to plot the carbon budget remaining in the animation in the article
- __plot_consumption__: numbers used to plot ranking of countries by colonial+consumption emissions in the article
- __plot_cumulative_per_capita__: numbers used plot the cumulative per yearly capita ranking in the article
- __plot_landvfossil__: numbers used to plot the fossil vs land emissions from 1850 to 2023 in the article
- __plot_NL__: numbers used to plot breakdown of Netherlands' territorial and colonial emissions in the article
- __plot_per_current_pop__:  numbers used plot the emissions per 2023 population ranking in the article
- __plot_ranking_chart__: numbers used to plot the change in rankings from territorial emissions to colonial emissions in the article
- __plot_top20_EU-UK__: numbers used to plot ranking of countries + EU-UK by colonial emissions in the article
- __plot_UK__: numbers used to plot breakdown of UK' territorial and colonial emissions in the article
- __territorial_rule_database_1850_2023__: yearly territorial rule data from 1850 to 2023, showing who was in control of each territory and therefore how emissions were allocated for each year (row sum =1)

Any questions, please contact Verner at verner.viisainen@carbonbrief.org.
