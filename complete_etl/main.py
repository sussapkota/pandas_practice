import csv
import os
import shutil
import time
import zipfile

from db_service.db_config import Database
from transform import Transform


def check_for_files():
    files = []
    for file in os.listdir():
        if file.split('.')[-1] == 'zip':
            files.append(file)
    return files


def check_valid_files(path):
    """
    Function to make sure we have the required files..
    :param path:
    :return:
    """
    VALID_NAMES = ['Attributes.csv', 'Invoice.csv', 'Packing-List.csv']
    zip_files = os.listdir(path)
    for zip_file_name in zip_files:
        if zip_file_name not in VALID_NAMES:
            print("All required files not in zip file... skipping")
            return False

    return True


def extract_files(files):
    for file in files:
        os.mkdir("." + file)
        try:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall("." + file)
        except Exception as e:
            print(e, "..Skipping..")


def clean_up(files):
    for file in files:
        shutil.rmtree('.' + file, ignore_errors=True)


# def send_to_db(file):
#     path = file + "final.csv"
#     user = "postgres"
#     password = user
#     ip = 'localhost'
#     dbase = 'etl'
#     conn = create_engine(f'postgresql://{user}:{password}@{ip}/{dbase}').raw_connection()
#     cursor = conn.cursor()
#     with open(path, 'r') as file:
#         data_df = pd.read_csv(file)
#
#     data_df.to_sql('restaurant', con=conn, index=True, index_label='id', if_exists='replace')


def send_to_db(file, db):
    path = file + "final.csv"

    with open(path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        for row in csvreader:
            s_id = int(row[0])
            gender = (row[1])
            brand = (row[2])
            style_name = (row[3])
            color = (row[4])
            image = (row[5])
            attributes = (row[6])
            price = float(row[7])
            quan = int(row[8])
            # db.add(*row)

            db.add(s_id, gender, brand, style_name, color, image, attributes, price, quan)


def transform(files, db):
    for file in files:
        if check_valid_files("." + file):
            print("Calling transform..")
            Transform("." + file)
            send_to_db("." + file + "/", db)
        else:
            print(f'Not all required files are there to process.. Skipping {file}.')


if __name__ == '__main__':
    found = []
    db = Database()
    while True:
        new_files = check_for_files()
        files = []

        for val in new_files:  # going through all files
            if val not in found:  # if not already in found process it and add to found and skip others
                files.append(val)
                found.append(val)
            else:
                print(f"{val} is already process and will be skipped...")

        try:
            extract_files(files)
            transform(files, db)
        except Exception as e:
            print(e.with_traceback())
        finally:
            clean_up(files)

        time.sleep(30)
        print("Checking again...")
