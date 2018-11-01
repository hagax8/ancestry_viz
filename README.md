# Ancestry clustering
This tutorial will show you how to do ancestry clustering using GTM (our [ugtm](https://github.com/hagax8/ugtm) implementation) or t-SNE (sklearn implementation).


### Requirements
The following python packages are required:
* ugtm 
* sklearn
* altair
* matplotlib
* numpy
* pandas

### Files in directory
* worldmap_1000G.py: Python script, creates interactive visualization gathering GTM, t-SNE and PCA 
* runGTM.py: runs GTM (using ugtm package) or t-SNE (using sklearn)
* data: directory, contains csv data files 
* data/dataframe_1000G_noadmixed.csv: csv file, 1000 Genomes project dataframe with corresponding t-SNE and GTM coordinates 

## First step: download files
You can download files for ancestry classification using 1000 genomes Phase 3 data from here (http://lovingscience.com/ancestries/), which are already formatted for this software. In this tutorial, we will use the following files:
- recoded_1000G.noadmixed.mat: 20 populations from 1000 Genomes Project (excluding MXL, ACB, ASW, ITU, STU, GIH)
- recoded_1000G.raw.noadmixed.lbls3_3: the corresponding ancestry labels (GBR and CEU were merged to obtain one category for Northern/Western European ancestry)
- recoded_1000G.raw.noadmixed.lbls3: the corresponding ancestry labels (GBR and CEU were not merged)
- recoded_1000G.raw.noadmixed.ids: the corresponding individual IDs

You can find out how these files were created by [clicking here](https://github.com/hagax8/uGTM/wiki/Appendix:-Generate-ancestry-files).

## Second step: visualization:

To build a map with parameters [k,m,l,s] = [16,4,0.1,0.3] and 10 principal components, run the following command:

```
python runGTM.py --model GTM --data recoded_1000G.noadmixed.mat --labels recoded_1000G.raw.noadmixed.lbls3 --labeltype discrete --out outputname --pca --n_components 10 --regularization 0.1 --rbf_width_factor 0.3 --missing --missing_strategy median --random_state 8 --ids recoded_1000G.raw.noadmixed.ids
```

It should be noted that our genotype file has missing values that we are handling with the --missing and --missing strategy options. You should obtain a pdf and an html file. The html file looks like this:
[1000G_GTM_20populations.html](http://www.lovingscience.com/ancestries/downloads/1000G_GTM_20populations.html)

To build a t-SNE map, run: 

```
python runGTM.py --model GTM --data recoded_1000G.noadmixed.mat --labels recoded_1000G.raw.noadmixed.lbls3 --labeltype discrete --out outputname --pca --n_components 10 --missing --missing_strategy median --random_state 8 --ids recoded_1000G.raw.noadmixed.ids
```

Click here to access the t-SNE map: [1000G_t-SNE_20populations.html](http://www.lovingscience.com/ancestries/downloads/1000G_t-SNE_20populations.html)

## Third step: evaluation of classification performances in a crossvalidation experiment, compare GTM and linear SVM:
python runGTM.py --model GTM --data recoded_1000G.noadmixed.mat --labels recoded_1000G.raw.noadmixed.lbls3_3 --labeltype discrete --out outputname --pca --n_components 10 --missing --missing_strategy median --random_state 8 --crossvalidate

This will give you per-class reports. Default class priors are equiprobable (cf. --prior option).


## Fourth step: train on provided data and project a test set onto the map:
```
python runGTM.py --model GTM --data recoded_1000G.noadmixed.mat --test recoded_1000G_MXL.mat --labels recoded_1000G.raw.noadmixed.lbls3_3 --labeltype discrete --out outputname --pca --n_components 10 --missing --missing_strategy median --random_state 8 
```

This will give you:
* predictions for individuals (output_indiv_predictions.csv)
* posterior probabilities for each ancestry (output_indiv_probabilities.csv) 
* posterior probabilities for the whole test set (output_group_probabilities.csv)
* a map with projected test set colored in black.

The projection for MXL population (Mexicans) can be visualized here: [1000G_GTM_projection_MXL.html](http://www.lovingscience.com/ancestries/downloads/1000G_GTM_projection_MXL.html)

## Addendum 1: map based on AFR superpopulation only 
To only run the computation for African samples:
* Download:
- recoded_1000G.noadmixed.AFR.mat: African (AFR) populations from 1000 Genomes Project (excluding ACB, ASW, ITU, STU)
- recoded_1000G.raw.noadmixed.AFR.lbls3: the corresponding ancestry labels
- recoded_1000G.raw.noadmixed.AFR.ids: the corresponding individual IDs 

* Build GTM and t-SNE: 

- GTM (cf. [output](http://www.lovingscience.com/ancestries/downloads/1000G_GTM_20populations.AFR.html))
```
python runGTM.py --model GTM --data recoded_1000G.noadmixed.AFR.mat --labels recoded_1000G.raw.noadmixed.AFR.lbls3 --labeltype discrete --out 1000G_GTM_AFR --pca --n_components 10 --regularization 0.1 --rbf_width_factor 0.3 --missing --missing_strategy median --random_state 8 --ids recoded_1000G.raw.noadmixed.AFR.ids
```
- t-SNE (cf. [output](http://www.lovingscience.com/ancestries/downloads/1000G_t-SNE_20populations.html)):
```
python runGTM.py --model GTM --data recoded_1000G.noadmixed.AFR.mat --labels recoded_1000G.raw.noadmixed.AFR.lbls3 --labeltype discrete --out 1000G_t-SNE_AFR --pca --n_components 10 --missing --missing_strategy median --random_state 8 --ids recoded_1000G.raw.noadmixed.AFR.ids
```

* African subpopulations classification performance:
```
python runGTM.py --model GTM --data recoded_1000G.noadmixed.AFR.mat --labels recoded_1000G.raw.noadmixed.AFR.lbls3 --labeltype discrete --out outputname --pca --n_components 10 --missing --missing_strategy median --random_state 8 --crossvalidate
```

## Addendum 2: Arabidopsis Thaliana geographic visualization
Cf. github repository https://github/hagax8/arabidopsis_viz 




