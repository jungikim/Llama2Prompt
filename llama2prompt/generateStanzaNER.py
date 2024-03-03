from llama2prompt.StanzaNER import StanzaNER

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
  parser.add_argument('--inputF', default=None, help='')
  parser.add_argument('--lang',   default='en', help='')
  args = parser.parse_args()

  ner=StanzaNER(args.lang)
  entitiesToSkip=set(['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL',
                      'NEM', 'NETI',
                      'TIME', 'NUM',
                      'PERCENTAGE',
                      'date', 'time',
                      'DTM', 'MEA',])

  doc = readBitext(args.inputF)
  nerF = open(args.inputF+'.stanzaner', 'w')
  for (id, src, tgt) in doc:
    # print(f'{id}: \n\tsrc: {src}\n\t tgt: {tgt}')
    id, genre, lang, author, _ = id
    entities = ner('\n'.join(src))
    seen={}
    uniq = []
    for ent in entities:
      if ent.type in entitiesToSkip:
        continue
      entStr = ent.text.strip().replace('\n',' ').replace('\t',' ')+':::'+ent.type.strip()
      if entStr in seen:
        continue
      uniq.append(entStr)
      seen[entStr]=''

    print(f'{id} {author} {genre} {lang}', flush=True)
    nerF.write('\t'.join([ent for ent in uniq])+'\n')
    nerF.flush()
  nerF.close()

if __name__ == '__main__':
  main()