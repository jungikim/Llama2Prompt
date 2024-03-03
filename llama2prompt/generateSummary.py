from llama2prompt.LLaMa2Summary import LLaMa2Summary

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
  args = parser.parse_args()

  sum=LLaMa2Summary(args.model_dir)
  doc = readBitext(args.inputF)
  summaryF = open(args.inputF+'.summary', 'w')
  for (id, src, tgt) in doc:
    # print(f'{id}: \n\tsrc: {src}\n\t tgt: {tgt}')
    id, genre, lang, author, _ = id
    summary = sum('\n'.join(src))
    print(f'{id} {author} {genre} {lang}')
    summaryF.write(summary+'\n')
    summaryF.flush()
  summaryF.close()

if __name__ == '__main__':
  main()