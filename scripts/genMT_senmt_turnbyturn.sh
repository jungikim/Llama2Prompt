for ncxt in 3 ; do
for s in 13b ; do # 7b
for q in int8_float16 ; do # float16

PYTHONPATH=. python3 llama2prompt/generatePromptSenMT_TurnByTurn.py \
--inputF wmt/test_wmt20_docsep.ende_first10 \
--sourceLang English \
--targetLang German \
--maxNumContext ${ncxt} \
--model_dir llama2_resources/llama-2-${s}-chat_hf_ct2_${q}/ \
> wmt/test_wmt20_docsep.ende_first10.generatePromptSenMT_TurnByTurn2_${ncxt}_${s}_${q}.log 2>&1 &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-tbt${ncxt}_senmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-tbt2_${ncxt}_senmt_${s}_${q} &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-tbt${ncxt}_senref wmt/test_wmt20_docsep.ende_first10.promptsenmt-tbt2_${ncxt}_senref_${s}_${q} &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-tbt${ncxt}_docmt  wmt/test_wmt20_docsep.ende_first10.promptsenmt-tbt2_${ncxt}_docmt_${s}_${q} &&
mv wmt/test_wmt20_docsep.ende_first10.promptsenmt-tbt${ncxt}_docref wmt/test_wmt20_docsep.ende_first10.promptsenmt-tbt2_${ncxt}_docref_${s}_${q} ;

done
done
done
