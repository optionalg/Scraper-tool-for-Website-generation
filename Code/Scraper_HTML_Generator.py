
# Description: This programs extracts keywords from inventory file and performs copounding of words, stop words removal

# stemming as well as spelling correction. It writes all the keywords to index.html file.



# Assumptions: 1.) We have assumed that compounding of words is only meaningful for words labeled as keywords

             # 2.) In order to execute the script, the user must download wordnet.

             #          - this can be done with the "nltk.download()" command in python.

             # 3.) We have removed URL's, doi numbers.

             # 4.) We have wordnet lemmatization instead of stemming to preserve the meaning of our words and improve the

             #     performance of our script.

             # 5.) We arranged the words in index.html in ascending order (alphabetically).

             # 6.) We have used UTF-16 encoding for Milestone4 Sub_Chhabra_Kelly_Savlani.csv file.





from nltk.stem.wordnet import *

import nltk

import re

import csv



# NOTE: please download the wordnet package with the following command (if it doesn't already exist):

# nltk.download()



word_net = WordNetLemmatizer()



# Reads file and returns a list of articles

def get_articles(filename):

    file = open(filename, encoding='utf8')

    doc = []  # a list of all articles

    article = ''

    # convert each line of an article to one string, then append article to doc

    for line in file:

        # empty line separates current article from the next

        if line.strip() == '':

            if not (article.startswith('"') or article.startswith('\ufeff')):

                doc.append(article)

            article = ''

        # otherwise add string to current article

        else:

            article += line.strip() + ' '

    return(doc)





def get_replacements(filename):

    replacements = {}

    with open(filename, 'rU', encoding='utf16') as f:

        reader = csv.reader(f, delimiter=',')

        for line in reader:

            replacements[line[0]] = line[1]



    return replacements





def get_noise_words(filename):

    with open(filename, encoding='utf8') as f:

        noisewords = [line.rstrip() for line in f]

    return noisewords





def extract_tokens(article):

    # remove journal, page number, doi (everything after title and before Abstract)

    article = re.sub('" .*Abstract:?', '"', article)

    # remove URL

    article = re.sub('}, URL: .*', '', article)

    # extract word tokens from the article before the keywords (remove numbers)

    m = re.findall(r"\b([a-zA-Z][a-zA-Z_\-]+\b)", article[:article.index('keywords: {')])

    m = [word_net.lemmatize(word) for word in m]

    # handle keywords differently as compound concepts

    temp = re.sub(' ', '_', article[article.index('keywords: {') + 11:])

    m += temp.split(';')

    return m





def remove_noise_words(tokens, noise_words):

    noise_words = set(noise_words)

    new_tokens = []

    for token in tokens:

        if token.lower() not in noise_words:

            new_tokens.append(token)

    return new_tokens





def replace_words(tokens, replacements):

    for i in range(len(tokens)):

        if tokens[i] in replacements:

            tokens[i] = replacements[tokens[i]]

    return tokens





def write_index_html(keywords):

    with open('index.html', 'w+', encoding='utf8') as f:

        f.write("<!DOCTYPE html>\n<!Author- Gaurav Savlani, Alex Kelly, Paras Chhabra>\n<!Creation Date- 4-11-2016>"

                "<!Last Modification Date- 4-11-2016> \n<!This html shows the output of ACM library publication displayed to the user to check research published.> \n"

                '<html> \n<head> \n<title>ACM Publications</title> <meta charset = "UTF-8">\n'

                '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n</head> \n'

                '<body> \n<div><center>'

                '\n<font size="7" color="blue"><b>ACM Digital Library</b></font></center></div>'

                '<h1>'

                '<b>'

                '<font size="4">Please choose a category below to find research details</font></b></h1>'

                '<form name="ACME_form" action="ACME_form">'

                '<br>')

        counter = 0

        for keyword in sorted(keywords):

            counter += 1

            f.write(str(counter) + '.  <a href = "' + keyword + '.html">' + keyword + '</a><br>\n')



        f.write("<br>")



        f.write('<b>Search for keyword</b><br><input type="text" name="Search keyword" value="" />'

                '</form>'

                '</body>'

                '</html>')



# item = (key, value)

def write_keyword_html(item):

    with open(item[0] + '.html', 'w+' ,encoding='utf8') as f:

        f.write(

            "<!DOCTYPE html>\n<!Author- Gaurav Savlani, Alex Kelly, Paras Chhabra>\n<!Creation Date- 4-11-2016>"

            "<!Last Modification Date- 4-11-2016> \n<!This html shows all ACM articles associated with the particular keyword.> \n"

            '<html> \n<head> \n<title>' + item[0] + '</title> <meta charset = "UTF-8">\n'

            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n</head> \n'

            '<body> \n<div><center>'

            '\n<font size="7" color="blue"><b>ACM Digital Library</b></font></center></div>'

            '<h1>'

            '<b>'

            '<font size="4">' + item[0] + '</font></b></h1>'

            '<form name="ACME_form" action="ACME_form">'

            '<br>')

        counter = 0

        for article in item[1]:

            counter += 1

            title = article.title

            bad = ["/", ".", " ", ":", "?"]

            for c in bad:

                title = title.replace(c, "_")

            f.write(str(counter) +'.  '+ article.authors + ' - "<a href="' + title + '.html">' + article.title + '"</a><br>\n')



def write_article_html(article):

    title = article.title

    bad = ["/", ".", " ", ":", "?"]

    for c in bad:

        title = title.replace(c, "_")

    try:

        with open(title + ".html", "w+", encoding='utf8') as f:

            f.write("<!DOCTYPE html>\n<!Author- Gaurav Savlani, Alex Kelly, Paras Chhabra>\n<!Creation Date- 4-11-2016>"

                "<!Last Modification Date- 25-11-2016> \n<!This html shows the info on article contained in ACM Inventory files.>"

                '<html> \n<head> \n<title> ' + title +'</title> <meta charset = "UTF-8">\n'

                '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n</head> \n'

                '<body> \n<div><center>'

                '\n<font size="7" color="blue"><b>ACM Digital Library</b></font></center></div>'

                '<h1>' '<b>'

                'Title: ' + article.title + '</b></h1>'

                '<h2>' + 'Authors: ' + article.authors + '</h2>'

                '<p>' + '<b>' + 'Abstract: ' + '</b>' + article.abstract + '</p>')

    except:

        print(title)





class Article:

    def __init__(self, article):

        m = re.match(r'(.*), "(.*),".*Abstract: (.*) keywords: {', article)

        self.authors = m.group(1)

        self.title = m.group(2)

        self.abstract = m.group(3)





# get replacements as a dictionary

replacements = get_replacements('Milestone4 Sub_Chhabra_Kelly_Savlani.csv')

# get noise_words as a set

noise_words = get_noise_words('Milestone4 Del_Chhabra_Kelly_Savlani.txt')

# get articles as a list of publication strings

articles = get_articles('downloadCitations.txt')

# iterate through articles and extract keywords

keywords = {}

for article in articles:

    a = Article(article)

    tokens = extract_tokens(article)

    tokens = remove_noise_words(tokens, noise_words)

    tokens = replace_words(tokens, replacements)

    for token in tokens:

        token = token.replace('/', '_')

        token = token.lower()

        if token in keywords:

            keywords[token].update([a])

        else:

            keywords[token] = set([a])

    write_article_html(a)



write_index_html(keywords)

while len(keywords) > 0:

    write_keyword_html(keywords.popitem())

