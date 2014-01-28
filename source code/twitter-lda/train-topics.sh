./../bin/mallet train-topics --input twitter.mallet --output-state out-state.gz --num-topics 5 \
--output-model out-model.txt --output-doc-topics out-doc-topics.txt \
--output-topic-keys out-top-keys.txt --topic-word-weights-file word-weights.txt \
--word-topic-counts-file topic-counts.txt --xml-topic-report topic-report.xml \
--xml-topic-phrase-report topic-phrase-rep.xml --inferencer-filename inferencer.txt