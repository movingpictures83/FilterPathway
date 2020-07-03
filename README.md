# FilterPathway
# Language: Python
# Input: TXT
# Output: TXT
# Tested with: PluMA 1.1, Python 3.6
# Dependencies: CSV2GML Plugin, Pathway Tools Databse

Take a CSV and find all pathways present in PathwayTools (Karp et al, 2015).

The plugin accepts as input a TXT file of keyword-value tab-delimited pairs:
correlationfile: CSV file for network
pathwayfile: TXT file of pathways present in PathwayTools.

The output TXT file contains all pathways from the pathway file that were also discovered in the correlation network.
