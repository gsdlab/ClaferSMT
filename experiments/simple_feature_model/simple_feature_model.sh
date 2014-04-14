LearnerZ3  \
    --numinstances -1 \
    --testset 3 \
    --learningiterations 7 \
    --cores 4  \
    --experimentnumsplits 4 8 12 16 \
    --parametersfile simple_feature_model.parameters \
    --generatorfile simple_feature_model.cfr \
    --formatter simple_feature_model_formatter.py \
    --heuristics simple_feature_model.big.heuristics \
    --outputdirectory ../runs/simple_feature_model/ \

