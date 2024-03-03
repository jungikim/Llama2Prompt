import os
import ctranslate2
import sentencepiece as spm

from llama2prompt.Util import Util

class LLaMa2MT():
  def __init__(self,
               model_dir,
               system_prompt='You are a %s-to-%s translator.',
               user_prompt=['Translate the following %s text into %s.\n%s: ', '\n%s:']):
    print("Loading the model...")
    self.generator = ctranslate2.Generator(model_dir, device="cpu", inter_threads=8, intra_threads=0)
    self.sp = spm.SentencePieceProcessor(os.path.join(model_dir, "tokenizer.model"))
    # self.context_length = 4096
    self.max_generation_length_factor = 1.5
    self.system_prompt = system_prompt
    self.user_prompt = user_prompt
    self.sampling_topp = 1.0
    self.sampling_topk = 20
    self.sampling_temperature = 0.00


  def __call__(self, inputStr, sourceLang, targetLang, system_prompt=None, user_prompt=None):
    dialog = []
    if system_prompt:
        dialog.append({"role": "system",
                       "content": system_prompt})
    elif self.system_prompt:
        dialog.append({"role": "system",
                       "content": self.system_prompt % (sourceLang, targetLang)})

    if user_prompt:
      dialog.append({"role": "user",
                     "content": user_prompt[0] + inputStr + (user_prompt[1])})
    else:
      dialog.append({"role": "user",
                     "content": (self.user_prompt[0] % (sourceLang, targetLang, sourceLang)) \
                                 + inputStr \
                                 + (self.user_prompt[1] % (targetLang))})

    prompt_tokens = Util.build_prompt(self.sp, dialog)
    step_results = self.generator.generate_tokens(
      prompt_tokens,
      max_length= int(self.max_generation_length_factor * len(prompt_tokens)),
      sampling_topp=self.sampling_topp,
      sampling_topk=self.sampling_topk,
      sampling_temperature=self.sampling_temperature,
    )
    output = Util.generate_words(self.sp, step_results)

    text_output = ''
    for word in output:
      if text_output:
        word = ' ' + word
      print(word, end='', flush=True)
      text_output += word
    print('')

    return text_output



if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--language',   default='en', help="")
  parser.add_argument('--input',      default=None, help="")
  parser.add_argument('--inputF',      default=None, help="")
  parser.add_argument('--model_dir',  default='llama2_resources/llama-2-7b-chat_hf_ct2_int8_float16/', help="")
  parser.add_argument('--sourceLang', required=True, type=str, help='full name of the language, e.g. German, Korean, Chinese')
  parser.add_argument('--targetLang', required=True, type=str, help='full name of the language, e.g. German, Korean, Chinese')

  args = parser.parse_args()

  mt=LLaMa2MT(args.model_dir)

  def _processInput(inputStr, sourceLang, targetLang):
    trans = mt(inputStr, sourceLang, targetLang)
    # print(*[f'entity: {ent.text}\ttype: {ent.type}' for ent in entities], sep='\n')
    print()
    print(trans)
    print()


  if args.input is not None:
    _processInput(args.input, args.sourceLang, args.targetLang)
  if args.inputF is not None:
    _processInput(open(args.inputF, 'r').read(), args.sourceLang, args.targetLang)
  else:
    while True:
      print('Enter: ', end='')
      try:
        inputStr = input()
      except:
        break
      _processInput(inputStr, args.sourceLang, args.targetLang)
