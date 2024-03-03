from llama2prompt.Util import Util
from llama2prompt.LLaMa2MT import LLaMa2MT

def readBitext(inputF):
  retVal=[]
  bitextF = open(inputF, 'r')
  idF = open(inputF+'.id', 'r')
  bitextF.readline()
  id = idF.readline()
  while id:
    id = id.strip().split('\t')
    src, tgt = [], []
    for line in bitextF:
      line = line.strip()
      if len(line)==0:
        break
      toks = line.split('\t')
      src.append(toks[0])
      tgt.append(toks[1])
    retVal.append((id, src, tgt))
    id = idF.readline()  
  return retVal


def main():
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--inputF', default=None, help="")
  parser.add_argument('--model_dir',  default='llama2_resources/llama-2-7b-chat_hf_ct2_int8_float16/', help="")
  parser.add_argument('--sourceLang', required=True, help='')
  parser.add_argument('--targetLang', required=True, help='')
  args = parser.parse_args()

  mt = LLaMa2MT(args.model_dir)

  doc = readBitext(args.inputF)

  promptDocMtF = open(args.inputF+'.promptsenmt_docmt', 'w')
  promptSenMtF = open(args.inputF+'.promptsenmt_senmt', 'w')
  promptDocRefF = open(args.inputF+'.promptsenmt_docref', 'w')
  promptSenRefF = open(args.inputF+'.promptsenmt_senref', 'w')
  for (id, src, tgt) in doc:
    # print(f'{id}: \n\tsrc: {src}\n\t tgt: {tgt}')
    id, genre, lang, author, _ = id
    print(f'{id} {author} {genre} {lang}')

    mtOutputs = []
    # user_prompt = ['Provide only the translation of the following sentence in %s:\n', '\n']
    # user_prompt = ['Provide the %s translation of the following sentence in a tabular format:\n', '\n| original sentence | %s Translation |' % (args.targetLang)]

    system_prompt = 'You are a %s-to-%s translator.' % (args.sourceLang, args.targetLang) + \
                    ' Always output your answer in the target language. No pre-amble.'
    user_prompt = ['%s: ' % (args.sourceLang),
                   '\n%s:' % (args.targetLang)]

    for s in src:
      mtOutput = mt(s,
                    args.sourceLang, args.targetLang,
                    system_prompt=system_prompt, user_prompt=user_prompt).strip().rstrip()
      # mtOutput = Util._getEntriesFromTable(mtOutput, num_fields=2)
      # if len(mtOutput) > 0:
      #   mtOutput = mtOutput[0][-1].replace('\n', ' ').replace('\t', ' ')
      # else:
      #   mtOutput = ''
      mtOutputs.append(mtOutput)

    promptDocMtF.write(' '.join(mtOutputs)+'\n')
    promptDocMtF.flush()
    promptDocRefF.write(' '.join(tgt).strip().rstrip()+'\n')
    promptDocRefF.flush()

    for idx, output in enumerate(mtOutputs):
      promptSenMtF.write(output+'\n')
      promptSenRefF.write(tgt[idx].strip().rstrip()+'\n')
    promptSenMtF.flush()
    promptSenRefF.flush()

  promptSenMtF.close()
  promptDocMtF.close()
  promptSenRefF.close()
  promptDocRefF.close()

if __name__ == '__main__':
  main()