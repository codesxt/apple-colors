from sklearn import linear_model

# #824f3d
# #d56f87
# #c22e44

red_x = [[130, 79, 61], [213, 111, 135], [194, 46, 68]]
red_y = [0, 0.5, 1]

regr = linear_model.LinearRegression()
regr.fit(red_x, red_y)

red_x_pred = [[177, 47, 47]]
print(regr.predict(red_x_pred))
