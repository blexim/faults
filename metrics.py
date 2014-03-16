#!/usr/bi/python
import math
import random

random.seed()

# Below are the 80 suspiciousness measures (which begin on line 56)
# There are 6 types of measures, as follows:
# CAUSAL MEASURES, STATISTICAL MEASURES, CONFIRMATION MEASURES, NEW SIMILARITY MEASURES, OLD MEASURES, CUSTOM MEASURES
# Key:
# cf is the number of test cases that cover c and fail
# cp is the number of test cases that cover c and pass
# nf is the number of test cases that don't cover c and fail
# np is the number of test cases that don't cover c and pass

# constant
c = 0.5
p = 0.0001

#  Probabilistic helper functions. These functions are used later on to ease the verbosity of definitions. 
#  They are NOT to be used as suspiciousness measures themselves

def Prob_C(cf, nf, cp, np):
  return (cf + cp) / (cf + nf + cp + np)

def Prob_E(cf, nf, cp, np):
  return (cf + nf) / (cf + nf + cp + np)

def Prob_not_C(cf, nf, cp, np):
  return (np + nf) / (cf + nf + cp + np)

def Prob_not_E(cf, nf, cp, np):
  return (np + cp) / (cf + nf + cp + np)

def Prob_E_given_C(cf, nf, cp, np):
  return (cf / (cf + cp))

def Prob_E_given_not_C(cf, nf, cp, np):
  if nf + np == 0:
    return 0.0

  return (nf / (nf + np))

def Prob_not_E_given_C(cf, nf, cp, np):
  return (cp / (cf + cp))

def Prob_not_E_given_not_C(cf, nf, cp, np):
  if nf + np == 0:
    return 0.0

  return (np / (nf + np))

def Prob_C_given_E(cf, nf, cp, np):
  return (cf / (cf + nf))

def Prob_not_C_given_E(cf, nf, cp, np):
  return (nf / (cf + nf))

def Prob_C_given_not_E(cf, nf, cp, np):
  return (cp / (cp + np))

def Prob_not_C_given_not_E(cf, nf, cp, np):
  return (np / (cp + np))

def Prob_C_and_E(cf, nf, cp, np):
  return (cf / (cf + nf + cp + np))

def Prob_not_C_and_not_E(cf, nf, cp, np):
  return (np + np) / (cf+nf+cp+np)


# CAUSAL MEASURES (x9)

def Suppes(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (cf / (cf + cp)) - (nf / (nf + np))

def Lewis(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return math.log10(((nf * cf) + (cf * np))/ ((nf * cf) + (nf * cp)))

def Good(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return math.log10(((cp * np) + (np * cf)) / ((cp * np) + (cp * nf)))

def PearlI(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return ((cf / (cf + cp)) - (nf / (nf + np))) / (cf / (cf + cp))

def PearlII(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return ((cf / (cf + cp)) - (nf / (nf + np))) / (np / (nf + np))

def Cheng(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return ((((cf / (cf + cp)) - (nf / (nf + np))))/ (1 - ((nf / (nf + np)))) )

def Korb2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (cf / (cf + cp)) * math.log10(((nf * cf) + (cf * cf) + (cf * cp) + (cf * np)) / ((nf * cf) + (nf * cp) + (cf * cf) + (cf * cp)))

def Korb3(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return ((cf + cp) / (cf + cp + nf + np)) * ((cf/(cf + cp)) * math.log10(((nf*cf) + (cf*cf) + (cf*cp) + (cf*np)) / ((nf*cf) + (nf*cp) + (cf*cf) + (cf*cp))))

def Landsberg(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  if np == nf:
    np += c

  return (np/(np-nf)) - (cp/(cp+cf))





# STATISTICAL MEASURES (x15)

def PPV(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (cf / (cf + cp))

def NPV(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (np / (nf + np))

def Sensitivity(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (cf / (cf + nf))

def Specificity(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (np / (cp + np))

def YoudensJ(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (cf / (cf + nf)) + (np / (cp + np)) - 1

def PosLikelyhood(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (cf / (cf + nf)) / (1 - (np / (cp + np)))

def YulesQ(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (((cf*np)-(cp*nf)) / ((cf*np)+(cp*nf))) 

def YulesY(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return ((math.sqrt(cf*np)-math.sqrt(cp*nf)) / (math.sqrt(cf*np)+math.sqrt(cp*nf)))

def GilbertWells(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  t = cf + nf + cp + np
  return math.log10(cf) - math.log10(t) - math.log10((cf + cp)/t) - math.log10((cf + nf)/t)

def Pearson1(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  bottom = (cf +cp )*(cf +nf )*(cp +np )*(nf +np )
  t = cf +nf +cp +np 
  chi_sq = (t*((cf *np )-(cp *nf )))/bottom
  return chi_sq 
 
def Pearson3(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  rho = ((cf *np ) - (nf *cp )) / math.sqrt((cf +cp )*(cf +nf )*(cp +np )*(nf +np ))
  t = cf + nf + cp + np 
  return rho

def PearsonHeron2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  pi = 3.1415926
  top = pi*math.sqrt(cp *nf )
  l_bot = math.sqrt(cf *np )
  r_bot = math.sqrt(cp *nf )
  return math.cos(top/(l_bot+r_bot))


def GoodKruskal(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  
  a1 = 0
  a2 = 0
  a3 = 0
  a4 = 0
  b1 = 0
  b2 = 0

  if cf > cp:
    a1 = cf
  else:
    a1 = cp

  if nf > np:
    a2 = nf
  else:
    a2 = np

  if cf > nf:
    a3 = cf
  else:
    a3 = nf

  if cp > np:
    a3 = cp
  else:
    a3 = np

  rho = a1+a2+a3+a4
  rho2 = 0

  if cf+nf > cp+np:
    b1 = cf+nf
  else:
    b2 = cp+np

  if cf+cp > nf+np:
    b1 = cf+cp
  else:
    b2 = nf+np

  rho2 = b1 + b2

  t = cf + nf + cp + np

  return (rho - rho2) / ((2 * t) - rho2)

def Anderberg(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  
  a1 = 0
  a2 = 0
  a3 = 0
  a4 = 0
  b1 = 0
  b2 = 0

  if cf > cp:
    a1 = cf
  else:
    a1 = cp

  if nf > np:
    a2 = nf
  else:
    a2 = np

  if cf > nf:
    a3 = cf
  else:
    a3 = nf

  if cp > np:
    a3 = cp
  else:
    a3 = np

  rho = a1+a2+a3+a4
  rho2 = 0

  if cf+nf > cp+np:
    b1 = cf+nf
  else:
    b2 = cp+np

  if cf+cp > nf+np:
    b1 = cf+cp
  else:
    b2 = nf+np

  rho2 = b1 + b2

  t = cf + nf + cp + np

  return (rho - rho2) / (2 * t)

def Peirce(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return ((cf *np ) + (cp *nf )) / ((cf *cp ) + (2*cp *nf ) + (nf *np ))



# CONFIRMATION MEASURES (x14)

def Earman(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return Prob_C_given_E(cf, nf, cp, np) - Prob_C(cf, nf, cp, np)

def Keynes(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return math.log10(Prob_C_given_E(cf, nf, cp, np) / Prob_C(cf, nf, cp, np))

def Good2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return math.log10(Prob_C_given_E(cf, nf, cp, np) / Prob_C_given_not_E(cf, nf, cp, np))

def Carnap1(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return Prob_C_and_E(cf, nf, cp, np) - (Prob_C(cf, nf, cp, np)* Prob_E(cf, nf, cp, np))

def Carnap2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return Prob_C(cf, nf, cp, np) * ((Prob_E_given_C(cf, nf, cp, np) - Prob_E(cf, nf, cp, np)) / Prob_E(cf, nf, cp, np))

def Crupi(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  buff = 0

  if Prob_C_given_E(cf, nf, cp, np) < Prob_C(cf, nf, cp, np):
    buff = (Prob_C_given_E(cf, nf, cp, np) - Prob_C(cf, nf, cp, np)) / Prob_C(cf, nf, cp, np)
  else: 
    buff = (Prob_C_given_E(cf, nf, cp, np) - Prob_C(cf, nf, cp, np)) / Prob_not_C(cf, nf, cp, np)
  return buff

def Rescher(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (Prob_E_given_C(cf, nf, cp, np) - Prob_E(cf, nf, cp, np)) * (Prob_C(cf, nf, cp, np)/Prob_not_C(cf, nf, cp, np))

def Kemeny(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (Prob_E_given_C(cf, nf, cp, np) - Prob_E_given_not_C(cf, nf, cp, np)) / (Prob_E_given_C(cf, nf, cp, np) + Prob_E_given_not_C(cf, nf, cp, np))

def Popper1(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return ((Prob_E_given_C(cf, nf, cp, np) - Prob_E(cf, nf, cp, np)) / (Prob_E_given_C(cf, nf, cp, np) + Prob_E(cf, nf, cp, np))) * Prob_C(cf, nf, cp, np) * Prob_E_given_C(cf, nf, cp, np)

def Popper2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (Prob_E_given_C(cf, nf, cp, np) - Prob_E(cf, nf, cp, np)) / ((Prob_E_given_C(cf, nf, cp, np) + Prob_E(cf, nf, cp, np)) * Prob_not_C(cf, nf, cp, np))

def Levi(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (((Prob_E_given_C(cf, nf, cp, np) - Prob_E_given_not_C(cf, nf, cp, np)) / Prob_E(cf, nf, cp, np))) * Prob_C(cf, nf, cp, np) * Prob_not_C(cf, nf, cp, np)

def Finch1(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (((Prob_C_given_E(cf, nf, cp, np) - Prob_C(cf, nf, cp, np)) / Prob_C(cf, nf, cp, np)))

def Gaifman(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return Prob_not_C(cf, nf, cp, np) / Prob_not_C_given_E(cf, nf, cp, np)

def Rips(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return 1 - (Prob_not_C_given_E(cf, nf, cp, np) / Prob_not_C(cf, nf, cp, np))





# NEW SIMILARITY MEASURES (x23)

def Faith(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  t = cf + nf + cp + np
  return (cf+(0.5*np))/t

def Forbes1(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  t = cf +nf +cp +np
  return (t * cf)/((cf + cp) * (cf + nf))

def Forbes2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  t = cf + nf + cp + np 
  p = (cf + cp) * (cf + nf)
  k = (cf + cp) * (cf + cp)
  mini = 0

  if cf + cp > cf + nf:
    mini = cf + nf
  else:
    mini = cf + cp 

  m = t * mini
# check this as it seems to measure the reverse of what we want!
  return (((t * cf) - p)/ (m - k))

def Sorgenfrei(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return (cf *cf )/((cf +cp )*(cf +nf ))

def Mountford(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return cf /((0.5*((cf *cp ) + (cf *nf ))) + (cp *nf ))

def Mcconnaughey(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return ((cf *cf )-(cp *nf ))/((cf +cp )*(cf +nf ))

def DandK(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  a = cf / 2
  b = 1 / (cf + cp)
  k = 1 / (cf + nf)
  return a * (b + k)

def Dennis(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  a = (cf * np) - (cp * nf)
  b = (cf + np) * (cp + nf)
  t = cf + nf + cp + np 
  return a/math.sqrt(t*b)

def Simpson(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
 
  if cf + cp > cf + nf:
    mini = cf + nf
  else:
    mini = cf + cp 

  return cf / mini

def FagerMc(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  a = cf /(math.sqrt((cf +cp )*(cf +nf )))
  
  if cf + cp > cf + nf:
    maxi = cf + cp
  else:
    maxi = cf + nf

  return a - maxi;

def Gower(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (cf +np )/math.sqrt((cf +cp )*(cf +nf )*(cp +np )*(nf +np ))

def Ochiai2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  bottom = (cf +cp )*(cf +nf )*(cp +np )*(nf +np );
  return (cf *np ) / math.sqrt(bottom)

def SokalSneath4(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  a = cf /(cf +cp )
  b1 = cf /(cf +nf )
  b2 = np /(cp +np )
  d = np /(nf +np )
  return (a+b1+b2+d)/4
 
def SokalSneath5(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  return (cf *np ) / math.sqrt((cf +cp )*(cf +nf )*(cp +np )*(nf +np ))
 
def Cole(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  two = 2
  top = math.sqrt(two) * ((cf *np ) - (cp *nf ))
  r_bot = (cf +cp )*(cf +nf )*(cp +np )*(nf +np )
  l_bot = ((cf *np ) - (cp *nf )) * ((cf *np ) - (cp *nf ))
  return (top / l_bot - r_bot)

def Stiles(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  bottom = (cf +cp )*(cf +nf )*(cp +np )*(nf +np )
  t = cf +nf +cp +np 
  top = t*pow(((abs(cf *np  - cp *nf )) - t/2)*((abs(cf *np  - cp *nf )) - t/2), 2)
  return math.log10(top / bottom)

def Dispersion(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return (cf *np ) - (cp *nf )

def Michael(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  top = 4*((cf *np ) - (cp *nf ))
  bottom = (pow((cf +np ),2) + pow((cp +np ),2))
  return top/bottom

def Baroni1(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  top = math.sqrt(cf +np ) + cf
  bottom = math.sqrt(cf +np ) + cf  + np  + nf
  return top/bottom

def Baroni2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  top = math.sqrt(cf +np ) + cf  - (cf  + nf )
  bottom = math.sqrt(cf +np ) + cf  + np  + nf 
  return  top/bottom

def ShapeDiff(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  t = cf+nf+cp+np
  return -((t*(cp+nf)) - ((cp-nf)*(cp-nf)))


def PatternDiff(cf, nf, cp, np):
  return -(cp*nf)

def Fager(cf, nf, cp, np):
  return (cf/math.sqrt((cf+nf)*(cf+cp))) - (1/(2*math.sqrt(cf+nf)))


# OLD MEASURES (x17)

def Jaccard_etc(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return cf/(cf+cp+nf)

def Scott_etc(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return 0.5*((cf/((2*cf)+nf+cp) + (np/((2*np)+nf+cp))))

def Kulczynski2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return 0.5*((cf/(cf+nf)) + (cf/(cf+cp)))

def Ochiai(cf, nf, cp, np):
  cf = cf
  nf = nf 
  cp = cp
  np = np

  if cf == 0:
    return 0

  return math.log(cf) - 0.5 * math.log(cp + cf)

  return cf/(math.sqrt((cf+nf)*(cf+cp)))

def M2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return cf / (cf + np + (2 * (nf + cp)))

def Naish_etc(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return cf - (cp/(cp + np + 1))

def Fleiss(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  x = ((4 * cf) * np) - ((4 * nf) * cp) - ((nf - cp) * (nf- cp))
  y = (2*cf) + nf + cp + (2*np) + nf + cp

  return x/y

def Ample2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return (cf/(cf+nf)) - (cp/(cp+np))

def ArithmeticMean(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  x = ((2*cf)*np) - ((2*nf)*cp)
  y = (cf + cp) * (np + nf)
  z = (cf + nf) * (cp + np)

  return x/(y + z)


def HarmonicMean(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  x = ((cf)*np) - ((nf)*cp)
  y = (cf + cp) * (np + nf)
  z = (cf + nf) * (cp + np)
  top = x*(y+z)
  a = (cf + cp) * (np + nf)
  b = (cf + nf) * (cp + np)
  bottom = a*b

  return top/bottom

def Cohen(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  x = ((2*cf)*np) - ((2*nf)*cp)
  y = (cf + cp) * (np + cp)
  z = (cf + nf) * (nf + np)

  return x/(y + z)

def Wong2_etc(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return cf-cp

def Wong3(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  buff = 0

  if cp <= 2:
    buff = cf - cp

  if 2 < cp and cp <= 10:
    buff = cf - (2 + (0.1*(cp - 2)))

  if 10 < cp:
    buff = cf - (2.8 + (0.01*(cp-10)))

  return buff

def Wong3Naish(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  buff = 0

  if cp + cf < 0:
    buff = -1000
  else:
    if cp <= 2:
      buff = cf - cp

    if 2 < cp and cp <= 10:
      buff = cf - (2 + (0.1*(cp - 2)))

    if 10 < cp:
      buff = cf - (2.8 + (0.01*(cp-10)))

  return buff


def CBISqrt(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  bottom_l = 1/Prob_E_given_C(cf, nf, cp, np)
  bottom_r = math.sqrt(cf+nf)/math.sqrt(cf)

  return 2/(bottom_l+bottom_r)
 

def CBIlog(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  bottom_l = 1/Prob_E_given_C(cf, nf, cp, np)
  bottom_r = math.log10(cf+nf)/math.log10(cf)

  return 2/(bottom_l+bottom_r);


def Zoltar(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c
  return cf/((cf+nf+cp)+((10000 * nf * cp) / cf))


# custom (x1)

def Lex(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  t = cf+nf+cp+np+1
  g = (cf+np)/t

  output = 0

  if nf < 1:
    output = g+3

  if cf >= 1 and nf > 1 and cp < 1 :
    output = g+2

  if cf >= 1 and nf > 1 and cp > 1 :
    output = g+1

  if cf < 1:
    output = g

  return output

def Const(cf, nf, cp, np):
  return 1.0

def Rand(cf, nf, cp, np):
  if cf + cp > 0:
    return 1.0 + random.random()
  else:
    return 0

# more Association metrics x13 (+ 1 helper function Prob_not_C_and_not_E)

def PhiCoefficient(cf, nf, cp, np):
  p = Prob_C(cf, nf, cp, np) * Prob_E(cf, nf, cp, np)
  a = 1-Prob_C(cf, nf, cp, np)
  b = 1-Prob_E(cf, nf, cp, np)

  if p*a*b == 0:
    return 1000

  return (Prob_C_and_E(cf, nf, cp, np) - p) / math.sqrt(p*a*b)

def Kappa(cf, nf, cp, np):
  p = Prob_C(cf, nf, cp, np) * Prob_E(cf, nf, cp, np);
  a = Prob_not_C(cf, nf, cp, np) * Prob_not_E(cf, nf, cp, np);
  return ((Prob_C_and_E(cf, nf, cp, np) + Prob_not_C_and_not_E(cf, nf, cp, np)) - p - a) / (1-p-a)

def MI(cf, nf, cp, np):
  top = Prob_C_and_E(cf, nf, cp, np) * math.log10(Prob_C_and_E(cf, nf, cp, np) / (Prob_C(cf, nf, cp, np) * Prob_E(cf, nf, cp, np)));
  bottom = -Prob_C(cf, nf, cp, np) - math.log10(Prob_C(cf, nf, cp, np)) - Prob_E(cf, nf, cp, np) - math.log10(Prob_E(cf, nf, cp, np));
  return top / bottom

def JMeasure(cf, nf, cp, np):
  t = cf+nf+cp+np
  a = Prob_C_and_E(cf, nf, cp, np) * math.log10(Prob_E_given_C(cf, nf, cp, np) / Prob_E(cf, nf, cp, np))
  p_notc_e = Prob_not_C_given_E(cf, nf, cp, np)
  p_notc = Prob_not_C(cf, nf, cp, np)
  p_note_c = Prob_not_E_given_C(cf, nf, cp, np)
  p_note = Prob_not_E(cf, nf, cp, np)

  if p_note_c == 0 or p_note == 0:
    b = cp/t
  else:
    b = cp/t * math.log10(p_note_c / p_note)

  c = Prob_C_and_E(cf, nf, cp, np) * math.log10(Prob_C_given_E(cf, nf, cp, np) / Prob_C(cf, nf, cp, np))

  if p_notc_e == 0 or p_notc == 0:
    d = nf/t
  else:
    d = nf/t * math.log10(p_notc_e / p_notc)

  output = 0

  if a+b < c+d:
    output = c+d

  if a+b >= c+d:
    output = a+b

  return output

def GiniIndex(cf, nf, cp, np):
  a = Prob_C(cf, nf, cp, np) * ((Prob_E_given_C(cf, nf, cp, np)*Prob_E_given_C(cf, nf, cp, np)) + (Prob_not_E_given_C(cf, nf, cp, np)*Prob_not_E_given_C(cf, nf, cp, np)))
  b = Prob_not_C(cf, nf, cp, np) * ((Prob_E_given_not_C(cf, nf, cp, np)*Prob_E_given_not_C(cf, nf, cp, np))) + (Prob_not_E_given_not_C(cf, nf, cp, np) * Prob_not_E_given_not_C(cf, nf, cp, np))
  c = (Prob_E(cf, nf, cp, np)*Prob_E(cf, nf, cp, np)) - (Prob_not_E(cf, nf, cp, np)*Prob_not_E(cf, nf, cp, np))
  d = (a + b) - c

  e = Prob_E(cf, nf, cp, np) * ((Prob_C_given_E(cf, nf, cp, np) * Prob_C_given_E(cf, nf, cp, np)) + (Prob_not_C_given_E(cf, nf, cp, np) * Prob_not_C_given_E(cf, nf, cp, np)))
  f = Prob_not_E(cf, nf, cp, np) * ((Prob_C_given_not_E(cf, nf, cp, np)*Prob_C_given_not_E(cf, nf, cp, np))) + (Prob_not_C_given_not_E(cf, nf, cp, np) * Prob_not_C_given_not_E(cf, nf, cp, np))
  g = (Prob_C(cf, nf, cp, np)*Prob_E(cf, nf, cp, np)) - (Prob_not_C(cf, nf, cp, np)*Prob_not_E(cf, nf, cp, np))
  h = (e + f) - g

  output = 0

  if d < h:
    output = h

  if d >= h:
    output = d

  return output

def Confidence(cf, nf, cp, np):
  a = Prob_C_given_E(cf, nf, cp, np)
  b = Prob_E_given_C(cf, nf, cp, np)

  output = 0

  if a < b:
    output = b

  if a >= a:
    output = a

  return output

def Laplace(cf, nf, cp, np):
  t = cf + nf + cp + np
  a = ((t * Prob_C_and_E(cf, nf, cp, np)) + 1) / ((t * Prob_C(cf, nf, cp, np)) + 2)
  b = ((t * Prob_C_and_E(cf, nf, cp, np)) + 1) / ((t * Prob_E(cf, nf, cp, np)) + 2)

  output = 0

  if a < b:
    output = b

  if a >= a:
    output = a

  return output

def Conviction(cf, nf, cp, np):
  t = cf + nf + cp + np
  a = Prob_C(cf, nf, cp, np) * Prob_not_E(cf, nf, cp, np)
  b = cp / t
  c = Prob_E(cf, nf, cp, np) * Prob_not_C(cf, nf, cp, np)
  d = nf / t

  if b == 0 or d == 0:
    return 0.0

  output = 0

  if a/b < c/d:
    output = c/d

  if a/b >= c/d:
    output = a/b

  return output

def Interest(cf, nf, cp, np):
  return  Prob_C_and_E(cf, nf, cp, np) / (Prob_C(cf, nf, cp, np) * Prob_E(cf, nf, cp, np))

def Certainty(cf, nf, cp, np):
  if Prob_E(cf, nf, cp, np) == 1.0 or Prob_C(cf, nf, cp, np) == 1.0:
    return 10000

  a = (Prob_E_given_C(cf, nf, cp, np) -  Prob_E(cf, nf, cp, np)) / (1 -  Prob_E(cf, nf, cp, np))
  b = (Prob_C_given_E(cf, nf, cp, np) -  Prob_C(cf, nf, cp, np)) / (1 -  Prob_C(cf, nf, cp, np))

  output = 0

  if a < b:
    output = b
  else:
    output = a

  return output

def AddedValue(cf, nf, cp, np):
  a = (Prob_E_given_C(cf, nf, cp, np) -  Prob_E(cf, nf, cp, np))
  b = (Prob_C_given_E(cf, nf, cp, np) -  Prob_C(cf, nf, cp, np))

  output = 0

  if a < b:
    output = b

  if a >= a:
    output = a

  return output


def CollectiveStrength(cf, nf, cp, np):
  a = Prob_C_and_E(cf, nf, cp, np) + Prob_not_C_and_not_E(cf, nf, cp, np)
  b = (Prob_C(cf, nf, cp, np) * Prob_E(cf, nf, cp, np)) + (Prob_not_C(cf, nf, cp, np) * Prob_not_E(cf, nf, cp, np)) 
  c = 1 - (Prob_C(cf, nf, cp, np) * Prob_E(cf, nf, cp, np)) - (Prob_not_C(cf, nf, cp, np) * Prob_not_E(cf, nf, cp, np)) 
  d = 1 - (Prob_C_and_E(cf, nf, cp, np) - Prob_not_C_and_not_E(cf, nf, cp, np))

  return (a/b) * (c/d)


def Klosgen(cf, nf, cp, np):
  a = math.sqrt(Prob_C_and_E(cf, nf, cp, np))
  b = (Prob_E_given_C(cf, nf, cp, np) -  Prob_E(cf, nf, cp, np))
  c = (Prob_C_given_E(cf, nf, cp, np) -  Prob_C(cf, nf, cp, np))

  output = 0

  if c < b:
    output = b

  if c >= b:
    output = c

  return a * output

def Just_cf(cf, nf, cp, np):
  return cf

def Just_nf(cf, nf, cp, np):
  return nf

def Lex_Ochiai(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  g = cf/(math.sqrt((cf+nf)*(cf+cp)))

  output = 0

  if nf < 1:
    output = g+3

  if cf >= 1 and nf > 1 and cp < 1 :
    output = g+1

  if cf >= 1 and nf > 1 and cp > 1 :
    output = g

  if cf < 1:
    output = 0

  return output

def Lex_Zoltar(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  g = cf/((cf+nf+cp)+((10000 * nf * cp) / cf))

  output = 0

  if nf < 1:
    output = g+3

  if cf >= 1 and nf > 1 and cp < 1 :
    output = g+1

  if cf >= 1 and nf > 1 and cp > 1 :
    output = g

  if cf < 1:
    output = 0

  return output

def Lex_M2(cf, nf, cp, np):
  cf = cf + c
  nf = nf + c
  cp = cp + c
  np = np + c

  g = cf / (cf + np + (2 * (nf + cp)))

  output = 0

  if nf < 1:
    output = g+3

  if cf >= 1 and nf > 1 and cp < 1 :
    output = g+1

  if cf >= 1 and nf > 1 and cp > 1 :
    output = g

  if cf < 1:
    output = 0

  return output
