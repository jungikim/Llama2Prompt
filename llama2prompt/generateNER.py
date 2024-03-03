from llama2prompt.LLaMa2NER import LLaMa2NER

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

  ner=LLaMa2NER(args.model_dir)
  doc = readBitext(args.inputF)
  nerF = open(args.inputF+'.ner', 'w')
  for (id, src, tgt) in doc:
    # print(f'{id}: \n\tsrc: {src}\n\t tgt: {tgt}')
    id, genre, lang, author, _ = id
    entities = ner('\n'.join(src))
    print(f'{id} {author} {genre} {lang}')
    nerF.write('\t'.join([ent.strip()+':::'+desc.strip() for (ent, desc) in entities])+'\n')
  nerF.close()

if __name__ == '__main__':
  main()