from constant import pd, np, copy, plt, cm, date, timedelta, MAX_STATION, math
from plot import plot_coordinate, plot_polynomial_of_degree_n, plot_lagrange, plot_custom, plot_piecewise, plot_grid_spline
from clean import drop_empty, replace_by_mean, idw

# ========================= PREPARE VARIABLE =========================
obs_data = {}

# ========================= DATA PREPATATION =========================
# read CSV file
pressure_level = pd.read_csv('../observation_data/Sotterranee_livello_piezometrico_PD_1999_2021.csv', sep=";", encoding='latin-1')
point_coordinate = pd.read_csv('../observation_data/anagrafica_Sotterranee_livello_piezometrico_PD_1999_2021.csv', sep=";", encoding='latin-1')
# define variable
station_point = point_coordinate.iloc[:, 0]
x_coordinate = point_coordinate.iloc[:, 1]
y_coordinate = point_coordinate.iloc[:, 2]

# ========================= PLOT BORE HOLE =========================
obs_data = plot_coordinate(station_point, x_coordinate, y_coordinate)

# ========================= DATA FILTERING & CLEANING =========================

# METHOD A (drop all empty data)
# obs_data = drop_empty(obs_data, pressure_level) 

# METHOD B: replace empty data by mean
# obs_data = replace_by_mean(obs_data, pressure_level) 

# METHOD C: IDW to predict other station point value
# obs_data = idw(obs_data, pressure_level, point_coordinate) 


# ========================= DATA INTERPOLATION =========================

# 1. least square smoothing interpolation,
# plot some sample only --> degree 2
# plot_polynomial_of_degree_n(station_point, obs_data, 2) # all point
# plot_polynomial_of_degree_n(station_point, { 56: obs_data[56] }, 2)
# plot_polynomial_of_degree_n(station_point, { 66: obs_data[66] }, 2)
# plot_polynomial_of_degree_n(station_point, { 77: obs_data[77] }, 2)
# plot_polynomial_of_degree_n(station_point, { 83: obs_data[83] }, 2)
# plot_polynomial_of_degree_n(station_point, { 239: obs_data[239] }, 2)

# plot some sample only --> degree 3
# plot_polynomial_of_degree_n(station_point, obs_data, 3) # all point
# plot_polynomial_of_degree_n(station_point, { 1030: obs_data[1030] }, 3)
# plot_polynomial_of_degree_n(station_point, { 56: obs_data[56] }, 3)
# plot_polynomial_of_degree_n(station_point, { 77: obs_data[77] }, 3)
# plot_polynomial_of_degree_n(station_point, { 83: obs_data[83] }, 3)
# plot_polynomial_of_degree_n(station_point, { 239: obs_data[239] }, 3)

# plot some sample only --> degree 5
# plot_polynomial_of_degree_n(station_point, obs_data, 5) # all point
# plot_polynomial_of_degree_n(station_point, { 56: obs_data[56] }, 5)
# plot_polynomial_of_degree_n(station_point, { 66: obs_data[66] }, 5)
# plot_polynomial_of_degree_n(station_point, { 77: obs_data[77] }, 5)
# plot_polynomial_of_degree_n(station_point, { 83: obs_data[83] }, 5)
# plot_polynomial_of_degree_n(station_point, { 239: obs_data[239] }, 5)

# plot all sample
# plot_polynomial_of_degree_n(station_point, obs_data, 2)
# plot_polynomial_of_degree_n(station_point, obs_data, 3)
# plot_polynomial_of_degree_n(station_point, obs_data, 5)

# plot only for method C
# plot_polynomial_of_degree_n(station_point, { 1068: obs_data[1068] }, 2)
# plot_polynomial_of_degree_n(station_point, { 1068: obs_data[1068] }, 3)
# plot_polynomial_of_degree_n(station_point, { 1068: obs_data[1068] }, 5)

# 2. exact interpolation, polynomials of max degree = num of samples
# plot_polynomial_of_degree_n(station_point, { 56: obs_data[56] }, 15) # maximum only 40, because Python cannot handled big size of array
# plot_polynomial_of_degree_n(station_point, { 1068: obs_data[1068] }, int(len(obs_data[1068]['measurement']))) # don't show data because mulitplication return NaN
# plot_polynomial_of_degree_n(station_point, { 77: obs_data[77] }, 5) # don't show data because mulitplication return NaN
# plot_polynomial_of_degree_n(station_point, obs_data, int(len(station_point))) --> # don't show data because mulitplication return NaN

# 3. Exact interpolation --> lagrange
# plot_lagrange(station_point, obs_data, 1000)
sorted_date = sorted(obs_data[56]['measurement'].keys())
plot_lagrange(station_point, { 56: obs_data[56] }, sorted_date[-1]-sorted_date[0])
# plot_lagrange(station_point, { 66: obs_data[66] }, 1000)
# plot_lagrange(station_point, { 77: obs_data[77] }, 1000)
# plot_lagrange(station_point, { 83: obs_data[83] }, 1000)
# plot_lagrange(station_point, { 239: obs_data[239] }, 1000)

# plot only for method C
# plot_lagrange(station_point, { 1068: obs_data[1068] }, 1000)

# 4. trigonometric polynomial
# def interp_function(data):
#   return math.sin(0.5*(math.pi/180)*data) 

# plot_custom(station_point, obs_data, 1000, interp_function, 'Trigonometric Polynomial')

# 5. piecewise interpolation --> cubic
# plot_piecewise(station_point, obs_data)
# plot_piecewise(station_point, { 56: obs_data[56] })
# plot_piecewise(station_point, { 66: obs_data[66] })
# plot_piecewise(station_point, { 77: obs_data[77] })
# plot_piecewise(station_point, { 83: obs_data[83] })
# plot_piecewise(station_point, { 239: obs_data[239] })

# plot only for method C
# plot_piecewise(station_point, { 1042: obs_data[1042] })
# plot_piecewise(station_point, { 1043: obs_data[1043] })
# plot_piecewise(station_point, { 1044: obs_data[1044] })
# plot_piecewise(station_point, { 1045: obs_data[1045] })
# plot_piecewise(station_point, { 1046: obs_data[1046] })
# plot_piecewise(station_point, { 1068: obs_data[1068] })

# 6 grid knot spline -->
# plot_grid_spline('linear', station_point,{ 56: obs_data[56] }, 10, 100)
# plot_grid_spline('cubic', station_point,{ 56: obs_data[56] }, 23, 100) # 10 knots, and 100 n sample
# plot_grid_spline('cubic', station_point,{ 56: obs_data[56] }, 20, 100) # 10 knots, and 100 n sample
# plot_grid_spline('cubic', station_point,{ 66: obs_data[66] }, 20, 100)
# plot_grid_spline('cubic', station_point,{ 66: obs_data[66] }, 20, 100)
# plot_grid_spline('cubic', station_point,{ 77: obs_data[77] }, 10, 100)
# plot_grid_spline('cubic', station_point,{ 77: obs_data[77] }, 25, 100)
# plot_grid_spline('cubic', station_point,{ 83: obs_data[83] }, 10, 100)
# plot_grid_spline('cubic', station_point,{ 239: obs_data[239] }, 10, 100)

# plot only for method C
# plot_grid_spline('cubic', station_point,{ 1068: obs_data[1068] }, 10, 100)

plt.show()
