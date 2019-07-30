from keras import models
from keras import layers
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import random


def setup_nn(n1, n2, n3, dim):
    model = models.Sequential()  # create sequential multi-layer perceptron
    model.add(layers.Dense(n1, input_dim=dim, kernel_initializer='normal', activation='relu'))
    model.add(layers.Dense(n2, kernel_initializer='normal', activation='relu'))
    model.add(layers.Dense(n3, kernel_initializer='normal', activation='relu'))
    model.add(layers.Dense(1, kernel_initializer='normal', activation='linear'))
    model.compile(loss='mean_squared_error', optimizer='Adam')
    return model

def training(n1, n2, n3):
    model = setup_nn(n1, n2, n3, X_train.shape[1])
    model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test), verbose=0)
    y_predict = model.predict(X_test)
    r2 = r2_score(y_test, y_predict)

    print('***********Nodes: ', n1, n2, n3, '\t\tScore: ', r2, '**************')

    return r2

def trying():
    best_score = 0
    nodes = []
    # for n3 in range(10, 80, 10):
    #     for n2 in random.randint(20, 90):
    #         for n1 in random.randint(30, 100):
    for i in range(100):
        n1 = random.randint(10, 80)
        n2 = random.randint(20, 90)
        n3 = random.randint(30, 100)
        mm = training(n1, n2, n3)
        if mm > best_score:
            best_score = mm
            nodes = [n1, n2, n3]
        print('\tBest: ', 'Nodes: ', nodes, '\t\tScore: ', best_score)

def generate_data(filename):
    df = pd.read_csv(filename)

    df['accommodates_s'] = df['accommodates'] ** 2
    df['scenery_s'] = df['scenery'] ** 2
    df['bedroom_s'] = df['bedroom'] ** 2
    df['beds_s'] = df['beds'] ** 2
    df['subway_s'] = df['subway'] ** 2
    df['accom_bedroom'] = df.accommodates * df.bedroom
    df['bedroom_for_each'] = df.accommodates / df.bedroom
    df['beds_for_each'] = df.accommodates / df.beds

    features = [df.Entire_home, df.accommodates, df.scenery, df.house_ln,
                df.Madison_Square_Garden,
                df.Flatiron_Building, df.madame_tussauds_new_york, df.Empire_state_Building,
                # df.intrepid_sea_air, df.Washington_Square_Park, df.New_york_Public_Library, df.Times_Square,
                # df.New_York_University, df.Grand_Centreal_Terminal, df.Top_of_the_Rock, df.St_Patrick_Cathedral,
                # df.Museum_of_Modern_Art, df.Manhattan_Skyline, df.United_Nations_Headquarters,

                df.bathroom, df.response_time_num, df.host_response_rate, df.crime_rate,
                df.guests, df.park, df.bedroom, df.beds, df.house_la, df.subway,
                df.sub_dist_1, df.sub_dist_2, df.sub_dist_3, df.bus_stop,
                df.accom_bedroom,

                # df.One_world_trade_cente, df.Central_Park, df.Van_Cortlandt, df.Flushing_Meadows, df.Prospect_Park,
                # df.Bronx_Park, df.Pelham_Bay_Park, df.Floyd_Bennet_Field, df.Jamaica_Bay, df.Jacob_Riis_Park,
                # df.Fort_Tilden, df.Greenbelt, df.The_Metropolitan_Museum_of_Art, df.statue_of_liberty,
                # df.American_Museum_of_Natual_History, df.Fifth_Avenue, df.Brooklyn_Bridge, df.Wall_Street,
                # df.Broadway, df.China_Town, df.West_Point_Academy, df.Columbia_University,
                # df.National_September_11_Memorial_Museum, df.SOHO, df.High_Line_Park,

                df.subway_s, df.accommodates_s, df.scenery_s,
                df.beds_s, df.beds_for_each, df.bedroom_for_each, df.bedroom_s,
                ]

    # dataset = pd.concat(features, axis=1)
    # dataset = dataset.dropna().astype(dtype='float64', copy=False)

    X = pd.concat(features, axis=1).dropna().astype(dtype='float64', copy=False)
    y = df.daily_price

    _x_train, _x_test, _y_train, _y_test = train_test_split(X.values, y.values, test_size=0.2)
    X_sc = StandardScaler()
    X_sc.fit(_x_train)
    _x_train = X_sc.transform(_x_train)
    _x_test = X_sc.transform(_x_test)
    return _x_train, _x_test, _y_train, _y_test


if __name__ == '__main__':
    X_train, X_test, y_train, y_test = generate_data('../data/housing_all_clean.csv')
    trying()
    # training(90, 90, 20)
    # 90 90 20
