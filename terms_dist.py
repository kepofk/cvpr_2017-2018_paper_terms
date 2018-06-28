#!/usr/bin/env python3.5
#-*- coding:utf-8 -*- 

import pandas as pd
import re

def loadTitles(input_path):
	titles = []
	with open(input_path, 'r') as input: 
		for line in input:
			if line.startswith("title"):
				title = line.replace("title = {", "").replace("},<br>","").strip()
				titles.append(title.lower())
	return titles	

def getTermCountsSeries(titles,sr_name):
	terms = []
	for title in titles:
		for term in title.split(' '):
			#remove non letters and numbers
			term = re.sub(r"[^a-zA-Z0-9]", "", term) 
			terms.append(term)
	return pd.Series(terms, name=sr_name).value_counts()

def printDfSortBy(df, sort_key, print_num):
	print("\n====================================================")
	print("sort by '%s'" % sort_key)
	print(df.sort_values(by=sort_key, ascending=False)[:print_num])

if __name__ == "__main__":
	last_year_path = "./dump/CVPR2017.py"
	this_year_path = "./dump/CVPR2018.py"
	output_path = "./output/cvpr_title_terms_dist_2017_2018.txt"

	last_year_titles = loadTitles(last_year_path)
	this_year_titles = loadTitles(this_year_path)
	
	print("\n====================================================")
	print("cvpr_2017_titles : %d, cvpr_2018_titles : %d" % (len(last_year_titles), len(this_year_titles)))

	last_year_terms_counts_sr = getTermCountsSeries(last_year_titles, "2017")
	this_year_terms_counts_sr = getTermCountsSeries(this_year_titles, "2018")

	df = pd.concat([last_year_terms_counts_sr, this_year_terms_counts_sr], axis=1).fillna(0)
	df["diff"] = df["2018"] - df["2017"]
	df["sum"] = df["2017"] + df["2018"]
	df["2017_norm"] = df["2017"] / df["2017"].sum()
	df["2018_norm"] = df["2018"] / df["2018"].sum()
	df["norm_diff"] = df["2018_norm"] - df["2017_norm"]

	printDfSortBy(df, "sum", 20)
	printDfSortBy(df, "diff", 20)
	printDfSortBy(df, "norm_diff", 20)
	
	print("\noutput_path : %s" % output_path)
	df = df.sort_values(by="diff", ascending=False)
	df.to_csv(output_path, sep="\t", float_format="%.3f")

