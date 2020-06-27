#!python
#!/usr/bin/python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#====================================
#
# @file   : evolution.py
# @version: see VERSION
# @created: 2020-06-27
# @author : pyramid
# @brief  : computational evolution time
# This is a computational proof of evolution probability
# Mathematical proff is available in
# There’s plenty of time for evolution. Herbert Wilf. 2010
# https://www.pnas.org/content/107/52/22454.full.pdf
# where the number of guesses is found to be
# K^L or for our model 10(numbers)^number_genes
#====================================
# Code style: 
# Classes - CamelCase 
# Methods - mixedCase (recommended: lowercase_with_underscores) 
# Constants - ALL_CAPITALS 
# public variables - lowercase_with_underscores 
# private variables - lowercase_with_underscores 
# also see http://www.python.org/dev/peps/pep-0008/ 
#====================================

VERSION = "v0.202006.27"


#=========================================
# imports
#=========================================

import os
import sys
import timeit
import random


#=========================================
# constants
#=========================================


#=========================================
# main entry
#=========================================

def main():
  # init
  echoStart()
  echoConfig()

  # exec
  print("--- Experiment Intro ---")
  print("Both experiments compute zero time for natural selection")
  print("so that the number of mutations required for the experiment must")
  print("be multiplied by the time natural selection to confirm the mutated")
  print("gene to be successful (i.e. becoming prevalent among a population).")
  print("In best case this would be one successful mutation every 10 years, the obtained")
  print("average mutations need to be multiplied by 10 years.")
  print("Humans have 20 - 25 000 genes.")
  print("Simple organisms have some 4 000 genes.")
  print("Minimum genes in single-cell organisms is 300.")
  print("Here we are satisfied with the comparison of average times")
  print("for finding 10 successful genes.")
  print("")
  print("Note that the experiments neither prove or disprove the possibility")
  print("of evolution but rather the probability of it having occurred in such")
  print("a large variety given the relatively short time required to evolve")
  print("successful combinations due to INDEPENDENCE of mutations and natural")
  print("selection.")
  print("Further, the experiments do not prove or disprove that mutation")
  print("success or failure probability is uniformly distributed, which")
  print("is the basic assumption in the computational proof.")
  print("")
  print("We obtain the following results on a single-core 2.20GHz CPU")
  print("Assuming 1 year between generations and 10 generations for")
  print("a successful gene to prevail, one mutation takes 10 years")
  print("to have successfully evolved.")
  print("DEPENDENT Experiment (1000 iterations)")
  print("-   6 genes: 10 Myears")
  print("-   7 genes: 80 Myears")
  print("-  10 genes:")
  print("")
  print("")
  print("")
  print("INDEPENDENT Experiment (1000 iterations)")
  print("-   6 genes: 600 years")
  print("- 100 genes: 10 kyears")
  print("- 300 genes: 30 kyears")
  print("- 20 kgenes: 200 kyears")
  print("")

  evolveAllAtOnceMulti()
  evolveProgressiveMulti()

  # finalize
  echoFinish()


#=========================================
# functions
#=========================================

intlen = 10
intmin = pow(10,intlen-1)
intmax = pow(10,intlen)-1
iter = 100
mutationTimeYears = 10  # successful mutation time for genes


#-----------------------------------------
# evolveAllAtOnce
#-----------------------------------------


def evolveAllAtOnce():
  mutations = 0

  #init timer
  timeIni = timeit.default_timer()

  # show max value
  #print(sys.maxsize)
  #print(sys.maxsize+1)
  #print(pow(2,64))
  #print(pow(2,64)+1)

  # pick rand
  irnd = random.randint(intmin, intmax)
  print(intmin, intmax, irnd, " ", end="\r")

  # generate desired number
  # with uniform distribution
  while True:
    rrnd = random.randint(intmin, intmax)
    mutations += 1
    if rrnd==irnd:
      #print("success:", rrnd, mutations)
      break

  # measure time
  timeEnd = timeit.default_timer()
  elapsed = timeEnd - timeIni
  #print("runtime [s]: %.02f" % elapsed) #elapsed time in seconds
  return elapsed, mutations


def evolveAllAtOnceMulti():
  print("--- DEPENDENT Experiment ---")
  print("This DEPENDENT experiment creates the whole organism at once.")
  print("We select a large random integer representing our evolved organism.")
  print("Each character represents one successful gene.")
  print("Here, one mutated gene is only successful at the same time")
  print("also the other genes are mutated successfully.")
  print("This argument is prevalent in theories against the probability of evolution")
  print("postulating that life is too complex to have evolved by random.")
  print("Mathematically it is sound, as this experiment proves, since time")
  print("grows exponentially with the number of genes.")
  print("The runtime for a simple (low number of genes) organism is enormous.")
  print("However, the logical presumption is flawed, since a new gene mutation")
  print("is independent from previous successful mutations.")
  print("It is also flawed since it does not allow for the large variety of species.")
  print("")

  avg = 0
  tot = 0
  mutations = 0 # average no mutations to get successful combination
  for i in range(iter):
    elapsed, mut = evolveAllAtOnce()
    avg = (avg*i+elapsed)/(i+1)
    tot += elapsed
    mutations = (mutations*i+mut)/(i+1)
    print(" ", i, "elapsed, average: %.06f, %.06f | mutations: %.00d %.00d " % (elapsed, avg, mut, mutations), end="\r")
  print("\nno. genes =", intlen)
  print("no. iter =", iter)
  print("mutation time [a] =", mutationTimeYears)
  print(" average time [s]: %.04f" % avg)
  print("total runtime [s]: %.04f" % tot)
  print("average mutations: %.02f" % mutations)
  print("evoluation time [a]: %.00d" % (mutations*mutationTimeYears))


#-----------------------------------------
# evolveProgressive
#-----------------------------------------

def evolveProgressive():
  mutations = 0

  #init timer
  timeIni = timeit.default_timer()

  # pick rand
  irnd = random.randint(intmin, intmax)
  srnd = str(irnd)
  #print(intmin, intmax, irnd, " ", end="\r")

  # generate desired number
  # with uniform distribution
  srndout = ""
  for i in range(intlen):
    #print(i)
    while True:
      rrnd = random.randint(0,9)
      mutations += 1
      #print(rrnd)
      if str(rrnd)==srnd[i]:
        #print("found:", srndout)
        srndout += str(rrnd)
        break
  #print("success:", srndout)


  # measure time
  timeEnd = timeit.default_timer()
  elapsed = timeEnd - timeIni
  #print("runtime [s]: %.02f" % elapsed) #elapsed time in seconds
  return elapsed, mutations


def evolveProgressiveMulti():
  print("--- INDEPENDENT Experiment ---")
  print("This INDEPENDENT experiment creates each successful genre one by one.")
  print("We select a large random integer representing our evolved organism.")
  print("Each character represents one successful gene.")
  print("Here, one mutated gene is only successful independently of other genes")
  print("success which has previously been proven by natural selection.")
  print("This supports the hypothesis for high probability of evolution")
  print("for a large diversity of organisms.")
  print("This experiment proves, that evolution time is linear to the")
  print("the number of genes.")
  print("A new gene mutation is independent from previous successful mutations.")
  print("It allows for a large variety of species.")
  print("")

  avg = 0
  tot = 0
  mutations = 0 # average no mutations to get successful combination
  for i in range(iter):
    elapsed, mut = evolveProgressive()
    avg = (avg*i+elapsed)/(i+1)
    tot += elapsed
    mutations = (mutations*i+mut)/(i+1)
    print(" ", i, "elapsed, average: %.06f, %.06f | mutations: %.00d %.00d " % (elapsed, avg, mut, mutations), end="\r")
  print("\nno. genes =", intlen)
  print("no. iter =", iter)
  print("mutation time [a] =", mutationTimeYears)
  print(" average time [s]: %.06f" % avg, " "*14)
  print("total runtime [s]: %.02f" % tot)
  print("evoluation time [a]: %.00d" % (mutations*mutationTimeYears))


#=========================================
# information
#=========================================

def echoStart():
  print("---------------------------------")
  print("--- " + __file__ + " " + VERSION + " ---")
  print("---------------------------------")

def echoConfig():
  pass

def echoFinish():
  pass



#=========================================
# Invoke main from cli
#=========================================

if __name__ == "__main__":
  main()


