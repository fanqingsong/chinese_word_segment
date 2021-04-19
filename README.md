
# implement chinese words segmentation with HMM model

# model training
python HMM_train.py

* RenMinData.RenMinData_utf8 corpus from People Daily with words segmentation.

Then three probability configurations are produced.

* prob_start.py -- initial state probability vector
* prob_trans.py -- transfer probability matrix between all states
* prob_emit.py -- watched probability matrix for every state

# model testing
python HMM_app.py

#reference
* viterbi ：http://zh.wikipedia.org/wiki/%E7%BB%B4%E7%89%B9%E6%AF%94%E7%AE%97%E6%B3%95
* https://github.com/fxsjy/finalseg
