from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import os
import re

# replace any character that is not digit or letter or space with empty string
replace_with_empty_pattern = re.compile(r'[^A-Za-z0-9\s]')
# replace consecutive spaces and enters(\n) with a single space
replace_with_single_space_pattern = re.compile(r'\s+')


def preprocess_content(content):
    return re.sub(
        replace_with_single_space_pattern, ' ',
        re.sub(replace_with_empty_pattern, '', content)
    )


print('Reading contents of 20newsgroup--18828 dataset...')
# out directory to store newsgroup datasset
directory = './20news-18828'
# category_names[label_number - 1] = category name
category_names = os.listdir(directory)
# sequence of news contents --- X
news_contents = list()
# sequence of news labels  --- Y
news_labels = list()
# traverse into directories
for i in range(len(category_names)):
    category = category_names[i]
    category_dir = os.path.join(directory, category)
    for file_name in os.listdir(category_dir):
        file_path = os.path.join(category_dir, file_name)
        # get the word list of a single news file
        raw_content = open(file_path, encoding='latin1').read().strip()
        news_content = preprocess_content(raw_content)
        # add to news labels and news contents
        news_labels.append(i + 1)
        news_contents.append(news_content)
        print(news_content)
    print('Read contents of category: %s!' % category)
print('Successfully read contents of 20newsgroup--18828 dataset!\n')


print('Splitting data into training and testing set...')
train_contents, test_contents, train_labels, test_labels = \
    train_test_split(news_contents, news_labels, shuffle=True, test_size=0.5)
print('Data is splitted successfully!\n')
print('Running pipeline of text classification...')
tfidf_vectorizer = TfidfVectorizer()
chi2_feature_selector = SelectKBest(chi2, k=5000)
svm_classifier = LinearSVC(verbose=True)
pipeline = Pipeline(memory=None, steps=[
    ('tfidf', tfidf_vectorizer),
    ('chi2', chi2_feature_selector),
    ('svm', svm_classifier),
])
pipeline.fit(train_contents, train_labels)
result = pipeline.predict(test_contents)
report = classification_report(test_labels, result, target_names=category_names)
print(report)
