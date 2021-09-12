import sys
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from LAC import LAC
from pprint import pp
import re

class Analizer():
    """
    Analizer Class. To use it, firstly instantiate it, then call clean, lexical,
    most common words, most active users, describe methods (the order matters)
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

        try:
            self.df = pd.read_csv(csv_path)
        except FileNotFoundError as e:
            print(e)
            print(f"Please pass a valid csv file.")
            sys.exit()

        # Use debugger to inspect these two lists for lexical performance.
        # Tune the dictionary and cleaning if needed
        self.text_list = None
        self.flatten_list = None

        self.most_common_words = None
        self.most_active_users = None


    def data_clean(self):
        # A call back function does some regular expression cleaning
        # replace some stuff to '' (empty string)
        self.df['content'] = self.df['content'].apply(self._clean_text)

        # Then Get rid of rows that only has '' (empty string)
        self.df = self.df[self.df['content'] != '']
        self.text_list = self.df['content'].tolist()

    def word_could(self):
        pass

    def lexical_analyze(self):
        """ Use jieba or baidulac to do lexical analysis (e.g word segmentation, ngram, etc) """

        if self.text_list:
            lac = LAC(mode='seg')
            lac.load_customization('files/custom_dictionary_for_lac.txt', sep=None)
            texts = self.text_list
            seg_result = lac.run(texts)

            self.flatten_list = [ele for inner_list in seg_result for ele in inner_list]
        else:
            print("No texts for lexical analysis")

    @staticmethod
    def _clean_text(source):
        """ For pandas df callback apply()"""
        source = str(source)
        source = source.upper()
        source = re.sub('[？|?|！|!|，|,|.|。|#|《|》|<|>|（|）|(|)|〉|、|／|…|-]', '', source)
        source = re.sub('[哈｜嘿｜呵]', '', source)
        source = re.sub('NAN', '', source)
        source = re.sub('\xa0', '', source)
        return source

    def describe(self):
        """ Describe the analysis """
        if self.most_common_words:
            pp(self.most_common_words)

            # Plotting Most common words
            fig, ax = plt.subplots()
            ax.set_title("Most Common Words")
            ax.set_xlabel("Words")
            ax.set_ylabel("Counts")

            plt.bar(self.most_common_words.keys(), self.most_common_words.values())
            plt.rcParams['font.sans-serif'] = ['PingFang HK']  # fix Chinese chars showing issue
            plt.xticks(rotation=70)

            plt.show()

        else:
            print(f"Most common words data not found. Have you run that analysis? Try call it with the instance.")
            
        if self.most_active_users:
            pp(self.most_active_users)

            # Plotting Most common words
            fig, ax = plt.subplots()
            ax.set_title("Most Active Users")
            ax.set_xlabel("Users")
            ax.set_ylabel("Counts")
            plt.bar(self.most_active_users.keys(), self.most_active_users.values())
            plt.rcParams['font.sans-serif'] = ['PingFang HK']  # fix Chinese chars showing issue
            plt.xticks(rotation=70)

            plt.show()
        else:
            print(f"Most active users data not found. Have you run that analysis? Try call it with the instance.")

    def most_common_words_analyze(self):
        """ Most common words. """
        counter = Counter(self.flatten_list)

        df = pd.DataFrame({'word': counter.keys(), 'num': counter.values()})
        df = df.sort_values(by='num', ascending=False)

        # Remove rows only contain one word if you want. Because normally one word chinese
        # is meaningless in analysis. (not always). Up to you.
        df['length'] = df['word'].apply(lambda x: len(x))
        df = df[df['length'] > 1]

        df = df[['word', 'num']].head(20)
        data = df.to_dict('split')['data']
        self.most_common_words = dict(data)

    def most_active_users_analyze(self):
        """Most active users. (means people sending the most legit danmus)"""
        df = self.df['nickname'].value_counts().head(20)
        self.most_active_users = df.to_dict()


if __name__ == '__main__':

    args = sys.argv
    # print(args[1:])
    # to design to expect arg as csv file path, if not there, use a default csv_path
    # or '-f' (1st agr) 'path...' (2nd arg). execute like 'python analyzier.py -f -myfile.csv'

    csv_path = 'csv/312212_2021_09_06_21_28_40.csv'

    if len(args) > 1:
        csv_path = args[1]
        print(f"File: {csv_path}")
    else:
        print(len(args))
        print(f"Argument not specified. Use default example file: {csv_path}")

    analizer = Analizer(csv_path)

    analizer.data_clean()
    analizer.lexical_analyze()
    analizer.most_common_words_analyze()
    analizer.most_active_users_analyze()

    analizer.describe()

    print("Bye")