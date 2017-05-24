# -*- coding: utf-8 -*-
import math


class QRSCompare(object):
   def __init__(self):
        pass

   def compare_segmentation(self, reference=None, test=None,
                            sampling_rate=250, tol_time=0.05):
        if test:
            max_test = max(test)
            min_test = min(test)
        else:
            max_test = -1
            min_test = -1

        new_reference = []

        # Ograniczenie zbioru referencyjnego do potrzeb
        for element in reference:
            if (element <= max_test and element >= min_test) :
                new_reference.append(element)


        # 1 krok: znalezienie TP
        TP = []
        for element in new_reference:
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
        for element in new_reference:
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
        for indeks, element in enumerate(new_reference):
            if indeks < (len(new_reference) - 1) :
                 not_qrs.append(new_reference[indeks + 1] + (new_reference[indeks + 1] - new_reference[indeks]) / 2)


        #print("Not QRS: ", not_qrs)
        for element in not_qrs:
            is_potential_TN = True
            for item in test:
                if item <= (element+tol_time) and item >= (element-tol_time):
                    is_potential_TN = False
                    break
            if is_potential_TN:
                TN.append(element)

        denom_sensiti = len(TP) + len(FN)
        if denom_sensiti != 0:
            sensivity = len(TP) / denom_sensiti
        else:
            sensivity = 0

        denom_specifi = (len(TN) + len(FP))
        if denom_specifi != 0:
            specifity = len(TN) / denom_specifi
        else:
            specifity = 0

        return [sensivity, specifity]
