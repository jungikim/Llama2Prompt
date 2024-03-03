PYTHONPATH=. python3 llama2prompt/generatePromptSenMT.py             --inputF wmt/test_wmt20_docsep.ende --targetLang German > wmt/test_wmt20_docsep.ende.generatePromptSenMT_German.log 2>&1 &
PYTHONPATH=. python3 llama2prompt/generatePromptDocMT.py             --inputF wmt/test_wmt20_docsep.ende --targetLang German > wmt/test_wmt20_docsep.ende.generatePromptDocMT_German.log 2>&1 &
PYTHONPATH=. python3 llama2prompt/generatePromptDocMT_Summary_NER.py --inputF wmt/test_wmt20_docsep.ende --targetLang German > wmt/test_wmt20_docsep.ende.generatePromptDocMT_Summary_NER_German.log 2>&1 &

PYTHONPATH=. python3 llama2prompt/generatePromptSenMT.py             --model_dir llama2_resources/llama-2-7b_hf_ct2_int8_float16/ --inputF wmt/test_wmt20_docsep.ende --targetLang German > wmt/test_wmt20_docsep.ende.generatePromptSenMT_German.log 2>&1 &
PYTHONPATH=. python3 llama2prompt/generatePromptDocMT.py             --model_dir llama2_resources/llama-2-7b_hf_ct2_int8_float16/ --inputF wmt/test_wmt20_docsep.ende --targetLang German > wmt/test_wmt20_docsep.ende.generatePromptDocMT_German.log 2>&1 &
PYTHONPATH=. python3 llama2prompt/generatePromptDocMT_Summary_NER.py --model_dir llama2_resources/llama-2-7b_hf_ct2_int8_float16/ --inputF wmt/test_wmt20_docsep.ende --targetLang German > wmt/test_wmt20_docsep.ende.generatePromptDocMT_Summary_NER_German.log 2>&1 &


PYTHONPATH=. python3 llama2prompt/generatePromptSenMT.py \
--inputF wmt/test_wmt20_docsep.ende_first10 \
--sourceLang English \
--targetLang German \
> wmt/test_wmt20_docsep.ende_first10.generatePromptSenMT.log 2>&1 &

PYTHONPATH=. python3 llama2prompt/generatePromptDocMT.py \
--inputF wmt/test_wmt20_docsep.ende_first10 \
--sourceLang English \
--targetLang German \
> wmt/test_wmt20_docsep.ende_first10.generatePromptDocMT.log 2>&1 &

PYTHONPATH=. python3 llama2prompt/generatePromptDocMT_Summary_NER.py \
--inputF wmt/test_wmt20_docsep.ende_first10 \
--sourceLang English \
--targetLang German \
> wmt/test_wmt20_docsep.ende_first10.generatePromptDocMT_Summary_NER.log 2>&1 &
