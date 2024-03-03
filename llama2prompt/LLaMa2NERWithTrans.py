import os
import ctranslate2
import sentencepiece as spm

from llama2prompt.Util import Util

class LLaMa2NERWithTrans():
  def __init__(self,
               model_dir,
               targetLang,
               system_prompt=None,
               user_prompt='Provide the descriptions and the translations in %s of any ambiguous acronyms or named entities in the following text in a tabular format: '):
    print("Loading the model...")
    self.generator = ctranslate2.Generator(model_dir, device="cpu", inter_threads=8, intra_threads=0)
    self.sp = spm.SentencePieceProcessor(os.path.join(model_dir, "tokenizer.model"))
    self.context_length = 4096
    self.max_generation_length = 512
    self.max_prompt_length = self.context_length - self.max_generation_length
    self.system_prompt = system_prompt
    self.user_prompt = user_prompt % (targetLang)
    self.sampling_topp = 1.0
    self.sampling_topk = 20
    self.sampling_temperature = 0.00


  def __call__(self, inputStr):
    dialog = []
    if self.system_prompt:
        dialog.append({"role": "system", "content": self.system_prompt})
    dialog.append({"role": "user", "content": self.user_prompt + ' ' + inputStr + '\n| Acronym/Named Entity | Description | Translation |'})

    prompt_tokens = Util.build_prompt(self.sp, dialog)
    step_results = self.generator.generate_tokens(
      prompt_tokens,
      max_length=self.max_generation_length,
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

    return Util._getEntriesFromTable(text_output, num_fields=3)


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('run',          choices=['prepare', 'analyze',], help='')
  parser.add_argument('--language',   default='en', help="")
  parser.add_argument('--input',      default=None, help="")
  parser.add_argument('--inputF',      default=None, help="")
  parser.add_argument('--model_dir',  default='llama2_resources/llama-2-7b-chat_hf_ct2_int8_float16/', help="")
  parser.add_argument('--targetLang',   default=None, help="")

  args = parser.parse_args()

  if args.run == 'analyze':
    ner=LLaMa2NERWithTrans(args.model_dir, args.targetLang)

    def _processInput(inputStr):
      entities = ner(inputStr)
      # print(*[f'entity: {ent.text}\ttype: {ent.type}' for ent in entities], sep='\n')
      print()
      print('\n'.join([str(t) for t in entities]))


    if args.input is not None:
      _processInput(args.input)
    if args.inputF is not None:
      _processInput(open(args.inputF, 'r').read())
    else:
      while True:
        print('Enter: ', end='')
        try:
          inputStr = input()
        except:
          break
        _processInput(inputStr)
  else:
    print('Unknown mode: %s' % (args.run))