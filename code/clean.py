from constant import pd, copy, date_to_int, MAX_STATION, int_to_date, date, MAX_YEAR, MIN_YEAR

# METHOD A (drop all empty data)
def drop_empty(obs_data, pressure_level):
  for i in range(int(len(pressure_level))):
    station_point = pressure_level.iloc[i, 0]
    if(station_point <= MAX_STATION):
      obs_date = date_to_int(pd.to_datetime(pressure_level.iloc[i, 1]))
      obs_value = pressure_level.iloc[i, 2]

      if isinstance((obs_value), str): # filter value in hashmap form and edit number format
        obs_data[station_point]['measurement'][obs_date] = float(obs_value.replace(',','.'))
    else: 
      obs_data.pop(station_point, None)
  return obs_data

# METHOD B: replace empty data by mean --> perlu di fix
def replace_by_mean(obs_data, pressure_level, max_station_point = MAX_STATION):
  for i in range(int(len(pressure_level))):
    station_point = pressure_level.iloc[i, 0]
    if(station_point <= max_station_point):
      obs_date = date_to_int(pd.to_datetime(pressure_level.iloc[i, 1]))
      obs_year = pd.to_datetime(pressure_level.iloc[i, 1]).year
      obs_value = pressure_level.iloc[i, 2]

      # hashmap preparation if not available yet
      if(obs_year not in obs_data[station_point]['statistic']):
          obs_data[station_point]['statistic'][obs_year] = { 'sum': 0, 'count': 0, 'mean': 0}

      # if obs value is not NaN, empty, or false; else set as zero
      if isinstance((obs_value), str):
        obs_data[station_point]['measurement'][obs_date] = float(obs_value.replace(',','.'))
        # sum and count is used for calculating mean
        obs_data[station_point]['statistic'][obs_year]['sum'] += float(obs_value.replace(',','.'))
        obs_data[station_point]['statistic'][obs_year]['count'] += 1 
        obs_data[station_point]['statistic'][obs_year]['mean'] = obs_data[station_point]['statistic'][obs_year]['sum']/obs_data[station_point]['statistic'][obs_year]['count']
      else:
        obs_data[station_point]['measurement'][obs_date] = 0
    else:
      obs_data.pop(station_point, None)

  # replacing each zero value with the mean ( mean is calculated based on specific year only not the whole data)
  for station in obs_data:
    for i in list(obs_data[station]['measurement'].keys()):
      if obs_data[station]['measurement'][i] == 0:
        if  (obs_data[station]['statistic'][int_to_date(i).year]['mean'] == 0):
          del obs_data[station]['measurement'][i]
        else:
          obs_data[station]['measurement'][i] = obs_data[station]['statistic'][int_to_date(i).year]['mean']
  
  return obs_data

# METHOD C: IDW to predict other station point value
def idw(obs_data, pressure_level, point_coordinate):
  # this idw method focus on station point that is totaly empty (station point number > 518) but the data focus on calculating
  # per year only (so 1 year is only one observation data)
  obs_data = replace_by_mean(obs_data, pressure_level, 1068)

  for k in range(MIN_YEAR, MAX_YEAR):
    for i in range(int(len(point_coordinate))):
      station_point = point_coordinate.iloc[:, 0][i]
      x_coordinate = point_coordinate.iloc[:, 1][i]
      y_coordinate = point_coordinate.iloc[:, 2][i]

      total_weight = 0
      distance = 0
      value_per_distance = 0

      for j in range(int(len(point_coordinate))):
        station_point_ref = point_coordinate.iloc[:, 0][j]
        x_ref = point_coordinate.iloc[:, 1][j]
        y_ref = point_coordinate.iloc[:, 2][j]
        
        if x_coordinate != x_ref and y_coordinate != y_ref and k in obs_data[station_point_ref]['statistic']:
          distance = (((x_coordinate - x_ref)**2) + ((y_coordinate - y_ref)**2)) ** 0.5
          total_weight += (1/distance)
          value_per_distance += obs_data[station_point_ref]['statistic'][k]['mean']/distance
          
      if (k not in obs_data[station_point]['statistic']): #right for 56
        obs_data[station_point]['statistic'][k] = {'mean': value_per_distance/total_weight} 
      elif (obs_data[station_point]['statistic'][k]['count'] == 0):
        obs_data[station_point]['statistic'][k] = {'mean': value_per_distance/total_weight} 

      
  # reassign empty data with IDW result
  for station in obs_data: 
    obs_data[station]['measurement'] = {}
    for year in sorted(obs_data[station]['statistic']):
      measuredData = date_to_int(date(year, 1, 1))
      obs_data[station]['measurement'][measuredData] = obs_data[station]['statistic'][year]['mean']

  return obs_data
