#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"

# import libraries
import matplotlib.pyplot as plt
import pandas as pd

# Driver program
if __name__ == '__main__':
    
    dataset = pd.read_csv("results/similarity_analysis_v1.csv", sep="\t")
    
    plt.clf() # Clear figure
    myFig = plt.figure(figsize=[12,10])
    width = 0.35
    #plt.plot(dataset[time], linestyle = 'dotted', marker = 'o', lw = 2, alpha=0.8, color = 'black')
    plt.bar(dataset["year"], dataset["jaccard_func_median"], width, hatch = ".", lw = 1.5, alpha=0.6, color = 'black')
    plt.bar(dataset["year"] + width, dataset["jaccard_library_median"], width, hatch = "x", lw = 1.5, alpha=0.65, color = 'black')
    plt.xticks(dataset["year"] + width / 2, dataset["year"], fontsize=16)
    plt.title("Similarity Analysis of Ransomware using Jaccard Index", fontsize=20, weight='bold')
    plt.ylabel("Similarity Index", fontsize=18, weight='bold')
    plt.xlabel("Ransomware Samples' Collection Year", fontsize=18, weight='bold')
    plt.legend(["Functions", "Libraries"], handleheight = 2.5, loc="best", fontsize='medium')
    plt.yticks(fontsize=16)
    plt.show()
    
    # Saving the figure
    myFig.savefig('graphs_generator/jaccard_index_v1.eps', format='eps', dpi=1200)
    myFig.savefig('graphs_generator/jaccard_index_v1.png', format='png', dpi=300)
    
    plt.clf() # Clear figure
    myFig = plt.figure(figsize=[12,10])
    width = 0.35
    #plt.plot(dataset[time], linestyle = 'dotted', marker = 'o', lw = 2, alpha=0.8, color = 'black')
    plt.bar(dataset["year"], dataset["cosine_func_median"], width, hatch = ".", lw = 1.5, alpha=0.6, color = 'black')
    plt.bar(dataset["year"] + width, dataset["consine_library_median"], width, hatch = "x", lw = 1.5, alpha=0.65, color = 'black')
    plt.xticks(dataset["year"] + width / 2, dataset["year"], fontsize=16)
    plt.title("Similarity Analysis of Ransomware using Cosine Index", fontsize=20, weight='bold')
    plt.ylabel("Similarity Index", fontsize=18, weight='bold')
    plt.xlabel("Ransomware Samples' Collection Year", fontsize=18, weight='bold')
    plt.legend(["Functions", "Libraries"], handleheight = 2.5, loc="best", fontsize='medium')
    plt.yticks(fontsize=16)
    plt.show()
    
    # Saving the figure
    myFig.savefig('graphs_generator/cosine_index_v1.eps', format='eps', dpi=1200)
    myFig.savefig('graphs_generator/cosine_index_v1.png', format='png', dpi=300)