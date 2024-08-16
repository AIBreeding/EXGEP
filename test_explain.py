from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.cm as cm
import networkx as nx
import xgboost as xgb
import numpy as np
import pandas as pd
import shap
import matplotlib
import matplotlib.pyplot as plt
from exgep.preprocess import datautils
from matplotlib.backends.backend_pdf import PdfPages
import argparse
import os
import json


def parse_args():
    parser = argparse.ArgumentParser(
        description='Explain the model')
    parser.add_argument('--Geno', type=str,
                        default='./data/genotype.csv', help='Path to genotype CSV file')
    parser.add_argument('--Phen', type=str,
                        default='./data/pheno.csv', help='Path to phenotype CSV file')
    parser.add_argument('--Soil', type=str,
                        default='./data/soil.csv', help='Path to soil CSV file')
    parser.add_argument('--Weather', type=str,
                        default='./data/weather.csv', help='Path to weather CSV file')
    parser.add_argument('--SSP', type=int, default=2,
                        help='Personalize interpretation of specific samples')
    parser.add_argument('--IEF1', type=str, default='pc2',
                        help='Interaction effect feature 1')
    parser.add_argument('--IEF2', type=str, default='RH2M',
                        help='Interaction effect feature 2')
    parser.add_argument('--job_id', type=str, default='20240813103950', help='Job ID generated during training'

                        )

    return parser.parse_args()


# geno_path = './data/genotype.csv'
# phen_path = './data/pheno.csv'
# soil_path = './data/soil.csv'
# weather_path = './data/weather.csv'
# Sample_sequential_position = 2 
# Interaction_effect_feature1 = 'pc2' 
# Interaction_effect_feature2 = 'RH2M'  

def main():

    args = parse_args()
    geno_path = args.Geno
    phen_path = args.Phen
    soil_path = args.Soil
    weather_path = args.Weather
    Sample_sequential_position = args.SSP  
    Interaction_effect_feature1 = args.IEF1 
    Interaction_effect_feature2 = args.IEF2
    jobnum = args.job_id 
    folder_name = f"{jobnum}/explainable"
    os.makedirs(folder_name, exist_ok=True)

    data = datautils.merge_data(geno_path, phen_path, soil_path, weather_path)
    X_train = data.iloc[:, 3:]
    y_train = data['Yield'].values 

    with open(f"{jobnum}/result/best_params.json", 'r') as json_file:
        paramdata = json.load(json_file)

   
    param = paramdata.get('xgboost', {})  
    param['booster'] = 'gbtree'

    dmat = xgb.DMatrix(X_train, y_train)
    bst = xgb.train(param, dmat)
    bst.set_param({"predictor": "gpu_predictor"})

    shap_values = bst.predict(dmat, pred_contribs=True)

    display_name = X_train.columns
    display_name = pd.DataFrame(
        {'feature_name': display_name, 'display_name': display_name})
    shap_values = shap_values
    fore_data = X_train
    label = data.iloc[:, 1:4]
    label = pd.DataFrame(label)

    col_dict = display_name
    display_col = []
    for col in fore_data.columns:
        if col in col_dict:
            display_col.append(col_dict[col])
        else:
            display_col.append(col)

    fontsize = 18
    plt.figure(figsize=(8, 4))
    # colors = ["#cfe5e2", "#70b2a9"]
    colors = ["#b5bcde", "#6f7dc0"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)

    # summary_plot
    shap.summary_plot(shap_values[:, :-1], fore_data, max_display=20,
                      show=False, plot_size=(10, 6))  # ,cmap=cmap
    plt.xticks(fontsize=fontsize-3)
    plt.yticks(fontsize=fontsize-3)
    plt.xlabel('SHAP value (impact on model output)', fontsize=fontsize)
    plt.savefig(os.path.join(folder_name, 'summary_of_important_feature.pdf'),
                format='pdf', bbox_inches='tight')

    columnName = np.transpose(display_col)
    shapvalue = pd.DataFrame(shap_values[:, :-1], columns=columnName)
    df = pd.concat([label, shapvalue], axis=1)
    df.to_csv(os.path.join(folder_name, "shap_values.csv"), index=False)

    fontsize = 18
    plt.figure(figsize=(8, 4))
    colors = ["#bebada", "#bc80bd"]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    # feature_plot
    shap.summary_plot(shap_values[:, :-1], X_train, max_display=20,
                      show=False, plot_size=(7, 6), cmap=cmap, plot_type="bar")
    plt.xticks(fontsize=fontsize-3)
    plt.yticks(fontsize=fontsize-3)
    plt.xlabel('SHAP value (impact on model output)', fontsize=fontsize)
    plt.savefig(os.path.join(folder_name, 'feature_importance.pdf'),
                format='pdf', bbox_inches='tight')

    feature_importances = pd.DataFrame(list(zip(X_train.columns, np.abs(
        shap_values).mean(0)[:-1])), columns=['Feature', 'Importance'])
    feature_importances.to_csv(os.path.join(
        folder_name, 'feature_importances.csv'), index=False)

    # Individualized_explanation
    explainer = shap.TreeExplainer(bst, X_train)
    GBM_shaps = explainer(X_train)

    fontsize = 18
    plt.figure(figsize=(8, 4))
    shap.plots.waterfall(GBM_shaps[Sample_sequential_position], show=False)
    plt.xticks(fontsize=fontsize-3)
    plt.yticks(fontsize=fontsize-3)
    plt.xlabel('SHAP value (impact on model output)', fontsize=fontsize)
    plt.savefig(os.path.join(folder_name, 'Individualized_explanation.pdf'),
                format='pdf', bbox_inches='tight')
    # plt.show()

    shap_interactions = bst.predict(dmat, pred_interactions=True)

    features = X_train.columns

    interaction_list = []

    for i in range(len(features)):
        for j in range(len(features)):
            interaction_value = np.abs(shap_interactions[:, i, j]).mean()
            interaction_list.append(
                [features[i], features[j], interaction_value])

    interaction_df = pd.DataFrame(interaction_list, columns=[
        'Feature_1', 'Feature_2', 'Interaction_Value'])

    interaction_df.to_csv(os.path.join(
        folder_name, 'feature_interactions.csv'), index=False)

    feature_importances_path = os.path.join(
        folder_name, './feature_importances.csv')
    feature_interactions_path = os.path.join(
        folder_name, './feature_interactions.csv')

    feature_importances_df = pd.read_csv(feature_importances_path)
    feature_interactions_df = pd.read_csv(feature_interactions_path)

    # top 20 fetures
    top_n = 20
    sorted_feature_importances_df = feature_importances_df.sort_values(
        by='Importance', ascending=False).head(top_n)

    sorted_features = sorted_feature_importances_df['Feature']

    interaction_matrix = feature_interactions_df.pivot(
        index='Feature_1', columns='Feature_2', values='Interaction_Value')

    interaction_matrix_sorted = interaction_matrix.loc[sorted_features,
                                                       sorted_features]

    G = nx.Graph()

    for feature, importance in zip(sorted_feature_importances_df['Feature'], sorted_feature_importances_df['Importance']):
        G.add_node(feature, size=importance * 1500,
                   color=importance)  

    for i, feature_1 in enumerate(sorted_features):
        for j, feature_2 in enumerate(sorted_features):
            if i < j: 
                interaction_value = interaction_matrix_sorted.loc[feature_1, feature_2]
                if interaction_value > 0:  
                    G.add_edge(feature_1, feature_2, weight=interaction_value)

    sizes = [G.nodes[node]['size'] for node in G.nodes]
    colors = [G.nodes[node]['color'] for node in G.nodes]

    weights = [G[u][v]['weight'] * 50 for u, v in G.edges] 
    edges = G.edges(data=True)
    edge_colors = [edge[2]['weight'] for edge in edges]

    node_cmap = LinearSegmentedColormap.from_list(
        "node_cmap", ["#fdb782", "#a63603"])
    edge_cmap = LinearSegmentedColormap.from_list(
        "edge_cmap", ["#8e8f93", "#626262"])

    fig, ax = plt.subplots(figsize=(8, 8))
    pos = nx.spring_layout(G, k=0.7) 

    nodes = nx.draw_networkx_nodes(
        G, pos, node_size=sizes, node_color=colors, cmap=node_cmap, alpha=0.8, ax=ax)

    edges = nx.draw_networkx_edges(
        G, pos, width=weights, edge_color=edge_colors, edge_cmap=edge_cmap, alpha=0.6, ax=ax)

    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

    sm = plt.cm.ScalarMappable(cmap=node_cmap, norm=plt.Normalize(
        vmin=min(colors), vmax=max(colors)))
    sm._A = []
    cbar_nodes = fig.colorbar(sm, ax=ax, label='Feature Importance',
                              orientation='vertical', fraction=0.02, pad=0.04, shrink=0.1)
    cbar_nodes.ax.set_position([0.9, 0.6, 0.02, 0.3]) 

    sm_edges = plt.cm.ScalarMappable(cmap=edge_cmap, norm=plt.Normalize(
        vmin=min(edge_colors), vmax=max(edge_colors)))
    sm_edges._A = []
    cbar_edges = fig.colorbar(sm_edges, ax=ax, label='Interaction Value',
                              orientation='vertical', fraction=0.02, pad=0.04, shrink=0.1)
    cbar_edges.ax.set_position([0.9, 0.1, 0.02, 0.3]) 

    plt.gca().set_axis_off()  
    plt.savefig(os.path.join(folder_name, './interaction_network.pdf'),
                format='pdf', bbox_inches='tight')
    # plt.show()
    
    shap.dependence_plot(Interaction_effect_feature1,
                         shap_values[:, :-1], X_train, interaction_index=Interaction_effect_feature2, show=False)
    plt.savefig(os.path.join(folder_name, f'{Interaction_effect_feature1}_{Interaction_effect_feature2}_interaction.pdf'),
                format='pdf', bbox_inches='tight')

    shap.dependence_plot(Interaction_effect_feature1,
                         shap_values[:, :-1], X_train, interaction_index=None, show=False)
    plt.savefig(os.path.join(folder_name, f'{Interaction_effect_feature1}.pdf'),
                format='pdf', bbox_inches='tight')

    display_name = X_train.columns
    # display_name = pd.DataFrame({ 'feature_name': display_name, 'display_name': display_name})
    shap.dependence_plot((Interaction_effect_feature1, Interaction_effect_feature2),
                         shap_interactions[:, :-1, :-1], X_train, feature_names=display_name, show=False)
    plt.savefig(os.path.join(folder_name, f"{Interaction_effect_feature2}_{Interaction_effect_feature1}_interaction.pdf"),
                format='pdf', bbox_inches='tight')
    # plt.show()


if __name__ == '__main__':
    main()
