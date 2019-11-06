'''

Converting scientific articles from xml file for elibrary.ru to xml for https://doaj.org (DOAJ Native XML)
russian metadata are dropped, only english are used
'''

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import re


# Этап 1 - создаем файл с записями, в которых прописаны одинаковые для всех элементы
tree2 = ET.parse('issue_unicode389.xml')
root2 = tree2.getroot()

recs = len(root2.findall("issue/articles/article"))
print(recs)

'''
root = ET.Element("root")
root.set('version', '1.0')
root.set('encoding', 'UTF-8')
'''


records = Element('records')
for i in range(recs):
    record = SubElement(records, 'record')
    language = SubElement(record, 'language')
    language.text = 'rus'
    publisher = SubElement(record, 'publisher')
    publisher.text = 'Krylov State Research Centre'
    journalTitle = SubElement(record, 'journalTitle')
    journalTitle.text = 'Transactions of the Krylov State Research Centre'
    issn = SubElement(record, 'issn')
    issn.text = '2542-2324'
    eissn = SubElement(record, 'eissn')
    eissn.text = '2618-8244'
    publicationDate = SubElement(record, 'publicationDate')
    publicationDate.text = '2019-08-30'
    volume = SubElement(record, 'volume')
    volume.text = '389'
    issue = SubElement(record, 'issue')
    issue.text = '3'





tree = ET.ElementTree(records)
doajfile = "doaj389.xml"
tree.write(doajfile)

# Этап 2 - Читаем исходный файл и переносим отдельные элементы в новую структуру
tree = ET.parse(doajfile)
root = tree.getroot()

i = 0
captions = []
abstracts = []
dois = []
startpages = []
endpages = []
authors = []
surnames = []
initials = []
orgnames =[]
keys_all=[]



for parent2 in root2.findall("issue/articles/article/artTitles"):

    for artTitle in parent2.findall("artTitle"):
        # print(artTitle.text)
        captions.append(artTitle.text)

for parent2 in root2.findall("issue/articles/article/abstracts"):

    for abstract in parent2.findall("abstract"):
        # print(artTitle.text)
        abstracts.append(abstract.text)

for parent2 in root2.findall("issue/articles/article"):

    for pages in parent2.findall("pages"):
        startpage, endpage = pages.text.split('-')
        startpages.append(startpage)
        endpages.append(endpage)

for parent2 in root2.findall("issue/articles/article/codes"):

    for doi in parent2.findall("doi"):
        dois.append(doi.text)



art = 0
for parent2 in root2.findall("issue/articles/article/authors"):
    auth = 0
    for author2 in parent2.findall("author"):

        for individInfo in author2.findall("individInfo"):

            auth_full = ''

            for initial in individInfo.findall("initials"):

                if auth%2 == 1:
                    #initials.append(str(art) + '-' + str(auth) + '-'+ initial.text)
                    auth_full =(str(art) + '-' + str(int((auth-1)/2)) + '-'+ initial.text)
                    #print(initial.text)

            for surname in individInfo.findall("surname"):

                if auth%2 == 1:
                    #surnames.append(str(art) + '-' + str(auth) + '-'+ surname.text)
                    auth_full += ' '+ surname.text
                    #print(surname.text)

            for orgName in individInfo.findall("orgName"):

                if auth%2 == 1:
                    #surnames.append(str(art) + '-' + str(auth) + '-'+ surname.text)
                    auth_full += '-'+ orgName.text
                    orgnames.append(orgName.text)
                    #print(orgName.text)



            auth += 1
        authors.append(auth_full)
        print(auth_full)
    art += 1

art = 0
for parent2 in root2.findall("issue/articles/article"):
    for kwdGroup in parent2.findall("keywords/kwdGroup"):
        print('next article')
        keys_in_article=[]
        for keyword in kwdGroup.findall("keyword"):
            pattern = re.compile('[a-zA-Z0-9]')
            is_english = pattern.match(keyword.text)
            if is_english:
                keys_in_article.append(keyword.text)
    keys_all.append(keys_in_article)
    art += 1
orgnames = set(orgnames)
orgnames = list(orgnames)
print(orgnames)

sum = len(authors)
print('Всего авторов', sum)
for parent in root.findall("record"):

    startPage = ET.SubElement(parent, 'startPage')
    startPage.text = startpages[i]

    endPage = ET.SubElement(parent, 'endPage')
    endPage.text = endpages[i]

    doi = ET.SubElement(parent, 'doi')
    doi.text = dois[i]

    publisherRecordId = SubElement(parent, 'publisherRecordId')
    publisherRecordId.text = '25422324'

    documentType = SubElement(parent, 'documentType')
    documentType.text = 'article'
    print('Номер статьи', i)
    title = ET.SubElement(parent, 'title', attrib={'language': "eng"})
    title.text = captions[2 * i + 1]



    authrs = ET.SubElement(parent, 'authors')


    affiliationsList = ET.SubElement(parent, 'affiliationsList')
    for work in range(len(orgnames)):
        if orgnames[work] == 'KSRC':
            orgnames[work] == 'Krylov State Research Centre'
        affiliationName = ET.SubElement(affiliationsList, 'affiliationName',  attrib={'affiliationId': str(work+1)})


        affiliationName.text = orgnames[work]

    for item in range(len(authors)):
        try:
            x, y, full_name, org = authors[item].split('-')
        except:
            print('ERROR! ', authors[item])

        if int(x) == i:
            print('№ автора: ' + str(item))
            author = ET.SubElement(authrs, 'author')
            name = ET.SubElement(author, 'name')
            name.text = full_name
            affiliationId = ET.SubElement(author, 'affiliationId')
            print(org, orgnames.index(org))
            affiliationId.text = str(orgnames.index(org) + 1)


    abstract = ET.SubElement(parent, 'abstract', attrib={'language': "eng"})
    abstract.text = abstracts[2 * i + 1]
    print(abstracts[2 * i + 1])

    fullTextUrl = SubElement(parent, 'fullTextUrl', attrib={'format': "pdf"})
    fullTextUrl.text = 'http://transactions-ksrc.ru/eng/archive/' + title.text.replace(' ', '-', 20) + '/'


    keywords = ET.SubElement(parent, 'keywords', attrib={'language': "eng"})
    for key in keys_all[i]:
        keyword = ET.SubElement(keywords, 'keyword')
        keyword.text = key
        print(key)



    i = i + 1
print(dois)
tree.write(doajfile)
'''



with open(doajfile, 'r') as f:
  old_data = f.read()

new_data = old_data.replace('>', '>\n')

with open (doajfile, 'w') as f:
  f.write(new_data)
'''