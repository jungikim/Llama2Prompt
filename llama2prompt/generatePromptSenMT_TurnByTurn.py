import re

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
  parser.add_argument('--maxNumContext', type=int, default=3, help='')
  args = parser.parse_args()

  mt = LLaMa2MT(args.model_dir)

  doc = readBitext(args.inputF)

  promptDocMtF = open(args.inputF+'.promptsenmt-tbt%d_docmt' % (args.maxNumContext), 'w')
  promptSenMtF = open(args.inputF+'.promptsenmt-tbt%d_senmt' % (args.maxNumContext), 'w')
  promptDocRefF = open(args.inputF+'.promptsenmt-tbt%d_docref' % (args.maxNumContext), 'w')
  promptSenRefF = open(args.inputF+'.promptsenmt-tbt%d_senref' % (args.maxNumContext), 'w')
  for (id, src, tgt) in doc:
    # print(f'{id}: \n\tsrc: {src}\n\t tgt: {tgt}')
    id, genre, lang, author, _ = id
    print(f'{id} {author} {genre} {lang}')

    mtOutputs = []    
    system_prompt = 'You are a %s-to-%s translator.' % (args.sourceLang, args.targetLang) + \
                    ' Always output your answer in the target language. No pre-amble.'
    user_prompt = ['', '']

    for sIdx, s in enumerate(src):
      context = ''
      assert (sIdx == len(mtOutputs))
      for tIdx in range(len(mtOutputs)):
        if tIdx + args.maxNumContext < sIdx: continue
        context += '%s: ' % (args.sourceLang) + src[tIdx] + '\n' + \
                   '%s: ' % (args.targetLang) + mtOutputs[tIdx] + '\n'
      
      # context += '%s: ' % (args.sourceLang) + s.replace('\n', ' ') + '\n' + \
      #            '%s: ' % (args.targetLang)      
      context += 'Given these translations of the previous sentences, translate the following %s sentence into %s:' % (args.sourceLang, args.targetLang) + '\n' + \
                 s.replace('\n', ' ') + '\nTranslation: '

      print('system_prompt: %s' % (system_prompt))
      print('context: %s' % (context))
      print('user_prompt: %s' % (user_prompt))

      mtOutput = mt(context,
                    args.sourceLang, args.targetLang,
                    system_prompt=system_prompt, user_prompt=user_prompt).strip()

      SurePattern = re.compile('^Sure.+?:\s*?$')
      HerePattern = re.compile('^Here.+?:\s*?$')
      NotePattern = re.compile('^\(Note.+?\)$')
      NotePattern2 = re.compile('^Note: .+?$')
      starPattern = re.compile('^\* .+?$')
      srcLangPattern = re.compile('^%s: '%(args.sourceLang))
      iHopePattern1 = re.compile('I hope this helps! Let me know if you have any other questions.')
      iHopePattern2 = re.compile('I hope this helps! Let me know if you have any further questions.')

      LangPattern = re.compile('^%s:[\s$]*'%(args.targetLang))
      LangPattern2 = re.compile('^%s translation:[\s$]*'%(args.targetLang))
      LangPattern3 = re.compile('^%s:[\s$]*'%('Deutsch'))
      InLangPattern = re.compile('^In %s.+? translate.+?:'%(args.targetLang))
      transPattern = re.compile('^Translation: ')

      tmpLines = []
      for tmpLine in mtOutput.split('\n'):
        if re.match(SurePattern, tmpLine): continue
        if re.match(HerePattern, tmpLine): continue
        if re.match(NotePattern, tmpLine): continue
        if re.match(NotePattern2, tmpLine): continue
        if re.match(starPattern, tmpLine): continue
        if re.match(srcLangPattern, tmpLine): continue
        if re.match(iHopePattern1, tmpLine): continue
        if re.match(iHopePattern2, tmpLine): continue
        if tmpLine.find(s.replace('\n', ' ')) >= 0: continue
        tmpLine = re.sub(LangPattern, '', tmpLine)
        tmpLine = re.sub(LangPattern2, '', tmpLine)
        tmpLine = re.sub(LangPattern3, '', tmpLine)
        tmpLine = re.sub(InLangPattern, '', tmpLine)
        tmpLine = re.sub(transPattern, '', tmpLine)
        tmpLine=tmpLine.strip()
        if len(tmpLine)==0: continue
        tmpLines.append(tmpLine.strip())        
      mtOutput = ' '.join(tmpLines)
      print('MT: %s' % (mtOutput))
      print()

      mtOutputs.append(mtOutput)

    promptDocMtF.write(' '.join(mtOutputs)+'\n')
    promptDocMtF.flush()
    promptDocRefF.write(' '.join(tgt).strip()+'\n')
    promptDocRefF.flush()

    promptSenMtF.write('\n')
    promptSenRefF.write('\n')
    for idx, output in enumerate(mtOutputs):
      promptSenMtF.write(output+'\n')
      promptSenRefF.write(tgt[idx].strip()+'\n')
    promptSenMtF.flush()
    promptSenRefF.flush()

  promptSenMtF.close()
  promptDocMtF.close()
  promptSenRefF.close()
  promptDocRefF.close()

if __name__ == '__main__':
  main()