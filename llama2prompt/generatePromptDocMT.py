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

  doc = readBitext(args.inputF)

  mt = LLaMa2MT(args.model_dir)

  promptDocMtF = open(args.inputF+'.promptdocmt_docmt', 'w')
  promptSenMtF = open(args.inputF+'.promptdocmt_senmt', 'w')
  promptDocRefF = open(args.inputF+'.promptdocmt_docref', 'w')
  promptSenRefF = open(args.inputF+'.promptdocmt_senref', 'w')
  for (id, src, tgt) in doc:
    # print(f'{id}: \n\tsrc: {src}\n\t tgt: {tgt}')
    id, genre, lang, author, _ = id
    print(f'{id} {author} {genre} {lang}')

    #user_prompt = ['Provide only the line-by-line translation of the following text in %s:\n', '\nTranslation only: ']
    #user_prompt = ['Provide the %s translation of the following text line-by-line in a tabular format:\n', '\n| Original line | %s Translation |' % (args.targetLang)]

    system_prompt = 'You are a %s-to-%s translator.' % (args.sourceLang, args.targetLang) + \
                    ' Always output your answer in the target language. No pre-amble.'
    user_prompt = ['%s:\n' % (args.sourceLang),
                   '\n%s:\n' % (args.targetLang)]

    mtOutput = mt('\n'.join(src),
                  args.sourceLang, args.targetLang,
                  system_prompt=system_prompt, user_prompt=user_prompt).strip().rstrip()
    mtOutputs = mtOutput.split('\n')
    # mtOutput = Util._getEntriesFromTable(mtOutput, num_fields=2)
    # mtOutputs = [s[1] for s in mtOutput]
    # mtOutput = '\n'.join(mtOutputs)

    promptDocMtF.write(mtOutput.replace('\n', ' ').replace('\t', ' ')+'\n')
    promptDocMtF.flush()
    promptDocRefF.write(' '.join(tgt).strip().rstrip()+'\n')
    promptDocRefF.flush()

    if len(tgt) != len(mtOutputs):
      print(f'numbers of sentences in tgt and mt do not match: {len(tgt)}, {len(mtOutputs)}')
      print('\n'.join([str(idx)+' '+s for idx, s in enumerate(tgt)]))
      print('\n'.join([str(idx)+' '+s for idx, s in enumerate(mtOutputs)]))
      continue

    promptSenMtF.write('\n')
    promptSenRefF.write('\n')
    for idx, output in enumerate(mtOutputs):
      promptSenMtF.write(output+'\n')
      promptSenRefF.write(tgt[idx]+'\n')
    promptSenMtF.flush()
    promptSenRefF.flush()
  
  promptSenMtF.close()
  promptDocMtF.close()
  promptSenRefF.close()
  promptDocRefF.close()


if __name__ == '__main__':
  main()