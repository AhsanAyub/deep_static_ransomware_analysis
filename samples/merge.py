import pandas as pd
import glob

# Driver program
if __name__ == '__main__':

	csv_files = [i for i in glob.glob('*.csv')]
	csv_files = sorted(csv_files)

	dfs = []

	for csv_file in csv_files:
		data = pd.read_csv(csv_file, sep="\t")
		dfs.append(data)
		del data

	data = pd.concat(dfs)
	print(data)
	data.to_pickle("2021_sample_info.pkl", protocol=3)
	data.to_csv("2021_sample_info.csv", sep="\t", index=False)