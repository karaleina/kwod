# -*- coding: utf-8 -*-
import math


class QRSCompare(object):
   def __init__(self):
        pass

   def compare_segmentation(self, reference=None, test=None,
                            sampling_rate=250, tol_time=0.05):

        # 1 krok: znalezienie TP
        TP = []
        for element in reference:
            for item in test:
                potential_TP = None
                min_diff = None
                if item <= (element+tol_time) and item >= (element-tol_time):
                    potential_diff = math.fabs(item-element)
                    if min_diff == None:
                        min_diff = potential_diff
                        potential_TP = item
                    elif potential_diff <= min_diff:
                        min_diff = potential_diff
                        potential_TP = item
                if(potential_TP!=None): TP.append(potential_TP)

        # 2 krok: znalezienie FP
        FP = []
        for element in test:
            if not(element in TP):
                FP.append(element)

        # 3 krok: znalezienie FN
        FN = []
        for element in reference:
            is_potential_FN = True
            for item in test:
                if item <= (element+tol_time) and item >= (element-tol_time):
                    is_potential_FN = False
                    break
            if(is_potential_FN == True):
                FN.append(element)

        # 4 krok: znalezienie TN
        # ograniczam liczbę TN, aby punkty mało istotne nie zdominowały statystyki
        TN = []
        not_qrs = []
        for indeks, element in enumerate(reference):
            if indeks < (len(reference) - 1) :
                 not_qrs.append(reference[indeks + 1] + (reference[indeks + 1] - reference[indeks])/2)


        #print("Not QRS: ", not_qrs)
        for element in not_qrs:
            is_potential_TN = True
            for item in test:
                if item <= (element+tol_time) and item >= (element-tol_time):
                    is_potential_TN = False
                    break
            if is_potential_TN:
                TN.append(element)

        sensivity = len(TP)/(len(TP)+len(FN))
        specifity = len(TN)/(len(TN)+len(FP))
        return [sensivity, specifity]
