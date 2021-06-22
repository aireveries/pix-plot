# PixPlot

This repository contains code that can be used to visualize tens of thousands of images in a two-dimensional projection within which similar images are clustered together. 

This is a fork based off the Yale DHLab's [repo found here](https://github.com/YaleDHLab/pix-plot). Please refer to it for additional documentation of functionality we do not use.

**NOTE**: To see more in depth setup documentation using our particular pipeline, please see the `Machine Learning Core | Platforms and Tools | Pixplot` page in Confluence.


## Dependencies

To install the Python dependencies, we recommend you [install Anaconda](https://www.anaconda.com/products/individual#Downloads) and then create a conda environment with a Python 3.7 runtime:

```bash
conda create --name=3.7 python=3.7
source activate 3.7
```

Then you can install the dependencies by running:

```bash
pip uninstall pixplot
pip install https://github.com/yaledhlab/pix-plot/archive/master.zip
```

Please note that you will need to use Python 3.6 or Python 3.7 to install and use this package. The HTML viewer also requires a WebGL-enabled browser.

## Quickstart

If you have a WebGL-enabled browser and a directory full of images to process, you can prepare the data for the viewer by installing the dependencies above then running:

```bash
pixplot --images "path/to/images/*.jpg"
```

To see the results of this process, you can start a web server by running:

```bash
# for python 3.x
python -m http.server 5000

# for python 2.x
python -m SimpleHTTPServer 5000
```

The visualization will then be available at `http://localhost:5000/output`.


## Controlling UMAP Layout

The [UMAP algorithm](https://github.com/lmcinnes/umap) is particularly sensitive to three hyperparemeters:

```
--min_distance: determines the minimum distance between points in the embedding
--n_neighbors: determines the tradeoff between local and global clusters
--metric: determines the distance metric to use when positioning points
```

UMAP's creator, Leland McInnes, has written up a [helpful overview of these hyperparameters](https://umap-learn.readthedocs.io/en/latest/parameters.html). To specify the value for one or more of these hyperparameters when building a plot, one may use the flags above, e.g.:

```bash
pixplot --images "path/to/images/*.jpg" --n_neighbors 2
```

## Curating Automatic Hotspots

PixPlot uses [Hierarchical density-based spatial clustering of applications with noise](https://hdbscan.readthedocs.io/en/latest/index.html), a refinement of the earlier [DBSCAN](https://en.wikipedia.org/wiki/DBSCAN) algorithm, to find hotspots in the visualization. You may be interested in consulting this [explanation of how HDBSCAN works](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html).

## Adding Metadata

If you have metadata associated with each of your images, you can pass in that metadata when running the data processing script. Doing so will allow the PixPlot viewer to display the metadata associated with an image when a user clicks on that image.

To specify the metadata for your image collection, you can add ` --metadata=path/to/metadata.csv` to the command you use to call the processing script. For example, you might specify:

```bash
pixplot --images "path/to/images/*.jpg" --metadata "path/to/metadata.csv"
```

Metadata should be in a comma-separated value file, should contain one row for each input image, and should contain headers specifying the column order. Here is a sample metadata file:

| filename | category  | tags  | description   | permalink   | Year     |
| -------- | --------- | ----- | ------------- | ----------- | -------- |
| bees.jpg | yellow    | a\|b\|c | bees' knees   | https://... | 1776     |
| cats.jpg | dangerous | b\|c\|d | cats' pajamas | https://... | 1972     |

The following column labels are accepted:

| *Column*         | *Description*                                           |
| ---------------- | ------------------------------------------------------- |
| **filename**     | the filename of the image                               |
| **category**     | a categorical label for the image                       |
| **tags**         | a pipe-delimited list of categorical tags for the image |
| **description**  | a plaintext description of the image's contents         |
| **permalink**    | a link to the image hosted on another domain            |
| **year**         | a year timestamp for the image (should be an integer)   |
| **label**        | a categorical label used for supervised UMAP projection |

## Acknowledgements

The DHLab would like to thank [Cyril Diagne](http://cyrildiagne.com/) and [Nicolas Barradeau](http://barradeau.com), lead developers of the spectacular [Google Arts Experiments TSNE viewer](https://artsexperiments.withgoogle.com/tsnemap/), for generously sharing ideas on optimization techniques used in this viewer, and [Lillianna Marie](https://github.com/lilliannamarie) for naming this viewer PixPlot.
