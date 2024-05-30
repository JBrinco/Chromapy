<h1 align="center">
  <img src="Examples_Templates/Images/Chromapy.png" alt="Chromapy">
</h1>

Python Scripts for Chromatographic Data Processing

Although uninventive, the name of the project is unlikely to cause any confusion as to its purpose.

# Newcomers, read this!

Thank you for your interest. This package can help you in the treatment of chromatographic data and the like. It does NOT read or manipulate chromatograms directly (the program that came with your instrument can do it better anyways, and there is always OpenChrom). You must integrate your chromatograms, and add that data (in the form of .csv or .xlsx) to this program.

If you are familiar with the Python programming language, the module will be very easy to use, and you can change it to your liking, just as long as you abide by the GNU General Public License v3.

If you are not familiar with any of this, and are wondering what the heck is this website GitHub and why do I care, then you can also benefit from this package. There are several scripts that can help you (for the command line).

This manual is written for semi-advanced users, who can script in python, and also for basic users. All the documentation is in this page. Specific tinkering will require you to look into the code... and change it! It not a bomb, you know?


# Table of Contents
1. [Overview of Functionality](#overview)
2. wef
3. [Example2](#example2)
4. [Third Example](#third-example)
5. [Fourth Example](#fourth-examplehttpwwwfourthexamplecom)

# Overview of Functionality <a name="overview"></a>

### There are two sides of this package: A module and a collection of scripts.

The module is useful for those familiar with the python programming language, as it can be used in the creation of custom scripts and routines.

The Scripts are intended for easy command line use, withought requiring any specialized computer knowledge.

In the future I might add a Graphical User Interface for those terribly intimidated by the command line. But for now, all functionality can be accesed this way.

## Functionality

### Design of Experiments (DOE)

Built on top of other DOE packages, provides both matrix design as well as data analysis and response surfaces. Supports Placket-Burman and two-level full factorial designs for screening. Also provides Box-Behnken designs for fitting a response surface.

#### Instructions

The input is very simple. For two level designs (Plackett-burman and full factorial), simply do:


| Variable1       | Variable2       | Variable3       | Variable4       | ... |
| ---             | ---             | ---             | ---             | --- |
| Var1 low value  | Var2 low value  | Var3 low value  | Var4 low value  | ... |
| Var1 high value | Var2 high value | Var3 high value | Var4 high value | ... |



You can name the variables whatever you want (try avoiding special symbols, like $#|\, etc. The values need not be numbers, they can be for example: Yes/No, Glass/Plastic, MgSO4/Na2SO4 or something like that. You also don't need to put the low value on top and the high value on the bottom. Check the sample file to get an idea.

For Box-Behnken designs, the input file changes slightly:



| Variable1            | Variable2            | Variable3            | Variable4            | ... |
| ---                  | ---                  | ---                  | ---                  | --- |
| Var1 center value    | Var2 center value    | Var3 center value    | Var4 center value    | ... |
| Var1 deviation value | Var2 deviation value | Var3 deviation value | Var4 deviation value | ... |



So if you put:



| Temperature   |
| --- |
| 250           |
| 50            |



The values for temperature will be 200, 250 and 300 (know thy units).

For calculating the main effect you have to input the .csv with the MATRIX (-1 and 1) which you got when you generated the design, and a second .csv with a single column entitled "Results" (capital R):


| Results |
| ---     |
| 3583.3  |
| 3945.1  |
| 2010.4  |
| 9231.8  |
| ...     |



These results must be in the same order as the experiments in the matrix.


### Quantification Buddy

Automatic quantification from signal values (does not perform integration). Provides also Recovery calculation and expanded measurement uncertainty (the full uncertainty calculated from all measurments and steps).


### ChromaCalc

Traditional chromatographic calculations for when needed: HPLC solvent consumption and GC flow to linear velocity and vice versa.




### Multivariate Analyser

Principal Component Analyis and discriminant partial least squares.

#### Instructions:

Options and explanations are given within each function in the source code. This is a quick exposition of the functionality. You can use the pre-made script for an easier time, especially if you don't understand python.

First, the file should be imported:

```python
import chromapy

df = chromapy.pca_import("Examples/input_data/wine_data.csv")
```

You do NOT need to use .csv files for most functions, but it is advised. Aso supported are: .xls, .xlsx, .xlsm, .xlsb, .odf, .ods, .odt, .csv

The input file should have:


| Sample | Type | Var1 | Var2 | Var3 | ... |
| ------ | ---- | ---- | ---- | ---- | --- |
| water1 | S    | 12.5 | 22.1 | 0.01 | ... |
| water2 | G    | 11.7 | 35.2 | 0.03 | ... |


`Var1`, `Var2`, etc. take any name or number you want, and this will be the name given to the loadings in the biplot. The `Type` is optional, and will separate the samples by color and shape, as well as print a label.

For ease of use and avoidance of errors, please use the sample.csv file provided! You can save it as .xlsx if you wish.

Then, we can normalize if we want:

```python
df_normalized = chromapy.normalize(df, normalization='area')
print(df_normalized)
```

The `normalization` option can be set to:
- "normalize" - Applies the normalize function from scikitlearn, documentation [here](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.normalize.html)
- "standard" - This is the default, if no option is given. Documentation [here](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
- "minmax" - Applies the MinMaxScaler. Documentation [here](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)

- "area" - Will make the sum of all values in a sample equal to 100. Equivalent to using relative percentages of a chromatogram, *ie.* assuming the total area is 100%, and the area of each peak is a certain percentage of that.

Normalizations occur on a sample by sample basis, naturally (not variable by variable).

After normalization, you can calculate the principal components. This function will return 3 objects: `pca_result` has the values for each sample witin the principal component space. `loadings_df` is a nicely formatted dataframe with each loading (variable) and its respective contribution to each principal component, and `loadings` is the actual object created by scikit-learn's computations, which is used internally when graphing.

```python
pca_result, loadings_df, loadings = chromapy.pca(df_normalized)
```

Finally we can graph the plot. This function has many options (check the source code), but this is an easy usage case:

```python
plot = chromapy.pca_plot(pca_result, loadings_df, loadings, output="sample_pca_output.svg", loadings_scale=10)
```

On Biplots (both samples and loadings) you will have to scale up or down the loadings to correctly fit the plot axis. This is done with the `loadings_scale` option, as shown. When the graph is shown on screen, you can save directly, so the `output` option is actually unnecessary.

You can (and should) save the graphs as .svg files, which you can then open in inkscape and edit to your heart's content! Or if you use LaTeX, which does not support .svg directly, you can convert them to .pdf in inkscape.

## Milestones

#### Design of Experiments

- [ ] Plackett burman significance calculation
- [ ] Plackett burman designs are "rotable"

#### Quantification Assistant

- [x] Automatic quantification
- [x] Results with stdev (+-), finds sample replicates and presents result with either stdev or student-t
- [x] Calculation of measurement performance parameters (LOD, Recovery, etc.)
- [x] Script for CLI

#### Multivariate Analyser

- [x] PCA
- [x] PLS
- [ ] ANOVA (one and two way)
- [ ] Cluster Analysis
- [ ] Discriminant Analysis
- [x] Graphing capabilities
- [x] Script for CLI

#### ChromaCalc

- [x] HPLC Solvent consumption
- [ ] Kovats Calculation
- [ ] Experiment Randomizer
- [ ] Analytical eco-scale calculation
