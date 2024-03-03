#PYTHONPATH=. python3 llama2prompt/generatePromptSenMT_Summary_NER.py \
#--inputF wmt/test_wmt20_docsep.ende_first10 \
#--sourceLang English \
#--targetLang German \
#--model_dir llama2_resources/llama-2-13b-chat_hf_ct2_float16/ \
#> wmt/test_wmt20_docsep.ende_first10.generatePromptSenMT_Summary_NER_13b_float16.log 2>&1 &&
#mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senmt_13b_float16 &&
#mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senref wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senref_13b_float16 &&
#mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docmt_13b_float16 &&
#mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docref wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docref_13b_float16 ; 

PYTHONPATH=. python3 llama2prompt/generatePromptSenMT_Summary_NER.py \
--inputF wmt/test_wmt20_docsep.ende_first10 \
--sourceLang English \
--targetLang German \
--model_dir llama2_resources/llama-2-13b-chat_hf_ct2_int8_float16/ \
> wmt/test_wmt20_docsep.ende_first10.generatePromptSenMT_Summary_NER_13b_int8_float16.log 2>&1 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senmt_13b_int8_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senref wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senref_13b_int8_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docmt_13b_int8_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docref wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docref_13b_int8_float16 ; 

PYTHONPATH=. python3 llama2prompt/generatePromptSenMT_Summary_NER.py \
--inputF wmt/test_wmt20_docsep.ende_first10 \
--sourceLang English \
--targetLang German \
--model_dir llama2_resources/llama-2-7b-chat_hf_ct2_float16/ \
> wmt/test_wmt20_docsep.ende_first10.generatePromptSenMT_Summary_NER_7b_float16.log 2>&1 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senmt_7b_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senref wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senref_7b_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docmt_7b_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docref wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docref_7b_float16 ;

PYTHONPATH=. python3 llama2prompt/generatePromptSenMT_Summary_NER.py \
--inputF wmt/test_wmt20_docsep.ende_first10 \
--sourceLang English \
--targetLang German \
--model_dir llama2_resources/llama-2-7b-chat_hf_ct2_int8_float16/ \
> wmt/test_wmt20_docsep.ende_first10.generatePromptSenMT_Summary_NER_7b_int8_float16.log 2>&1 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senmt_7b_int8_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senref wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_senref_7b_int8_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docmt_7b_int8_float16 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docref wmt/test_wmt20_docsep.ende_first10.promptsenmt-sum-ner_docref_7b_int8_float16 ;


