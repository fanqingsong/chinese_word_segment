#!/usr/bin/python
#-*-coding:utf-8
import os
import sys
import pdb

class WordSegmentApp:
    def __init__(self):
        self._prob_start = "prob_start.py"
        self._prob_emit = "prob_emit.py"
        self._prob_trans = "prob_trans.py"
        self._state_list = ['B', 'M', 'E', 'S']

        self._load_models()

    def _load_model(self, model_file):
        model_handler = file(model_file, 'rb')

        return eval(model_handler.read())

    def _load_models(self):
        self._prob_start_data = self._load_model(self._prob_start)
        self._prob_trans_data = self._load_model(self._prob_trans)
        self._prob_emit_data = self._load_model(self._prob_emit)

    def viterbi(self, obs):
        V = [{}] #tabular
        path = {}

        state_list = self._state_list
        prob_start = self._prob_start_data
        prob_trans = self._prob_trans_data
        prob_emit = self._prob_emit_data

        # init first word gain
        for y in state_list: #init
            V[0][y] = prob_start[y] * prob_emit[y].get(obs[0],0)
            path[y] = [y]

        # dynamic program to calc every state gain for the rest words
        for t in range(1,len(obs)):
            V.append({})
            newpath = {}

            for y in state_list:
                (prob, state) = max([(V[t-1][y0] * prob_trans[y0].get(y,) * prob_emit[y].get(obs[t],0) ,y0) for y0 in state_list if V[t-1][y0]>0])
                V[t][y] = prob
                newpath[y] = path[state] + [y]

            path = newpath

        (prob, state) = max([(V[len(obs) - 1][y], y) for y in state_list])
        return (prob, path[state])

    def cut(self, sentence):
        #pdb.set_trace()
        prob, pos_list =  self.viterbi(sentence)
        return (prob,pos_list)


if __name__ == "__main__":
    app = WordSegmentApp()

    test_str = u"长春市长春节讲话。"
    prob,pos_list = app.cut(test_str)
    print(test_str)
    print(pos_list)

    test_str = u"他说的确实在理."
    prob,pos_list = app.cut(test_str)
    print(test_str)
    print(pos_list)

    test_str = u"毛主席万岁。"
    prob,pos_list = app.cut(test_str)
    print(test_str)
    print(pos_list)

    test_str = u"我有一台电脑。"
    prob,pos_list = app.cut(test_str)
    print(test_str)
    print(pos_list)

