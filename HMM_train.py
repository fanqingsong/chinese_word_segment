#!/usr/bin/python
#-*-coding:utf-8

import sys
import math
import pdb

class WordSegmentTrainer:
    def __init__(self):
        self._state_M = 4
        self._word_N = 0

        self._state_transfer_count = {}
        self._state_emit_count = {}
        self._state_count = {}
        self._state_pi_count = {}
        self._word_set = set()
        self._state_list = ['B','M','E','S']
        self._line_num = -1

        self._corpus_file = "RenMinData.txt_utf8"
        self._prob_start = "prob_start.py"
        self._prob_emit = "prob_emit.py"
        self._prob_trans = "prob_trans.py"

        self._init_ds()

    def _init_ds(self):
        for state in self._state_list:
            self._state_transfer_count[state] = {}

            for state1 in self._state_list:
                self._state_transfer_count[state][state1] = 0.0

        for state in self._state_list:
            self._state_pi_count[state] = 0.0
            self._state_emit_count[state] = {}
            self._state_count[state] = 0

    def _get_states(self, input_str):
        outpout_str = []

        input_len = len(input_str)

        if input_len == 0:
            pass
        elif input_len == 1:
            outpout_str.append('S')
        elif len(input_str) == 2:
            outpout_str = ['B','E']
        else:
            M_num = len(input_str) -2
            M_list = ['M'] * M_num
            outpout_str.append('B')
            outpout_str.extend(M_list)
            outpout_str.append('S')

        return outpout_str

    def _output_prob_start(self):
        start_handler = file(self._prob_start, 'w')

        for key in self._state_pi_count:
            '''
            if Pi_dic[key] != 0:
                Pi_dic[key] = -1*math.log(Pi_dic[key] * 1.0 / line_num)
            else:
                Pi_dic[key] = 0
            '''
            self._state_pi_count[key] = self._state_pi_count[key] * 1.0 / self._line_num

        start_handler.write(self._state_pi_count.__str__())

        start_handler.close()

    def _output_prob_trans(self):
        trans_handler = file(self._prob_trans,'w')

        for src_state in self._state_transfer_count:
            src_state_count = self._state_count[src_state]
            dst_states_count = self._state_transfer_count[src_state]

            for one_dst_state in dst_states_count:
                '''
                if A_dic[key][key1] != 0:
                    A_dic[key][key1] = -1*math.log(A_dic[key][key1] / Count_dic[key])
                else:
                    A_dic[key][key1] = 0
                '''
                one_dst_state_count = dst_states_count[one_dst_state]

                self._state_transfer_count[src_state][one_dst_state] = one_dst_state_count / src_state_count

        trans_handler.write(self._state_transfer_count.__str__())

        trans_handler.close()

    def _output_prob_emit(self):
        emit_handler = file(self._prob_emit, 'w')

        for src_state in self._state_emit_count:
            src_state_count = self._state_count[src_state]
            dst_words_count = self._state_emit_count[src_state]

            for one_dst_word in dst_words_count:
                '''
                if B_dic[key][word] != 0:
                    B_dic[key][word] = -1*math.log(B_dic[key][word] / Count_dic[key])
                else:
                    B_dic[key][word] = 0
                '''
                one_dst_word_count = dst_words_count[one_dst_word]

                self._state_emit_count[src_state][one_dst_word] = one_dst_word_count / src_state_count

        emit_handler.write(self._state_emit_count.__str__())

        emit_handler.close()

    def _output_prob_matrixes(self):
        print("len(word_set) = %s " % (len(self._word_set)))

        self._output_prob_start()
        self._output_prob_trans()
        self._output_prob_emit()

    def _get_line_words(self, line):
        word_list = []
        for i in range(len(line)):
            if line[i] == " ":
                continue

            word_list.append(line[i])

        self._word_set = self._word_set | set(word_list)

        return word_list

    def _get_line_states(self, line):
        segments = line.split(" ")

        state_list = []
        for one_segment in segments:
            segment_states = self._get_states(one_segment)
            state_list.extend(segment_states)

        return state_list

    def _handle_one_line(self, line):
        line = line.strip()

        if not line:
            return

        line = line.decode("utf-8", "ignore")

        word_list = self._get_line_words(line)
        state_list = self._get_line_states(line)

        word_len = len(word_list)
        state_len = len(state_list)

        if word_len != state_len:
            print("exception on [line_num = %d][line = %s]" % (self._line_num, line.endoce("utf-8", 'ignore')))
            return

        for i in range(state_len):
            one_state = state_list[i]
            one_word = word_list[i]

            if i == 0:
                self._state_pi_count[one_state] += 1
                self._state_count[one_state] += 1
                continue

            prev_state = state_list[i - 1]

            self._state_transfer_count[prev_state][one_state] += 1
            self._state_count[one_state] += 1

            state_emit_count = self._state_emit_count[one_state]
            if not state_emit_count.has_key(one_word):
                state_emit_count[one_word] = 0.0
            else:
                state_emit_count[one_word] += 1

    def train(self):
        corpus_handler = file(self._corpus_file)

        for line in corpus_handler:
            self._line_num += 1

            if self._line_num % 10000 == 0:
                print(self._line_num)

            self._handle_one_line(line)

        corpus_handler.close()

        self._output_prob_matrixes()


if __name__ == "__main__":
    trainer = WordSegmentTrainer()
    trainer.train()
