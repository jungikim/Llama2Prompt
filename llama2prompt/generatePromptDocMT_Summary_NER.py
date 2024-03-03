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


def readSummary(inputF):
  retVal=[]
  inF=open(inputF, 'r')
  for line in inF:
    retVal.append(line.strip().rstrip().replace('\n', ' ').replace('\t', ' '))
  inF.close()
  return retVal


def readNER(inputF):
  retVal=[]
  inF=open(inputF, 'r')
  for line in inF:
    line = line.strip().rstrip()
    NEs = []
    header=None
    cols = line.split('\t')
    for col in cols:
      if len(col) == 0:
        continue
      fields = col.split(':::')
      if len(fields)==2:
        NEs.append('| ' + fields[0] + ' | ' + fields[1] + ' |')
        if header is None:
          header = '| Entity/Acronym | Description |'
      elif len(fields)==3:
        NEs.append('| ' + fields[0] + ' | ' + fields[1] + ' | ' + fields[2] + ' |')
        if header is None:
          header = '| Entity/Acronym | Description | Translation |'
      else:
        raise IndexError(f'Unrecognized number of fields in NER file: %s "%s"' % (inputF, line))
    if len(NEs) > 0:
      NEs.insert(0, header)
    retVal.append(NEs)
  inF.close()
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
  sum = readSummary(args.inputF+'.summary')
  ner = readNER(args.inputF+'.ner_w_trans_' + args.targetLang)

  mt = LLaMa2MT(args.model_dir)

  promptDocMtF = open(args.inputF+'.promptdocmt-sum-ner_docmt', 'w')
  promptSenMtF = open(args.inputF+'.promptdocmt-sum-ner_senmt', 'w')
  promptDocRefF = open(args.inputF+'.promptdocmt-sum-ner_docref', 'w')
  promptSenRefF = open(args.inputF+'.promptdocmt-sum-ner_senref', 'w')
  for idx, (id, src, tgt) in enumerate(doc):
    # print(f'{id}: \n\tsrc: {src}\n\t tgt: {tgt}')
    id, genre, lang, author, _ = id
    print(f'{id} {author} {genre} {lang}')

    system_prompt = 'You are a %s-to-%s translator.' % (args.sourceLang, args.targetLang)

    # user_prompt = ['', '\n']
    # user_prompt = ['', '\n| Original line | %s Translation |' % (args.targetLang)]

    if len(sum[idx]) > 0:
      # user_prompt[0] += sum[idx].replace('The text describes ', 'The following article describes ', 1) + '\n'
      system_prompt += '\nYou are given a text that ' + sum[idx].replace('The text describes ', 'describes ', 1) + '\n'
    if len(ner[idx]) > 0:
      # user_prompt[0] += 'The article contains these entities and acronyms: ' + '\n' + '\n'.join(ner[idx]) + '\n'
      system_prompt += 'The text contains these entities and acronyms: ' + '\n' + '\n'.join(ner[idx]) + '\n'
    system_prompt += 'Always output your answer in the target language. No pre-amble.'

    # if len(user_prompt[0]) > 0:
    #   # user_prompt[0] += 'With these information, provide only the line-by-line translation of the following text in %s:\n'
    #   user_prompt[0] += 'With these information, provide the %s translation of the following text line-by-line in a tabular format:\n'
    # else:
    #   # user_prompt[0] += 'Provide only the line-by-line translation of the following text in %s:\n'
    #   user_prompt[0] += 'Provide the %s translation of the following sentence in a tabular format:\n'

    user_prompt = ['%s:\n' % (args.sourceLang),
                   '\n%s:\n' % (args.targetLang)]

    print(system_prompt)
    print(user_prompt)

    mtOutput = mt('\n'.join(src),
                  args.sourceLang, args.targetLang,
                  system_prompt=system_prompt, user_prompt=user_prompt,
                  ).strip().rstrip()
    mtOutputs = mtOutput.split('\n')
    # mtOutput = Util._getEntriesFromTable(mtOutput, num_fields=2)
    # mtOutputs = [s[1] for s in mtOutput]
    # mtOutput = '\n'.join(mtOutputs)

    promptDocMtF.write(mtOutput.replace('\n', ' ').replace('\t', ' ')+'\n')
    promptDocMtF.flush()
    promptDocRefF.write(' '.join(tgt).strip().rstrip()+'\n')
    promptDocRefF.flush()

    if len(src) != len(mtOutputs):
      print(f'numbers of sentences in src and mt do not match: {len(src)}, {len(mtOutputs)}')
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