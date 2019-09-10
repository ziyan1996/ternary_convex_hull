# Ternary convex hull analysis
Automated ternary convex hull analysis based on the formation energy values of each composition within the ternary space is employed in this script, instructions are provided below. The phase stablity is determined using convex hull analysis, where the energy above hull (E_hull) provide a quantitative measurement of the thermodynamic stability.

## How to use it

First, prepare your data in an excel file (.xlsx format). This excel file should contain 4 colomns like this:

| A | B | C | Ef |
| ---- | ---- | ---- | ---- |
| A fraction | B fraction | C fraction | formation energy |

Here, your ternary system is represented with three component A, B and C, and the first three colomns in your input file is their fractions. The fourth column in your input file is the formation energies of each composition. Please make sure you name the fourth colomn to be "Ef" (easier for me to inded it ^^).

Once you have the input file read, run the following command:

```
python hull.py --data_file "your_file.xlsx"
```

After it's done, a file called "energy_above_hull.xlsx" will be generated, containing the E_hull values of all the compositions in your ternary space, as a measurement of their thermodynamic stability.
