from constant import np, date, plt, color, MAX_STATION, timedelta, pd, date_to_int, int_to_date, math
from interpolation import polynomial_of_degree_n, lagrange
from typing import List, Dict, Callable

# plot coordinate --> to plot coordinate location
def plot_coordinate(station_arr, x_arr, y_arr):
  obs_data = {}
  # plot_header('Borehole Position', 'X Coordinate', 'Y Coordinate', 'Borehole')
  
  for i, c in zip(range(int(len(station_arr))), color(len(station_arr))):
    obs_data[station_arr[i]] = { 
      'coordinate': {
        'x': x_arr[i], 
        'y': y_arr[i],
      }, 
      'measurement': {},
      'statistic': {}, 
    }

    # plt.plot(x_arr[i], y_arr[i], 'o')
    # plot_setting(x_arr[i], y_arr[i], station_arr[i], False)
  return obs_data

# sketch interpolation function
def plot_polynomial_of_degree_n(station_arr: List, obs_data: Dict, n_coeff):
  plot_header('Polynomial of Degree N Interpolation')

  for station, c in zip(obs_data, color(len(station_arr))):
    sorted_date = sorted(obs_data[station]['measurement'].keys())
    x = [] # observation date 
    f = [] # observation value -> matrix f
    A = [] # matrix A
    n_interpolated = np.linspace(sorted_date[0], sorted_date[-1], num = int(100)) # number of sample x to be interpolated

    for data in sorted(obs_data[station]['measurement']):
    # for data in sorted(test):
      x.append(int_to_date(data))
      f.append(obs_data[station]['measurement'][data])
      # use polynomial_of_degree_n from interpolation.py
      A.append(polynomial_of_degree_n(data, n_coeff))
      #plot each observation
      plt.plot(int_to_date(data), obs_data[station]['measurement'][data], '.', color='gray')          

    # finding unknown coeff
    matrix_A = np.array(A, dtype='float64')
    matrix_f = np.array(f, dtype='float64')
    matrix_N = np.transpose(matrix_A).dot(matrix_A)
    matrix_x = np.linalg.inv(matrix_N).dot((np.transpose(matrix_A).dot(np.transpose(matrix_f))))

    f_temp = [] # for looping sample
    x_interpolated = [] # for looping sample
    for i in range(int(n_interpolated[0]), int(n_interpolated[-1])):
      x_interpolated.append(int_to_date(math.ceil(i)))
      # use lagrange function from file interpolation.py
      f_temp.append(polynomial_of_degree_n(i, n_coeff))

    f_interpolated = np.array(f_temp, dtype='float64').dot(matrix_x)

    plt.plot(x_interpolated, f_interpolated, label = "P{}".format(int(station)))
    plot_setting(x_interpolated[-1], f_interpolated[ -1], station) # beautify plot
    
def plot_lagrange(station_arr: List, obs_data: Dict, n_sample):
    plot_header('Lagrange Interpolation')

    for station, c in zip(obs_data, color(len(station_arr))):
      sorted_date = sorted(obs_data[station]['measurement'].keys())
      n_interpolated = np.linspace(sorted_date[0], sorted_date[-1], num = int(n_sample)) # number of sample x to be interpolated
      x_interpolated = [] # obs date
      f_interpolated = [] # obs value

      # plot observation point
      for data in sorted(obs_data[station]['measurement']):
        obs_value = obs_data[station]['measurement'][data]
        obs_date = int_to_date(data)

        plt.plot(obs_date, obs_value, 'o', color='red')
      
      # sample to be inserted into lagrange function
      for i in range(len(n_interpolated)):
        x_interpolated.append(int_to_date(math.ceil(n_interpolated[i])))
        # use lagrange function from file interpolation.py
        f_interpolated.append(lagrange(math.ceil(n_interpolated[i]), obs_data[station]['measurement']))

      plt.plot(x_interpolated, f_interpolated, label = "P{}".format(int(station)))
      plot_setting(x_interpolated[-1], f_interpolated[-1], station)

def plot_custom(station_arr, obs_data, n_interpolated, interpolation_method, interpolation_title):
  # sketch interpolation using defined custom math function
  plot_header(interpolation_title)

  for station, c in zip(obs_data, color(len(station_arr))):
    sorted_date = sorted(obs_data[station]['measurement'].keys())
    n_interpolated = np.linspace(sorted_date[0], sorted_date[-1], num = int(n_interpolated)) # number of sample x to be interpolated
    x_interpolated = [] # obs date
    f_interpolated = [] # obs value

    # plot observation point
    for data in sorted(obs_data[station]['measurement']):
      plt.plot(int_to_date(data), obs_data[station]['measurement'][data], '.', color='gray')

    for i in range(len(n_interpolated)):
      x_interpolated.append(int_to_date(math.ceil(n_interpolated[i])))
      # interpolation_method function is fetched from interpolation.py file
      f_interpolated.append(interpolation_method(math.ceil(n_interpolated[i])))

    plt.plot(x_interpolated, f_interpolated, label = "P{}".format(int(station)))
    plot_setting(x_interpolated[-1], f_interpolated[-1], station)

def plot_piecewise(station_arr, obs_data):
  plot_header('Piecewise Interpolation')

  for station, c in zip(obs_data, color(len(station_arr))):
    obs_date = [] # obs date
    f_obs = [] # obs value

    for data in sorted(obs_data[station]['measurement']):
      # plot observation point
      plt.plot(int_to_date(data), obs_data[station]['measurement'][data], 'o', color='red')
      obs_date.append(data)
      f_obs.append(obs_data[station]['measurement'][data])
      
    obs_date = np.array(obs_date)
    x_interp = np.array(range(obs_date[0], obs_date[-1])) # sample taken between obs date point
    f_obs = np.array(f_obs)

    h = np.diff(obs_date) #spacing
    N_ini = 0 #initial first derivative
    N_fin = 0 #final first derivative
    n_obs = len(obs_date)

    d = 3*(f_obs[2:]-f_obs[1:-1])/h[1:]*h[:-1] + 3*(f_obs[1:-1]-f_obs[:-2])/h[:-1]*h[1:]

    A1 = np.diag(2*(h[:-1] + h[1:]), 0)
    A2 = np.diag(h[:-2], 1)
    A3 = np.diag(h[2:], -1)
    A = A1+A2+A3
    y = d

    y[0] = y[0]-h[1]*N_ini
    y[-1] =  y[-1]-h[-1]*N_fin

    N = np.linalg.inv(A).dot((np.transpose(y)))
    N = np.insert(N, 0, 0, axis=0)
    N = np.append(N,0)

    for i in range(1, n_obs):
      x_fix = []
      x_date = []
      for j in range(len(x_interp)):
        if(x_interp[j] >= obs_date[i-1]-1 and x_interp[j]<= obs_date[i]+1):
          x_date.append(int_to_date(int(x_interp[j])))
          x_fix.append(int(x_interp[j]))
      # calculate final math function 
      S = f_obs[i-1] + N[i-1]*(np.array(x_fix)-obs_date[i-1]) + ((3*(f_obs[i]-f_obs[i-1]))/(h[i-1]**2)-(2*N[i-1]+N[i])/(h[i-1]))*((np.array(x_fix)-obs_date[i-1])**2) + ((-2*(f_obs[i]-f_obs[i-1]))/(h[i-1]**3)+(N[i-1]+N[i])/(h[i-1]**2))*((np.array(x_fix)-obs_date[i-1])**3)
      plt.plot(x_date, S, label = "P{}".format(int(station)), color='gray')
      if(i == n_obs-1): plot_setting(x_date[-1], S[-1], station, False)

def plot_grid_spline(name, station_arr, obs_data, n_spl, n_obs): # n_obs sample
  if (name == 'linear'):
    plot_header(name)
    for station, c in zip(obs_data, color(len(station_arr))):
      sorted_date = sorted(obs_data[station]['measurement'].keys())
      # x_interp is spreaded obs_date data based on n_obs but in integer format --> needed for mesh grid
      x_interp = np.linspace(sorted_date[0], sorted_date[-1], num = int(n_obs)) 
      # x_interp_date is spreaded obs_date data based on n_obs but in integer format --> needed for final plot
      x_interp_date = pd.date_range(start=int_to_date(sorted_date[0]), end=int_to_date(sorted_date[-1]), periods=n_obs)
      x_obs = [] # obs date
      f_interpolated = [] # obs value

      for data in sorted(obs_data[station]['measurement']):
        x_obs.append(data)
        f_interpolated.append(obs_data[station]['measurement'][data])
        # plot observation point
        plt.plot(int_to_date(data), obs_data[station]['measurement'][data], '.', color='gray')  

      delta = (x_obs[-1] - x_obs[0])/(n_spl-1);	
      x_spl = np.linspace(sorted_date[0], sorted_date[-1], int((sorted_date[-1] - sorted_date[0])/int(delta)) + 1) # number of x to be interpolated
      SPL,OBS = np.meshgrid(x_spl,x_obs)
      D = (OBS-SPL)/delta
      A1 = 1-D
      A2 = 1+D
      A1[(D<0) | (D>1)] = 0
      A2[(D<-1) | (D>0)] = 0
      A = A1+A2
      A[D<=0] = 1
      N = np.transpose(A).dot(A)
      f = np.transpose(A).dot(np.transpose(f_interpolated))
      x = np.linalg.inv(N).dot(f)

      SPL,PRED = np.meshgrid(x_spl,x_interp)
      D = (PRED-SPL)/delta
      A1 = 1-D
      A2 = 1+D
      A1[(D<0) | (D>1)] = 0
      A2[(D<-1) | (D>0)] = 0
      A = A1+A2
      D = np.array(D)
      A[D<=0] = 1
      f_interp = np.array(A).dot(np.transpose(x))

      plt.plot(x_interp_date, f_interp)
      plot_setting(x_interp_date[-1], f_interp[-1], station, False)

  elif(name == 'cubic'):
    plot_header(name)
    for station, c in zip(obs_data, color(len(station_arr))):
      sorted_date = sorted(obs_data[station]['measurement'].keys())
      # x_interp is spreaded obs_date data based on n_obs but in integer format --> needed for mesh grid
      x_interp = np.linspace(sorted_date[0], sorted_date[-1], num = int(n_obs))
      # x_interp_date is spreaded obs_date data based on n_obs but in integer format --> needed for final plot
      x_interp_date = pd.date_range(start=int_to_date(sorted_date[0]), end=int_to_date(sorted_date[-1]), periods=n_obs)
      x_obs = []
      f_interpolated = [] # obs value -> matrix f
      
      for data in sorted(obs_data[station]['measurement']):
        x_obs.append(data)
        f_interpolated.append(obs_data[station]['measurement'][data])
        plt.plot(int_to_date(data), obs_data[station]['measurement'][data], '.', color='gray')  

      delta = (x_obs[-1] - x_obs[0])/(n_spl-1)
      x_spl = np.linspace(sorted_date[0], sorted_date[-1], int((sorted_date[-1] - sorted_date[0])/int(delta)) + 1) # number of x to be interpolated
      SPL,OBS = np.meshgrid(x_spl,x_obs)
      D = (OBS-SPL)/delta
      A1 = 1/6*((D+2)**3)
      A2 = 1/6*(((D+2)**3)-4*((D+1)**3))
      A3 = 1/6*(((2-D)**3)-4*((1-D)**3))
      A4 = 1/6*(2-D)**3
      A1[(D<=-2) | (D>=-1)] = 0
      A2[(D<=-1) | (D>=0)] = 0
      A3[(D<=0) | (D>=1)] = 0
      A4[(D<=1) | (D>=2)] = 0
      A = A1+A2+A3+A4
      A[D==0] = 2/3
      A[D==-1] = 1/6
      A[D==+1] = 1/6
      N = np.transpose(A).dot(A)
      f = np.transpose(A).dot(np.transpose(f_interpolated))
      x = np.linalg.inv(N).dot(f)

      SPL,PRED = np.meshgrid(x_spl,x_interp)
      D = (PRED-SPL)/delta
      A1 = 1/6*((D+2)**3)
      A2 = 1/6*(((D+2)**3)-4*((D+1)**3))
      A3 = 1/6*(((2-D)**3)-4*((1-D)**3))
      A4 = 1/6*((2-D)**3)
      A1[(D<=-2) | (D>=-1)] = 0
      A2[(D<=-1) | (D>=0)] = 0
      A3[(D<=0) | (D>=1)] = 0
      A4[(D<=1) | (D>=2)] = 0
      A = A1+A2+A3+A4
      A[D==0] = 2/3
      A[D==-1] = 1/6
      A[D==+1] = 1/6
      f_interp = A.dot(x)
      plt.plot(x_interp_date, f_interp)
      plot_setting(x_interp_date[-1], f_interp[-1], station, False)

# setting for plot
def plot_header(title, xlabel = 'Observation date', ylabel = 'Water pressure level', figure = 'Piezometer Measurements in the District of Padua'):
  plt.figure(figure)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

def plot_setting(abscissa: List, ordinate: List, label: List, legend = True):
  plt.annotate("P{}".format(label), # this is the text
              (abscissa, ordinate), # these are the coordinates to position the label
              textcoords="offset points", # how to position the text
              xytext=(15,-3), # distance from text to points (x,y)
              fontsize=7, # fontsize
              ha='center') # horizontal alignment can be left, right or center
  if(legend): plt.legend(loc=(1, 0))