import pandas as pd

DESIRED_COLUMNS = ['description', 'material_&_care', 'article_type', 'fabric', 'fit', 'neck', 'pattern', 'type',
                   'length', 'country_of_origin', 'waist_rise', 'wash_care', 'sleeve_length']


def standardize_columns(col_names):
    final = []
    for item in col_names:
        item = item.lower()
        item = item.split(' ')
        item = "_".join(item)
        final.append(item)
    return final


def generate_html_table(row):
    row = dict(row)
    first = '<table border="0">'
    for k, v in row.items():
        if str(v) != 'nan' and k in DESIRED_COLUMNS:
            first = first + '<tr><td><strong>' + str(k) + '</strong></td></tr>'
            first = first + '<tr><td><p>' + str(v) + '</p></td><tr>'
    last = '</table>'

    return first + last


class Transform:

    def __init__(self, path):
        self.path = path
        self.df = None
        self.process_file()
        self.second_df = None

    def process_file(self):
        self.df = pd.read_csv(self.path + "/" + "Attributes.csv")
        self.df.columns = standardize_columns(self.df.columns)
        self.df['image'] = self.df[self.df.columns[18:]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)
        self.df = self.df.drop(['default_image', 'front_image', 'front_image',
                                'side_image', 'back_image', 'detail_angle', 'look_shot_image',
                                'additional_image_1', 'additional_image_2'], axis=1)

        self.df['attributes'] = self.df.apply(generate_html_table, 1)
        second_df = pd.read_csv(self.path + "/" + "Invoice.csv")
        second_df = second_df.drop(
            ['HS Code', 'DESCRIPTION OF GOODS', 'SKU Code', 'Brand', 'Dispatch Qty', 'TOTAL VALUE\nIN INR'], axis=1)
        second_df.columns = ['style_id', 'PRICE PER UNIT\nIN INR']
        self.df = pd.merge(self.df, second_df, how="inner", on=["style_id"])
        self.df = self.df.apply(lambda x: x * 1.6 if x.name == 'PRICE PER UNIT\nIN INR' else x)
        self.df = self.df.rename(columns={'PRICE PER UNIT\nIN INR': 'price'})
        third_df = pd.read_csv(self.path + "/" + 'Packing-List.csv')
        third_df = third_df.groupby(['Style Id'], as_index=False)['Ship Quantity'].sum()
        third_df = third_df.rename(columns={'Style Id': 'style_id', 'Ship Quantity': 'quantity'})
        self.df = pd.merge(self.df, third_df, how="inner", on=["style_id"])
        self.df = self.df.drop(DESIRED_COLUMNS, axis=1)
        self.extract_csv()

    def extract_csv(self):
        self.df.to_csv(self.path + "/" + "final.csv", index=False)




