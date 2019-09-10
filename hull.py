# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:10:27 2019

@author: ziyan
"""

import argparse
import os
import shutil
import sys
import time
import warnings
import numpy as np
from scipy.spatial import ConvexHull
import pandas as pd

parser = argparse.ArgumentParser(description='ternary convex hull analysis')
parser.add_argument('--data_file', required=True, help="The file containing compositions and formation energies")
args = parser.parse_args()

points=pd.read_excel(args.data_file)
pts=np.array(points)

def makeTriangle(composition):
    comp = composition/sum(composition)
    return (comp[0] + comp[1]/2, comp[1]*np.sqrt(3)/2)
npts=[]
for pt in pts:
    x,y = makeTriangle(pt[:3])
    npts.append([x,y,pt[3]])
npts=np.array(npts)

hull=ConvexHull(npts)
for p in hull.vertices:
    lable=''
    for i,s in zip(pts[p,:3],['A', 'B', 'C']):
        if i > 0:
            lable += str(s)
            if i >1:
                lable += str(int(i))
    #print(lable, pts[p])
hull_comp=[]
for p in hull.vertices:
    comp=pts[p]
    hull_comp.append(comp)
hull_comp=np.array(hull_comp)
df_hull_comp=pd.DataFrame(hull_comp)
hull_comp_lower_half=df_hull_comp[~(df_hull_comp[[3]] > 0).any(axis=1)]
hull_comp_lower_half=np.array(hull_comp_lower_half)
df_hull_lower=pd.DataFrame(hull_comp_lower_half)
df_hull_lower = df_hull_lower[df_hull_lower[0] != 1]
df_hull_lower = df_hull_lower[df_hull_lower[1] != 1]
df_hull_lower = df_hull_lower[df_hull_lower[2] != 1]
ele=[0,0,1,0,0,1,0,0,1,0,0,0]
df_ele = pd.DataFrame(np.array(ele).reshape(3,4))
df_hull_lower=df_hull_lower.append(df_ele)
hull_comp_lower_half=df_hull_lower.to_numpy()
npts_lower_half=[]
for pt1 in hull_comp_lower_half:
    x1,y1=makeTriangle(pt1[:3])
    npts_lower_half.append([x1,y1,pt1[3]])
npts_lower_half=np.array(npts_lower_half)
lower_half_hull=ConvexHull(npts_lower_half)
all_hull_eqs=lower_half_hull.equations
df_all_hull_eqs=pd.DataFrame(all_hull_eqs)
thermo_hull_eqs=df_all_hull_eqs[~(df_all_hull_eqs[[3]] == 0).any(axis=1)]
eqs=np.array(thermo_hull_eqs)
a=[]
b=[]
c=[]
d=[]
x=[]
y=[]
for i2 in range(len(eqs)):
    a1=eqs[i2][0]
    a.append(a1)
    b1=eqs[i2][1]
    b.append(b1)
    c1=eqs[i2][2]
    c.append(c1)
    d1=eqs[i2][3]
    d.append(d1)
for i1 in range(len(npts)):
    x1=npts[i1][0]
    x.append(x1)
    y1=npts[i1][1]
    y.append(y1)

E_i2=[]
for i1 in range(len(npts)):
    for i2 in range(len(eqs)):
        E1=-(x[i1]*a[i2]+y[i1]*b[i2]+d[i2])/c[i2]
        E_i2.append(E1)
df_E = pd.DataFrame(np.array(E_i2).reshape(len(npts),len(eqs)))       
df_E[df_E>0]= -100    
E_max=df_E.max(axis=1)
Ef=points['Ef']
E_hull=[]
for i in range(len(Ef)):
    Ehull=Ef[i]-E_max[i]
    E_hull.append(Ehull)

E_hull=pd.DataFrame(E_hull)
E_hull.to_excel('energy_above_hull.xlsx', index=False)