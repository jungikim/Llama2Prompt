import stanza

class StanzaNER():
  @staticmethod
  def getTagSet(lang):
    if lang == 'en':
      return [
        'PERSON',
        'NORP',  # (Nationalities/religious/political group)
        'FAC',   # (Facility)
        'ORG',
        'GPE',   # (Countries/cities/states)
        'LOC',
        'PRODUCT',
        'EVENT',
        'WORK_OF_ART',
        'LAW',
        'LANGUAGE',
        'DATE',
        'TIME',
        'PERCENT',
        'MONEY',
        'QUANTITY',
        'ORDINAL',
        'CARDINAL',]    
    return []

  def __init__(self, lang='en', resources_dir='stanza_resources'):
    if resources_dir != None:
      import os
      os.environ["STANZA_RESOURCES_DIR"]=resources_dir
      self.stanzaNER = stanza.Pipeline(lang=lang,
                                       processors='tokenize,ner',
                                       verbose=False,
                                       dir=resources_dir,
                                       download_method=None,)
    else:
      # will attempt to download missing models
      self.stanzaNER = stanza.Pipeline(lang=lang,
                                       processors='tokenize,ner',
                                       verbose=False)

  def __call__(self, inputStr, tagSet=None):
    doc = self.stanzaNER(inputStr)
    # print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')
    retVal=[]
    for sent in doc.sentences:
      for ent in sent.ents:
        if tagSet is None or ent.type in tagSet:
          retVal.append(ent)
    return retVal

def _downloadmodels():
  # WMT 14-20 lang freq ( ls *.???? | sed "s#\.#   #" | cut -f 2 | sed "s#\(..\)#\1\t#" | tr "\t" "\n" | sort | uniq -c | sort -n -k 1 -r)
  # 93 en
  # 20 de
  # 15 cs
  # 14 ru
  # 10 fi
  #  8 zh
  #  6 tr
  #  6 fr
  #  2 ta
  #  2 ro
  #  2 ps
  #  2 pl
  #  2 lv
  #  2 lt
  #  2 km
  #  2 kk
  #  2 ja
  #  2 iu
  #  2 hi
  #  2 gu
  #  2 et
  notSupportedList = []
  for l in ['en', 'de', 'cs', 'ru', 'fi', 
            'zh', 'tr', 'fr',
            'ta', 'ro', 'ps', 'pl', 'lv', 'lt', 'km', 'kk', 'ja', 'iu', 'hi', 'gu', 'et']:
    try:
      stanza.Pipeline(lang=l, processors='tokenize,ner', dir='stanza_resources')
    except:
      print(f"Lang {l} is not supported by stanza")
      notSupportedList.append(l)
  print("Languages not supported by Stanza: %s" % (notSupportedList))
  # Languages not supported by Stanza: ['cs', 'ta', 'ro', 'ps', 'lv', 'lt', 'km', 'iu', 'hi', 'gu', 'et']



if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('run',          choices=['prepare', 'analyze',], help='')
  parser.add_argument('--lang',       default='en', help="")
  parser.add_argument('--input',      default=None, help="")
  args = parser.parse_args()

  if args.run == 'prepare':
    _downloadmodels()
  elif args.run == 'analyze':
    ner=StanzaNER(lang=args.lang)

    def _processInput(inputStr):
      entities = ner(inputStr)
      print(*[f'entity: {ent.text}\ttype: {ent.type}' for ent in entities], sep='\n')

    if args.input is not None:
      _processInput(args.input)
    else:
      while True:
        print('Enter: ', end='')
        try:
          inputStr = input()
        except:
          break
        _processInput(inputStr)
