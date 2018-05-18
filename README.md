# Evidence and Bayesian Occam's Razor

Reproducing the example of the implicit Occam's razor effect of Bayesian model
comparison that is used in Murray I., Ghahramani Z. (2005) A note on the
evidence and Bayesian Occam’s razor, GCNU-TR 2005-003.

The report is included in the repo as `GCNU-TR_2005-003.pdf` for reference or
can be found online at
[www.gatsby.ucl.ac.uk](http://www.gatsby.ucl.ac.uk/publications/tr/tr05-003.pdf).

## Description

Please find the python code in `code.py`

These graphs and data sets show that by comparing the evidence of Bayesian models
the simplest model is preffered as in Occam's razor. We create an example
dataset of all the possibly labellings of a 3x3 grid, either o or x.

We then formulate four simple models: H&#8320; assigns constant probability,
H&#8321; is linear regression with a parameter for one dimension, H&#8322; a
linear regression with parameters for both dimensions and H&#8323; the same as
H&#8322; with the addition of an bias parameter. You should see that as a model
increases in complexity it places more probability among a greater number of
datasets and is therefore less sure while the simpler models despite describing
fewer models assign more of their weight to the data they can describe well.

The datasets for which the evidence is maximal are also displayed below and these
are coherent with our models.  H&#8320; has equal evidence for all the datasets
so is ignored, but H&#8321; and H&#8322; are clearly linearly boundaries in one
and two dimensions while the bias parameter of H&#8323; allows it to push the
boundary off of the dataset.

The datasets for the graphs are ordered as in the Appendix of the paper.

## Results

![All data sets](graphs/all_data_sets.png)

![Subset data sets](graphs/subset_data_sets.png)

Dataset that maximises P(D|H&#8321;)
```
x x x 
o o o 
o o o 
```

Dataset that maximises P(D|H&#8322;)
```
x o o 
x o o 
x x o 
```

Dataset that maximises P(D|H&#8323;)
```
x x x 
x x x 
x x x 
```

### Prerequisites

This code relies upon the python packages
* numpy
* matplotlib
* itertools
* scipy

### Running

Can run to produce either the graphs above as output or the grid of inputs as
TikZ code for formatting in LaTeX

For `matplotlib.pyplot` graphs:

```
./code.py graph
```

For the maximal evidence datasets:

```
./code.py draw
```
