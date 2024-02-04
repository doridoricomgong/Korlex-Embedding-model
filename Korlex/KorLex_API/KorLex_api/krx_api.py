import json
import time
import pickle

import pandas as pd
import numpy as np
import copy
import os

## Korlex API Definition
#from krx_def import *
from .krx_def import *

class KorLexAPI:
    ### PRIVATE ###
    def __init__(self, ssInfo_path:str, seIdx_path:str, reIdx_path:str, kwn_std_path:str):
        print("[KorLexAPI][INIT] Plz Wait...")

        self.is_set_ssInfo_path = False
        self.is_set_seIdx_path = False
        self.is_set_reIdx_path = False
        self.is_set_kwn_std_path = False

        # check seIdx_path
        if 0 >= len(seIdx_path):
            print("[KorLexAPI][INIT] ERR - Plz check seIdx_path:", seIdx_path)
            return
        if not os.path.exists(seIdx_path):
            print("[KorLexAPI][INIT] ERR -", seIdx_path, "is Not Existed !")
            return

        self.seIdx_path = seIdx_path
        self.is_set_seIdx_path = True

        # check reIdx_path
        if 0 >= len(reIdx_path):
            print("[KorLexAPI][INIT] ERR - Plz check reIdx_path:", reIdx_path)
            return
        if not os.path.exists(reIdx_path):
            print("[KorLexAPI][INIT] ERR -", reIdx_path, "is Not Existed !")
            return

        self.reIdx_path = reIdx_path
        self.is_set_reIdx_path = True

        # Check ssinfo_path
        if 0 >= len(ssInfo_path):
            print("[KorLexAPI][INIT] ERR - Plz check ssInfo_path:", ssInfo_path)
            return

        if not os.path.exists(ssInfo_path):
            print("[KorLexAPI][INIT] ERR -", ssInfo_path, "is Not Existed !")
            return

        self.is_set_ssInfo_path = True
        self.ssInfo_path = ssInfo_path

        # Check kwn_std_path
        if 0 >= len(kwn_std_path):
            print("[KorLexAPI][INIT] ERR - Plz check kwn_std_path:", kwn_std_path)
            return

        if not os.path.exists(kwn_std_path):
            print("[KorLexAPI][INIT] ERR -", kwn_std_path, "is Not Existed !")
            return

        self.is_set_kwn_std_path = True
        self.kwn_std_path = kwn_std_path

        print("[KorLexAPI][INIT] - Complete set to path,", self.ssInfo_path,
              "you can use load method.")

    # 단순 구현
    def change_pos_type(self, pos):
        if type(pos) == tuple:
            return str(pos[0])
        else:
            return str(pos)

    def change_sid_type(self, sid: int):
        if sid > 9:
            return str(sid)
        elif sid < 0:
            print("sid error check it out")
            return str(sid)
        else:
            return '0' + str(sid)

    '''class synset:
        def __init__(self, wordInfo: str):
            # long input word
            if wordInfo.count('.') != 2:
                print('Check if the format of word is [word.pos.sid]')
                self.Synset = ""

            # 단순 구현 버전
            word, pos, sid = wordInfo.split('.')
            self.Synset = Synset(text=word, pos=pos, sense_id=sid)'''

    def synset(self, wordInfo: str):
        # long input word
        if wordInfo.count('.') != 2:
            print('Check if the format of word is [word.pos.sid]')
            self.Synset = ""
            return self.Synset
        # 단순 구현 버전
        word, pos, s_num = wordInfo.split('.')
        self.Synset = Synset(text=word, pos=self.change_pos_type(pos), std_num=s_num)
        return self

    #수정필요
    def lemmas(self):
        # get siblings
        word = self.Synset.text
        raw_result = self.search_word(word=word, ontology=ONTOLOGY.KORLEX.value)
        siblings = []
        for line in raw_result:
            target = line[0].target
            if int(target.std_num) == int(self.Synset.std_num) and target.pos == self.Synset.pos:
                sibling = line[0].siblings
                for s_node in sibling:
                    for sset in s_node.synset_list:
                        siblings.append(sset)
        return siblings

    def hypernyms(self):
        hypernyms = []
        sibling_idx_list = np.where((self.kwn_std_df["ss_type"].values == self.Synset.pos) &
                                    (self.kwn_std_df["std_num"].values == self.Synset.std_num) &
                                    (self.kwn_std_df["korean"].values == self.Synset.text))
        #empty
        if sibling_idx_list[0].size == 0:
            return hypernyms

        sibling_soff_idx = []
        for sIdx in sibling_idx_list[0]:
            temp_soff = self.kwn_std_df.loc[sIdx]['soff']
            sibling_soff_idx += list(np.where((self.seIdx_df["soff"].values == temp_soff) &
                                               (self.seIdx_df["word"].values == self.Synset.text) &
                                               (self.seIdx_df["pos"].values == self.Synset.pos))[0])
        sibling_obj_list = []
        for sIdx in sibling_soff_idx:
            sibling_obj_list.append(copy.deepcopy(self.seIdx_df.loc[sIdx]))

        ret_json_list = []
        # Make Result Json
        for target_obj in sibling_obj_list:
            target_krx_json = self._make_result(target_obj=target_obj, ontology=ONTOLOGY.KORLEX.value,
                                                relation="parent",
                                                is_target=False)
            ret_json_list.append(copy.deepcopy(target_krx_json))
        if len(ret_json_list)==0:
            return ret_json_list


        for krx_result in ret_json_list:
            hypernyms += krx_result.results[0].synset_list
        return list(set(hypernyms))

    def hyponyms(self):
        hyponyms = []

        sibling_idx_list = np.where((self.kwn_std_df["ss_type"].values == self.Synset.pos) &
                                    (self.kwn_std_df["std_num"].values == self.Synset.std_num) &
                                    (self.kwn_std_df["korean"].values == self.Synset.text))
        # empty
        if sibling_idx_list[0].size == 0:
            return hyponyms

        sibling_soff_idx = []
        for sIdx in sibling_idx_list[0]:
            temp_soff = self.kwn_std_df.loc[sIdx]['soff']
            sibling_soff_idx += list(np.where((self.seIdx_df["soff"].values == temp_soff) &
                                              (self.seIdx_df["word"].values == self.Synset.text) &
                                              (self.seIdx_df["pos"].values == self.Synset.pos))[0])
        sibling_obj_list = []
        for sIdx in sibling_soff_idx:
            sibling_obj_list.append(copy.deepcopy(self.seIdx_df.loc[sIdx]))

        ret_json_list = []
        # Make Result Json
        for target_obj in sibling_obj_list:
            target_krx_json = self._make_result(target_obj=target_obj, ontology=ONTOLOGY.KORLEX.value,
                                                relation="child", is_target=False)
            ret_json_list.append(copy.deepcopy(target_krx_json))
        if len(ret_json_list)==0:
            return ret_json_list

        for krx_result in ret_json_list:
            hyponyms += krx_result.results[0].synset_list
        return list(set(hyponyms))

    def _make_result(self, target_obj: object, ontology: str, relation: str, is_target: bool):
        target_list = []

        # check if word is target
        if is_target:
            ele = "trg_elem"
            target_ele = "elem"
            target_pos = "pos"
        else:
            ele = "elem"
            target_ele = "trg_elem"
            target_pos = "trg_pos"

        search_idx = np.where(self.reIdx_df[ele].values == target_obj["soff"])
        for pt_idx in search_idx:
            for _, pt_item in self.reIdx_df.loc[pt_idx].iterrows():
                pt_relation = pt_item["relation"]
                if relation == pt_relation:
                    pt_elem = pt_item[target_ele]
                    pt_pos = pt_item[target_pos]
                    target_list.append((pt_elem, pt_pos))

        result_data = KorLexResult(Target(ontology=ontology,
                                          word=target_obj["word"],
                                          pos=self.change_pos_type(target_obj["pos"]),
                                          sense_id=self.change_sid_type(target_obj["senseid"]),
                                          soff=target_obj["soff"]), [], [])
        curr_ss_node = SS_Node(synset_list=[], soff=target_obj["soff"], pos=self.change_pos_type(target_obj["pos"]))

        for ele, pos in target_list:
            curr_se_matcing_list = np.where((self.seIdx_df["soff"].values == ele) &
                                            (self.seIdx_df["pos"].values == pos))
            for curr_se_idx in curr_se_matcing_list:
                for _, curr_se_item in self.seIdx_df.loc[curr_se_idx].iterrows():
                    curr_seIdx_word = curr_se_item["word"]
                    if curr_seIdx_word == target_obj["word"]:
                        continue
                    curr_seIdx_senseId = self.change_sid_type(curr_se_item["senseid"])
                    curr_seIdx_pos = self.change_pos_type(curr_se_item["pos"])

                    curr_kwn_std_num = self.find_std_num(curr_seIdx_word, curr_seIdx_senseId, curr_seIdx_pos)
                    if curr_kwn_std_num == '99':
                        continue

                    curr_synset_data = Synset(text=curr_seIdx_word, pos=curr_seIdx_pos,
                                              sense_id=curr_seIdx_senseId, std_num=curr_kwn_std_num)
                    curr_ss_node.synset_list.append(copy.deepcopy(curr_synset_data))

        result_data.results.append(curr_ss_node)

        return result_data

    def member_holonyms(self):
        holonyms = []
        sibling_idx_list = np.where((self.kwn_std_df["ss_type"].values == self.Synset.pos) &
                                    (self.kwn_std_df["std_num"].values == self.Synset.std_num) &
                                    (self.kwn_std_df["korean"].values == self.Synset.text))
        # empty
        if sibling_idx_list[0].size == 0:
            return holonyms

        sibling_soff_idx = []
        for sIdx in sibling_idx_list[0]:
            temp_soff = self.kwn_std_df.loc[sIdx]['soff']
            sibling_soff_idx += list(np.where((self.seIdx_df["soff"].values == temp_soff) &
                                              (self.seIdx_df["word"].values == self.Synset.text) &
                                              (self.seIdx_df["pos"].values == self.Synset.pos))[0])
        sibling_obj_list = []
        for sIdx in sibling_soff_idx:
            sibling_obj_list.append(copy.deepcopy(self.seIdx_df.loc[sIdx]))

        ret_json_list = []
        # Make Result Json
        for target_obj in sibling_obj_list:
            target_krx_json = self._make_result(target_obj=target_obj, ontology=ONTOLOGY.KORLEX.value,
                                                relation="#m",
                                                is_target=False)
            ret_json_list.append(copy.deepcopy(target_krx_json))

        if len(ret_json_list) == 0:
            return ret_json_list

        for krx_result in ret_json_list:
            holonyms += krx_result.results[0].synset_list
        return list(set(holonyms))

    #get synset for evaluation
    def eval_synset(self, word, pos):
        sibling_idx_list = np.where((self.kwn_std_df["ss_type"].values == pos) &
                                    (self.kwn_std_df["korean"].values == word))
        # empty
        if sibling_idx_list[0].size == 0:
            return []

        sibling_soff_set = set()
        for sIdx in sibling_idx_list[0]:
            temp_soff = self.kwn_std_df.loc[sIdx]['soff']
            temp_list = np.where((self.kwn_std_df["soff"].values == temp_soff)&
                                              (self.kwn_std_df["ss_type"].values == pos))[0]
            for soffIdx in temp_list:
                row = self.kwn_std_df.loc[soffIdx]
                sibling_soff_set.add(row['korean']+'.'+row['ss_type']+'.'+row['std_num'])
        l = []
        for wor in list(sibling_soff_set):
            text, pos, sid = wor.split('.')
            if text == word:
                l.append(wor)
        return l

    # get synset for evaluation
    def eval_synset_from_word(self, word, pos):
        sibling_idx_list = np.where((self.kwn_std_df["ss_type"].values == pos) &
                                    (self.kwn_std_df["korean"].values == word))
        # empty
        if sibling_idx_list[0].size == 0:
            return []

        all_words_set = set()
        for sIdx in sibling_idx_list[0]:
            row = self.kwn_std_df.loc[sIdx]
            all_words_set.add(row['korean'] + '.' + row['ss_type'] + '.' + row['std_num'])

        return list(all_words_set)

    # get synset for evaluation
    def fse_synset(self, word, pre_pos):
        text, pos, std_num = word.split('.')
        if pos != pre_pos:
            print('pos error check')

        sibling_idx_list = np.where((self.kwn_std_df["ss_type"].values == pos) &
                                    (self.kwn_std_df["std_num"].values == std_num) &
                                    (self.kwn_std_df["korean"].values == text))
        # empty
        if sibling_idx_list[0].size == 0:
            return []
        sibling_soff_set = set()
        for sIdx in sibling_idx_list[0]:
            temp_soff = self.kwn_std_df.loc[sIdx]['soff']
            temp_list = np.where((self.kwn_std_df["soff"].values == temp_soff) &
                                 (self.kwn_std_df["ss_type"].values == pos))[0]
            for soffIdx in temp_list:
                row = self.kwn_std_df.loc[soffIdx]
                sibling_soff_set.add(row['korean'] + '.' + row['ss_type'] + '.' + row['std_num'])

        return list(sibling_soff_set)

    # 단순구현 버전, ss_node 버전으로 교체해야됨
    def path_similarity(self, word1, word2):
        synset_list1 = set()
        synset_list2 = set()
        for syns in self.fse_synset(word1, word1.split('.')[1]):
            idx1 = self.kwn_synset_vocab.index(syns)
            synset_list1.add(str(idx1))
        for syns in self.fse_synset(word2, word2.split('.')[1]):
            idx2 = self.kwn_synset_vocab.index(syns)
            synset_list2.add(str(idx2))
        path1 = 1
        path2 = 0
        if word1 == word2:
            return 1 / path1
        total_set1 = set()
        total_set2 = set()
        total_set1 = total_set1.union(synset_list1)
        total_set2 = total_set2.union(synset_list2)
        inter = synset_list1.intersection(synset_list2)
        check = 0
        while len(inter) == 0:
            for syn in synset_list1:
                synset_list1 = synset_list1.union(set(self.neighbor_dic[str(syn)]))
            synset_list1 = synset_list1.difference(total_set1)
            total_set1 = total_set1.union(synset_list1)
            inter = total_set1.intersection(total_set2)
            path1 += 1
            if len(inter) != 0:
                break
            for syn in synset_list2:
                synset_list2 = synset_list2.union(set(self.neighbor_dic[str(syn)]))
            path2 += 1
            synset_list2 = synset_list2.difference(total_set2)
            total_set2 = total_set2.union(synset_list2)
            inter = total_set1.intersection(total_set2)
            check += 1
            if check > 100:
                return 0
        shortest_path = path1 + path2
        return 1 / shortest_path

    def new_path_similarity(self, word1, word2):
        try:
            idx1, idx2 = self.kwn_synset_vocab.index(word1), self.kwn_synset_vocab.index(word2)
        except:
            print('not in the vocab list')
            return -1
        path1 = 1
        path2 = 0
        if idx1 == idx2:
            return 1/path1
        synset_list1 = set()
        synset_list2 = set()
        synset_list1.add(str(idx1))
        synset_list2.add(str(idx2))
        total_set1 = set()
        total_set2 = set()
        total_set1 = total_set1.union(synset_list1)
        total_set2 = total_set2.union(synset_list2)
        inter = synset_list1.intersection(synset_list2)
        check = 0
        while len(inter) == 0:
            for syn in synset_list1:
                synset_list1 = synset_list1.union(set(self.neighbor_dic[str(syn)]))
            synset_list1 = synset_list1.difference(total_set1)
            total_set1 = total_set1.union(synset_list1)
            inter = total_set1.intersection(total_set2)
            path1 += 1
            if len(inter) != 0:
                break
            for syn in synset_list2:
                synset_list2 = synset_list2.union(set(self.neighbor_dic[str(syn)]))
            path2 += 1
            synset_list2 = synset_list2.difference(total_set2)
            total_set2 = total_set2.union(synset_list2)
            inter = total_set1.intersection(total_set2)
            check += 1
            if check > 100:
                return 0
        shortest_path = path1 + path2
        return 1/shortest_path


    #check if the word is in krx
    def check_word_is_in_krx(self, word):
        #input word = text.pos.std_num
        text, pos, std_num = word.split('.')
        same_list = np.where((self.kwn_std_df["korean"].values == text) & (
                self.kwn_std_df["std_num"].values == std_num) & (self.kwn_std_df["ss_type"].values == pos))
        if len(same_list[0]) > 0:
            return True
        else:
            return False

    #find stdnum
    def find_std_num(self, word, sense_id, pos):
        idx = np.where((self.kwn_std_df["korean"].values == word) & (self.kwn_std_df["ss_type"].values == pos) & (self.kwn_std_df["senseid"].values == int(sense_id)) )
        if len(idx[0]) == 0:
            # most of the cases are English word
            return '99'
        std_num = int(list(set(self.kwn_std_df.loc[idx[0]]['std_num'].values))[0])
        return self.change_sid_type(std_num)

    def _make_hyponym_list(self, soff:int, pos:str):
        ret_hyponym_list = []

        target_re_idx_list = np.where((self.reIdx_df["elem"].values == soff) &
                                        (self.reIdx_df["relation"].values == "child") &
                                        (self.reIdx_df["trg_pos"].values == pos))
        for t_elem_re_idx in target_re_idx_list:
            for _, reIdx_item in self.reIdx_df.loc[t_elem_re_idx].iterrows():
                trg_elem = reIdx_item["trg_elem"]
                trg_elem_seIdx_list = np.where((self.seIdx_df["soff"].values == trg_elem) &
                                               (self.seIdx_df["pos"].values == pos))

                for t_elem_se_idx in trg_elem_seIdx_list:
                    se_ss_node = SS_Node([], soff=trg_elem, pos=pos)
                    for _, seIdx_item in self.seIdx_df.loc[t_elem_se_idx].iterrows():
                        # update - 2022.11.09
                        curr_std_num = "00"  # update - 2022.11.09
                        target_std_num_list = np.where((self.kwn_std_df["soff"].values == seIdx_item["soff"]) &
                                                         (self.kwn_std_df["korean"].values == seIdx_item["word"]) &
                                                         (self.kwn_std_df["senseid"].values == seIdx_item["senseid"]))
                        if 0 < len(target_std_num_list[0]):
                            curr_std_num = self.kwn_std_df.loc[target_std_num_list[0]]["std_num"].values[0]

                        se_synset = Synset(text=seIdx_item["word"],
                                           sense_id=seIdx_item["senseid"],
                                           std_num=curr_std_num,
                                           pos=seIdx_item["pos"])
                        se_ss_node.synset_list.append(copy.deepcopy(se_synset))
                    ret_hyponym_list.append(copy.deepcopy(se_ss_node))

        return ret_hyponym_list

    def _make_result_json(self, target_obj:object, ontology:str):
        ret_korlex_result_list = []

        # check, is target parent dobule?
        target_parent_list = []
        check_parent_list = np.where(self.reIdx_df["trg_elem"].values == target_obj["soff"])
        for pt_idx in check_parent_list:
            for _, pt_item in self.reIdx_df.loc[pt_idx].iterrows():
                pt_relation = pt_item["relation"]
                if "child" == pt_relation:
                    pt_elem = pt_item["elem"]
                    pt_pos = pt_item["pos"]
                    target_parent_list.append((pt_elem, pt_pos))

        if 0 >= len(target_parent_list): # Except (e.g. eat(convert to korean))
            target_std_num = "00"  # update - 2022.11.09
            target_std_num_list = np.where((self.kwn_std_df["soff"].values == target_obj["soff"]) &
                                             (self.kwn_std_df["korean"].values == target_obj["word"]) &
                                             (self.kwn_std_df["senseid"].values == target_obj["senseid"]))
            if 0 < len(target_std_num_list[0]):
                target_std_num = self.kwn_std_df.loc[target_std_num_list[0]]["std_num"].values[0]

            result_data = KorLexResult(Target(ontology=ontology,
                                              word=target_obj["word"],
                                              pos=target_obj["pos"],
                                              sense_id=target_obj["senseid"],
                                              soff=target_obj["soff"],
                                              std_num=target_std_num
                                              ), results=[], hyponym=[])

            ss_node = SS_Node(synset_list=[], soff=target_obj["soff"], pos=target_obj["pos"])
            seIdx_matching_list = np.where(self.seIdx_df["soff"].values == ss_node.soff)
            for mat_idx in seIdx_matching_list:
                for _, seIdx_item in self.seIdx_df.loc[mat_idx].iterrows():
                    seIdx_word = seIdx_item["word"]
                    seIdx_pos = seIdx_item["pos"]
                    seIdx_senseId = seIdx_item["senseid"]

                    if seIdx_pos == target_obj["pos"]:
                        seIdx_std_num = "00"  # update - 2022.11.09
                        target_std_num_list = np.where((self.kwn_std_df["soff"].values == seIdx_item["soff"]) &
                                                         (self.kwn_std_df["korean"].values == seIdx_item["word"]) &
                                                         (self.kwn_std_df["senseid"].values == seIdx_item["senseid"]))
                        if 0 < len(target_std_num_list[0]):
                            seIdx_std_num = self.kwn_std_df.loc[target_std_num_list[0]]["std_num"].values[0]

                        synset_data = Synset(text=seIdx_word,
                                             sense_id=seIdx_senseId,
                                             std_num=seIdx_std_num,
                                             pos=seIdx_pos)
                        ss_node.synset_list.append(copy.deepcopy(synset_data))
            result_data.results.append(ss_node)

            hyponym_list = self._make_hyponym_list(soff=target_obj["soff"], pos=target_obj["pos"])
            result_data.hyponym = copy.deepcopy(hyponym_list)

            ret_korlex_result_list.append(result_data)

        # Existed Parent
        for target_parent in target_parent_list:
            # set target info
            target_std_num = "00"  # update - 2022.11.09
            target_std_num_list = np.where((self.kwn_std_df["soff"].values == target_obj["soff"]) &
                                             (self.kwn_std_df["korean"].values == target_obj["word"]) &
                                             (self.kwn_std_df["senseid"].values == target_obj["senseid"]))
            if 0 < len(target_std_num_list[0]):
                target_std_num = self.kwn_std_df.loc[target_std_num_list[0]]["std_num"].values[0]

            result_data = KorLexResult(Target(ontology=ontology,
                                              word=target_obj["word"],
                                              pos=target_obj["pos"],
                                              sense_id=target_obj["senseid"],
                                              soff=target_obj["soff"],
                                              std_num=target_std_num
                                              ), results=[], hyponym=[])

            ## Search processing
            curr_target = (target_parent[0], target_parent[-1])

            # current target synset
            curr_ss_node = SS_Node(synset_list=[], soff=target_obj["soff"], pos=target_obj["pos"])
            curr_se_matcing_list = np.where((self.seIdx_df["soff"].values == target_obj["soff"]) &
                                            (self.seIdx_df["pos"].values == target_obj["pos"]))

            for curr_se_idx in curr_se_matcing_list:
                for _, curr_se_item in self.seIdx_df.loc[curr_se_idx].iterrows():
                    curr_seIdx_word = curr_se_item["word"]
                    curr_seIdx_senseId = curr_se_item["senseid"]
                    curr_seIdx_pos = curr_se_item["pos"]
                    # update - 2022.11.09
                    curr_std_num = "00"  # update - 2022.11.09
                    target_std_num_list = np.where((self.kwn_std_df["soff"].values == curr_se_item["soff"]) &
                                                     (self.kwn_std_df["korean"].values == curr_se_item["word"]) &
                                                     (self.kwn_std_df["senseid"].values == curr_se_item["senseid"]))
                    if 0 < len(target_std_num_list[0]):
                        curr_std_num = self.kwn_std_df.loc[target_std_num_list[0]]["std_num"].values[0]

                    curr_synset_data = Synset(text=curr_seIdx_word,
                                              sense_id=curr_seIdx_senseId,
                                              std_num=curr_std_num,
                                              pos=curr_seIdx_pos)
                    curr_ss_node.synset_list.append(copy.deepcopy(curr_synset_data))
            result_data.results.append(curr_ss_node)

            # search hyponym for target
            hyponym_list = self._make_hyponym_list(soff=curr_target[0], pos=curr_target[-1])
            result_data.hyponym = copy.deepcopy(hyponym_list)

            # search loop
            while True:
                prev_target = copy.deepcopy(curr_target)

                # Search synset
                ss_node = SS_Node(synset_list=[], soff=curr_target[0], pos=curr_target[-1])
                seIdx_matching_list = np.where(self.seIdx_df["soff"].values == curr_target[0])
                for mat_idx in seIdx_matching_list:
                    for _, seIdx_item in self.seIdx_df.loc[mat_idx].iterrows():
                        seIdx_word = seIdx_item["word"]
                        seIdx_pos = seIdx_item["pos"]
                        seIdx_senseId = seIdx_item["senseid"]

                        if seIdx_pos == curr_target[-1]:
                            # update - 2022.11.09
                            curr_std_num = "00"  # update - 2022.11.09
                            target_std_num_list = np.where((self.kwn_std_df["soff"].values == seIdx_item["soff"]) &
                                                             (self.kwn_std_df["korean"].values == seIdx_item["word"]) &
                                                             (self.kwn_std_df["senseid"].values == seIdx_item[
                                                                 "senseid"]))
                            if 0 < len(target_std_num_list[0]):
                                curr_std_num = self.kwn_std_df.loc[target_std_num_list[0]]["std_num"].values[0]

                            synset_data = Synset(text=seIdx_word,
                                                 sense_id=seIdx_senseId,
                                                 std_num=curr_std_num,
                                                 pos=seIdx_pos)
                            ss_node.synset_list.append(copy.deepcopy(synset_data))

                if 0 >= len(ss_node.synset_list):
                    break
                else:
                    result_data.results.append(copy.deepcopy(ss_node))

                # Search parent
                reIdx_matching_list = np.where(self.reIdx_df["trg_elem"].values == curr_target[0])
                for mat_idx in reIdx_matching_list:
                    for _, reIdx_item in self.reIdx_df.loc[mat_idx].iterrows():
                        reIdx_rel = reIdx_item["relation"]
                        reIdx_pos = reIdx_item["pos"]

                        if ("child" == reIdx_rel) and (reIdx_pos == curr_target[-1]):
                            reIdx_elem = reIdx_item["elem"]
                            curr_target = (reIdx_elem, reIdx_pos)
                            break

                if(prev_target[0] == curr_target[0]): break
            ret_korlex_result_list.append(copy.deepcopy(result_data))

        return ret_korlex_result_list

    ### PUBLIC ###
    def load_synset_data(self):
        print("[KorLexAPI][load_synset_data] Load pickle Data, Wait...")
        is_set_pkl_files = True
        if not self.is_set_ssInfo_path:
            print("[KorLexAPI][load_synset_data] ERR - Plz set json path")
            is_set_pkl_files = False

        if not self.is_set_seIdx_path:
            print("[KorLexAPI][load_synset_data] ERR - Plz set seIdx path")
            is_set_pkl_files = False

        if not self.is_set_reIdx_path:
            print("[KorLexAPI][load_synset_data] ERR - Plz set reIdx path")
            is_set_pkl_files = False

        if not self.is_set_kwn_std_path:
            print("[KorLexAPI][load_synset_data] ERR - Plz set kwn_std path")
            is_set_pkl_files = False

        if not is_set_pkl_files:
            return

        # Load seIdx.pkl
        print("[KorLexAPI][load_synset_data] Loading seIdx.pkl...")
        self.seIdx_df = None
        with open(self.seIdx_path, mode="rb") as seIdx_file:
            self.seIdx_df = pickle.load(seIdx_file)
            self.seIdx_df.drop_duplicates(inplace=True)
            print("[KorLexAPI][load_synset_data] Loaded seIdx.pkl !")

        # Load reIdx.pkl
        print("[KorLexAPI][load_synset_data] Loading reIdx.pkl...")
        self.reIdx_df = None
        with open(self.reIdx_path, mode="rb") as reIdx_file:
            self.reIdx_df = pickle.load(reIdx_file)
            self.reIdx_df.drop_duplicates(inplace=True)
            print("[KorLexAPI][load_synset_data] Loaded reIdx.pkl !")

        # Load ssInfo
        print("[KorLexAPI][load_synset_data] Loading ssInfo.pkl...")
        self.ssInfo_df = None
        with open(self.ssInfo_path, mode="rb") as ssInfo_file:
            self.ssInfo_df = pickle.load(ssInfo_file)
            self.ssInfo_df.drop_duplicates(inplace=True)
            print("[KorLexAPI][load_synset_data] Loaded ssInfo.pkl !")

        # Load kwn_std
        print("[KorLexAPI][load_synset_data] Loading kwn_std.pkl...")
        self.kwn_std_df = None
        with open(self.kwn_std_path, mode="rb") as kwn_std_file:
            self.kwn_std_df = pickle.load(kwn_std_file)
            self.kwn_std_df.drop_duplicates(inplace=True)
            self.kwn_std_df['korean'] = np.array(map(lambda x: x.replace(" ", "_"), self.kwn_std_df['korean'].values))
            #self.kwn_std_df['korean'] = np.array(map(lambda x: x.replace(".", ""), self.kwn_std_df['korean'].values))
            self.kwn_std_df['std_num'] = self.kwn_std_df['std_num'].map(lambda x: self.map_format_of_std_num(x))
            print("[KorLexAPI][load_synset_data] Loaded kwn_std.pkl !")

        #self.hypernym_list = json.load(open('../hypernym_list.json'))
        #self.hyponym_list = json.load(open('../hyponym_list.json'))
        self.kwn_synset_vocab = json.load(open('/home/ben/Documents/NLP/path2vec/KorLex_API/kwn_korean_synsets_vocab.json'))
        self.neighbor_dic = json.load(open('/home/ben/Documents/NLP/path2vec/KorLex_API/neighbor_list.json'))

    def check_only_space(self, string):
        if string.replace(" ", "") == "":
            return True
        else:
            return False

    def search_word(self, word:str, ontology=str):
        ret_json_list = []

        if 0 >= len(word):
            print("[KorLexAPI][search_word] ERR - Check input:", word)
            return ret_json_list

        if word not in self.seIdx_df["word"].values:
            print("[KorLexAPI][search_word] ERR - Not Existed SE Index Table:", word)
            return ret_json_list

        # Search hyponym nodes
        hyponym_idx_list = np.where(self.seIdx_df["word"].values == word)
        hyponym_obj_list = []
        for sIdx in hyponym_idx_list[0]:
            hyponym_obj_list.append(copy.deepcopy(self.seIdx_df.loc[sIdx]))

        # Make Result Json
        for target_obj in hyponym_obj_list:
            target_krx_json = self._make_result_json(target_obj=target_obj, ontology=ontology)
            ret_json_list.append(copy.deepcopy(target_krx_json))

        return ret_json_list

    def search_synset(self, synset:str, ontology:str):
        ret_json_list = []

        if 0 >= len(synset):
            print("[KorLexAPI][search_synset] ERR - Check input:", synset)
            return ret_json_list

        synset = int(synset)
        if synset not in self.seIdx_df["soff"].values:
            print("[KorLexAPI][search_synset] ERR - Not Existed SE Index Table:", synset)
            return ret_json_list

        # Search hyponym nodes
        hyponym_idx_list = np.where(self.seIdx_df["soff"].values == synset)
        hyponym_obj_list = []
        for sIdx in hyponym_idx_list[0]:
            hyponym_obj_list.append(copy.deepcopy(self.seIdx_df.loc[sIdx]))

        # Make Result Json
        for target_obj in hyponym_obj_list:
            target_krx_json = self._make_result_json(target_obj=target_obj, ontology=ontology)
            ret_json_list.append(copy.deepcopy(target_krx_json))

        return ret_json_list

    # WIKI
    def load_wiki_relation(self, wiki_rel_path:str):
        self.wiki_df = None

        if not os.path.exists(wiki_rel_path):
            print("[KorLexAPI][load_wiki_relation] ERR - Plz Check wiki_rel_path:", wiki_rel_path)
            return

        with open(wiki_rel_path, mode="r", encoding="cp949") as wiki_rel_file:
            word_list = []
            sysnet_list = []
            for line in wiki_rel_file.readlines():
                split_line = line.strip().split(",")
                sysnet = split_line[0]
                sysnet_list.append(sysnet)

                word = split_line[-1]
                word_list.append(word)
            self.wiki_df = pd.DataFrame((word_list, sysnet_list), index=["word", "synset"]).transpose()

    def search_wiki_word(self, word:str, ontology:str):
        ret_target_list = []
        ret_related_list = []

        if 0 >= len(word):
            print("[KorLexAPI][search_wiki_word] ERR - Word is NULL word:", word)
            return ret_target_list, ret_related_list
        if self.wiki_df is None:
            print("[KorLexAPI][search_wiki_word] ERR - self.wiki_df is None !")
            return ret_target_list, ret_related_list

        # Convert wiki word to synset num
        total_result_list = []
        target_wiki_rel_list = np.where(self.wiki_df["word"].values == word)
        for t_wiki_rel_idx in target_wiki_rel_list:
            for _, wiki_rel_item in self.wiki_df.loc[t_wiki_rel_idx].iterrows():
                wiki_rel_synset = wiki_rel_item["synset"]
                wiki_rel_result = self.search_synset(synset=wiki_rel_synset, ontology=ontology)
                if wiki_rel_result is not None:
                    total_result_list.extend(copy.deepcopy(wiki_rel_result))

        for result in total_result_list:
            if word == result[0].target.word:
                ret_target_list.extend(copy.deepcopy(result))
            else:
                ret_related_list.extend(copy.deepcopy(result))

        return ret_target_list, ret_related_list

    def check_df_size(self):
        print('kwn:', self.kwn_std_df.shape,len(set(self.kwn_std_df['soff'].values)))
        print('seIdx:', self.seIdx_df.shape, len(set(self.seIdx_df['soff'].values)))
        print('ssInfo:', self.ssInfo_df.shape, len(set(self.ssInfo_df['soff'].values)))
        print('reIdx:', self.reIdx_df.shape, len(set(self.reIdx_df['elem'].values)))

    def remain_word_in_krx(self):
        # divided word(vocab) to in_krx and out_krx
        f = open('../../new_korean_synsets_vocab.json')
        kor_vocab = json.load(f)
        f.close()
        in_krx_list = set()
        out_krx_list = set()
        for idx, obj in enumerate(kor_vocab):
            if idx%1000 == 0:
                print('going: ', idx , '/', len(kor_vocab))
                print('len of in and out: ', len(in_krx_list), len(out_krx_list))
            if self.check_word_is_in_krx(obj):
                in_krx_list.add((idx, obj))
            else:
                out_krx_list.add((idx, obj))
        print('len of in and out: ', len(in_krx_list), len(out_krx_list))

        new_in_krx_list = list(in_krx_list)
        new_out_krx_list = list(out_krx_list)

        #save file(with shoulder num)
        new_file_name = 'korean_synsets_vocab.json'
        with open(new_file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_in_krx_list, indent=2))

        new_file_name = 'not_in_korean_synsets_vocab.json'
        with open(new_file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_out_krx_list, indent=2))

    def map_format_of_std_num(self, std_num: str):
        if len(std_num) == 2:
            return std_num
        elif len(std_num) == 1:
            return '0'+std_num
        else:
            print('error', std_num)
            return std_num

    def make_new_vocab(self):
        '''self.kwn_std_df.iloc[8747]['korean'] = '공고라교양주의자.n.00'
                    self.kwn_std_df.iloc[80372]['korean'] = '22.n.00'''
        word_set = set()
        for index, data_row in self.kwn_std_df.iterrows():
            #only for noun
            #if data_row['ss_type']!='n':
            #    continue
            formatted_word = '.'.join([data_row['korean'], data_row['ss_type'], data_row['std_num']])
            word_set.add(formatted_word)
        print('len: ', len(word_set))
        file_name = 'all_kwn_korean_synsets_vocab.json'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(list(word_set), indent=2))

    def make_similarity_score(self):
        dir_path = '../../Korean_Korlex_dataset/korea_train/new_korean_shp.tsv.gz'
        df = pd.read_csv(dir_path, compression='gzip', names=['vocab1', 'vocab2', 'score'],
                         header=None, sep='\t', quotechar='"', encoding='utf-8', engine='python')
        err =0
        for idx, row in df.iterrows():
            try:
                row['new_score'] = self.new_path_similarity(row['vocab1'], row['vocab2'])
            except:
                row['new_score']=0
                print('errr')
                err +=1

            if idx % 1000 == 0:
                print(idx, '/', len(df))
        df.to_csv('new_shp.tsv.gz',
                  sep='\t',
                  header=False,
                  index=False,
                  compression="gzip")
        print('diff: ', sum(np.where(row['new_socre']!=row['score'])))

    def check_the_word(self, word):
        if word in self.kwn_std_df['korean'].values:
            return True
        else:
            return False

    def you_want_nogada(self, word):
        sibling_idx_list = np.where((self.kwn_std_df["ss_type"].values =='n') &
                                    (self.kwn_std_df["korean"].values == word))
        # empty
        if sibling_idx_list[0].size == 0:
            return []

        sibling_soff_set = set()
        for sIdx in sibling_idx_list[0]:
            temp_soff = self.kwn_std_df.loc[sIdx]['soff']
            temp_list = np.where((self.kwn_std_df["soff"].values == temp_soff) &
                                 (self.kwn_std_df["ss_type"].values == 'n'))[0]
            for soffIdx in temp_list:
                row = self.kwn_std_df.loc[soffIdx]
                sibling_soff_set.add(row['korean'] + '.' + row['ss_type'] + '.' + row['std_num'])

        return list(sibling_soff_set)

### TEST ###
if "__main__" == __name__:
    ssInfo_path = "./dic/korlex_ssInfo.pkl"
    seIdx_path = "./dic/korlex_seIdx.pkl"
    reIdx_path = "./dic/korlex_reIdx.pkl"
    kwn_std_path = "./dic/korlex_kwn_std.pkl"
    krx_json_api = KorLexAPI(ssInfo_path=ssInfo_path,
                             seIdx_path=seIdx_path,
                             reIdx_path=reIdx_path,
                             kwn_std_path=kwn_std_path)
    krx_json_api.load_synset_data()
    krx_json_api.make_new_vocab()
    #print(krx_json_api.check_the_word('파라_강'))
    #print(krx_json_api.path_similarity('삼촌.n.01', '이모.n.02'))

    '''for idx, row in krx_json_api.kwn_std_df.iterrows():
        if len(row['korean']) > 20:
            print(row['korean'])'''

    '''print(krx_json_api.kwn_std_df.head(3))
    print(krx_json_api.seIdx_df.head(3))
    print(krx_json_api.reIdx_df.head(3))
    print(krx_json_api.ssInfo_df.head(3))'''

    '''#check if there the word is in krx
    import json
    f = open('../../new_korean_synsets_vocab.json')
    kor_vocab = json.load(f)
    f.close()
    count=0
    new_json_list = []
    for idx, obj in enumerate(kor_vocab):
        if not krx_json_api.check_word_is_in_krx(obj):
            count += 1
            print(count,'/', idx, obj)
    print(count)'''

    '''start_time = time.time()
    test_search_synset = krx_json_api.search_word(word="개", ontology=ONTOLOGY.KORLEX.value)
    end_time = time.time()
    print("proc time:", end_time - start_time)
    for t_s in test_search_synset:
        print(t_s)
    exit()'''

    start_time = time.time()
    word = "주식.n.01"


    print(krx_json_api.eval_synset('배', 'n'))

    test = krx_json_api.synset('키보드.n.01')
    # print 에선 울다.v.03 형식, but 실제 객체는 -> Synset(text="울다", pos="v", sense_id="03")
    print(test.Synset)
    #print(test.check_word_is_in_krx("파라_강.n.00"))
    # print(krx_json_api.lemmas())
    print(test.hypernyms())
    print(test.member_holonyms())
    print(test.hyponyms())
    end_time = time.time()
    print("proc time:", end_time - start_time)

    #krx_json_api.make_similarity_score()

    '''# if you want to use wiki relation, write below methods
    wiki_rel_path = "./wiki/pwn2.0_krwiki.txt"
    krx_json_api.load_wiki_relation(wiki_rel_path=wiki_rel_path)

    start_time = time.time()
    target_result, related_result = krx_json_api.search_wiki_word(word="사과", ontology=ONTOLOGY.KORLEX.value)
    end_time = time.time()

    for t_r in target_result:
        print(t_r)
    print()
    for r_r in related_result:
        print(r_r)

    print("proc time:", end_time - start_time)'''
