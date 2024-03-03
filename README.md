
# Various Llama2 prompts

## Prompt-based Document Machine Translation
### Goal
We want to create and provide a document translation task to an LLM with a prompt with general information about the job that may be also given to human translators.

The translation process could also mimick how a team of human translators function.


### Process 1: first translation
We want to create useful prompt for translation, utilizing the information about: 
 - the author
   - who wrote this? where is it located?
   - "The following is a news article from the Telegraph in UK written in English."

 - general summary
   - subject, intent, 
   - "The article is about the education system in the UK."

 - the entities mentioned in the text and their relations
   - names of people, location and organization, and acronyms can sometimes be ambiguous (ACL, )
   - "GCSE: The General Certificate of Secondary Education is an academic qualification in a range of particular subjects, taken in England, Wales, and Northern Ireland."
   - "Ofqual: The Office of Qualifications and Examinations Regulation (Ofqual) regulates qualifications, examinations and assessments in England. Michael Gove is the Education Secretary in UK."
 
 - terminology translation candidates (dictionary, generic and/or domain-specific)
   -

 - expertise required to translate the text
   - 

 - the style, genre of the input and the target text
   - 

 - collective knowledge (TM, terminology) for consistent translation
   - 
 
 - draft translation?


### Process 2: iterative fine-tune (stabilize) step

 - Make sure that translations are consistent and confined by the global constraints
 
 - Global constraints:
   - terminology, ACRONYMS
   - way to address person: Mr./Dr., he/him, ...

 - This would be also useful if a document is split into subsections when being translated.



### preliminary test - one document from WMT 2014 ENDE

#### SRC
```
Schools urged to focus more on maths, spelling and grammar
English literature courses will require pupils to study at least one Shakespeare play, a 19th century novel, Romantic poetry and contemporary British fiction from 1914 onwards.
The exam will also feature "unseen texts" to encourage wider reading;
A combined English literature and language course will be scrapped.
From 2015, pupils will be required to take a standalone GCSE in language, with strong incentives to choose English literature as a separate qualification.
The Department for Education is due to release the new syllabuses in English and maths tomorrow - the first subjects to undergo a radical overhaul.
It will make changes in other core subjects next year.
In a separate move, Ofqual, the exams regulator, will unveil a shake-up of the structure of GCSEs, with a new grading system and less coursework.
Speaking in the summer, Michael Gove, the Education Secretary, said there was a "widespread consensus that we need to reform our examination system to restore public confidence," insisting GCSEs would be "more challenging, more ambitious and more rigorous."
Studies show that English schools devote less time to maths - 116 hours a year or three hours a week during term time - than in most countries.
By comparison, Australian schools provide an average of 143 hours a year and pupils do around 138 hours in Singapore.
While there will be no formal requirement to devote more of the timetable to maths, Coalition sources said the extensive maths GCSE - combined with more weighting for the subject in league tables - was likely to encourage schools to provide extra teaching.
The syllabus will place a greater focus on "real world problems," including financial mathematics. 
```

#### Reference
```
Schulen werden zu größerem Fokus auf Mathematik, Rechtschreibung und Grammatik angehalten
In Kursen zu englischer Literatur müssen Schüler künftig mindestens ein Stück von Shakespeare, einen Roman des 19. Jahrhunderts, romantische Lyrik und zeitgenössische britische Romane ab 1914 behandeln.
In die Prüfung finden auch „ungesehene Texte" Eingang, um zu breiterem Lesen anzuregen.
Der kombinierte Kurs aus englischer Literatur und Sprache wird abgeschafft.
Ab 2015 müssen Schüler eine eigenständige GCSE-Prüfung für Sprache ablegen, wobei es starke Anreize dafür gibt, englische Literatur als separate Qualifikation zu wählen.
Das Bildungsministerium wird morgen die neuen Lehrpläne für Englisch und Mathematik veröffentlichen – die ersten Fächer, die radikal umgestaltet wurden.
Andere Kernfächer werden nächstes Jahr geändert.
In einer separaten Initiative wird Ofqual, die Aufsichtsbehörde für Prüfungen, eine Neuorganisation der GCSE-Strukturen bekannt geben, einschließlich eines neuen Benotungssystems und weniger Kursarbeit.
In einer Rede im Sommer sagte Bildungsminister Michael Gove, dass es einen „breiten Konsens gibt, dass wir unser Prüfungssystem reformieren müssen, um das öffentliche Vertrauen wiederherzustellen", wobei er betonte, die GCSEs würden „herausfordernder, ambitionierter und strenger" werden.
Studien zeigen, dass in englischen Schulen weniger Zeit für Mathematik aufgewendet wird – 116 Stunden pro Jahr oder drei Stunden wöchentlich pro Schuljahr – als in den meisten anderen Ländern.
Demgegenüber unterrichten australische Schulen durchschnittlich 143 Stunden jährlich und Schüler in Singapur erhalten 138 Stunden.
Zwar wird es keine formelle Anforderung geben, im Stundenplan mehr Zeit für Mathematik vorzusehen, doch aus Koalitionskreisen heißt es, die umfassende Matheprüfung – kombiniert mit einer stärkeren Gewichtung des Fachs in Ranglisten – werde Schulen vermutlich dazu ermutigen, mehr Stunden anzusetzen.
Im Lehrplan wird mehr Augenmerk auf „Probleme aus dem richtigen Leben" gelegt, einschließlich Finanzmathematik.
```


#### Prompt (baseline)

```Translate this English news article into German: ""```

#### Prompt (proposed; prepared by hand)

```The following is a news article from the Telegraph in UK written in English. The article is about the education system in the UK.  GCSE: The General Certificate of Secondary Education is an academic qualification in a range of particular subjects, taken in England, Wales, and Northern Ireland. Ofqual: The Office of Qualifications and Examinations Regulation (Ofqual) regulates qualifications, examinations and assessments in England. Michael Gove is the Education Secretary in UK. With these information, translate this article into German: ""```

#### BLEU / chrF2 

| Baseline | Proposed | Google |
| -------- | -------- | ------ |
| 28.3 / 62.2 | 31.6 / 63.2  | 31.2 / 63.1 |


### Approach (WIP; brainstorming)

#### It may be possible to identify useful information in the metadata
    - WMT
      - docid: url . serialnum (salzburg.com.254713, handelsblatt.com.267929, ...)
      - genre: News

#### To identify automatically:
 - person names, location, organization
 - ACRONYM detection
 - topic / style
 
#### To provide in the prompt:
 - author
 - genre, style, domain, summary
 - list of NEs, acronyms (preferred way of referring to the entities)
   - disambiguated if multiple candidates exist
 - domain-specific terminology (e.g. dictionary definition/translation in the target language)
 - customer-specific requests
