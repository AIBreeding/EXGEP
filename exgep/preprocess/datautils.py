import pandas as pd

def read_and_prepare_data(genotype_path, pheno_path, soil_path, weather_path):
    genotype_df = pd.read_csv(genotype_path)
    pheno_df = pd.read_csv(pheno_path)
    soil_df = pd.read_csv(soil_path)
    weather_df = pd.read_csv(weather_path)
    
    pheno_df['DP'] = pd.to_datetime(pheno_df['DP'])
    pheno_df['DH'] = pd.to_datetime(pheno_df['DH'])
    weather_df['Date'] = pd.to_datetime(weather_df['Date'])
    
    return genotype_df, pheno_df, soil_df, weather_df

def process_weather_data(weather_df, pheno_df):
    results = []
    for env in pheno_df['Env'].unique():
        env_data = pheno_df[pheno_df['Env'] == env].iloc[0]
        start_date = env_data["DP"]
        end_date = env_data["DH"]
        data_subset = weather_df[(weather_df["Env"] == env) & 
                                 (weather_df["Date"] >= start_date) & 
                                 (weather_df["Date"] <= end_date)]
        if 'Date' in data_subset.columns:
            data_subset = data_subset.drop(columns=['Date'])
        result = data_subset.mean(numeric_only=True).to_frame().T
        result.insert(0, 'Env', env)
        results.append(result)
    
    weather_means_df = pd.concat(results, ignore_index=True)
    columns = ['Env'] + [col for col in weather_means_df.columns if col != 'Env']
    weather_means_df = weather_means_df[columns]
    return weather_means_df

def merge_data(genotype_path, pheno_path, soil_path, weather_path):
    genotype_df, pheno_df, soil_df, weather_df = read_and_prepare_data(genotype_path, pheno_path, soil_path, weather_path)
    weather_means_df = process_weather_data(weather_df, pheno_df)
    
    weather_soil_merged = pd.merge(weather_means_df, soil_df, on='Env', how='outer')
    weather_soil_merged = weather_soil_merged[['Env'] + [col for col in weather_soil_merged.columns if col != 'Env']]
    
    weather_soil_pheno_merged = pd.merge(pheno_df, weather_soil_merged, on='Env', how='outer')
    weather_soil_pheno_merged = weather_soil_pheno_merged[['Hybrid', 'Env'] + 
                                                           [col for col in weather_soil_pheno_merged.columns if col not in ['Hybrid', 'Env']]]

    final_merged_df = pd.merge(weather_soil_pheno_merged, genotype_df, on='Hybrid', how='outer')
    final_merged_df = final_merged_df[['Hybrid', 'Env'] + 
                                       [col for col in final_merged_df.columns if col not in ['Hybrid', 'Env']]]
    final_merged_df = final_merged_df.drop(columns=['DP', 'DH'])
    final_merged_df = final_merged_df.sort_values(by=['Hybrid', 'Env'])
    final_merged_df = final_merged_df.dropna()
    
    return final_merged_df