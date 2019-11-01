def cities_max(df): 
    '''
    Def: Graphs cities per hour over course of desk
    Inputs:
        df: day_filter df
    Return: list of tuples with first value desk, second value max number of cities on desk
    '''
    city_constraint = np.full((24,1),10)
    org_cities = df.filter(['Org','Desk','Rls_HR'])
    org_cities = org_cities.filter(['Org','Desk','Rls_HR']).rename(columns={"Org": "City"})

    dst_cities = df.filter(['Dst','Desk','Rls_HR'])
    dst_cities = dst_cities.filter(['Dst','Desk','Rls_HR']).rename(columns={"Dst": "City"})

    cities = org_cities.append(dst_cities).groupby(['Desk','Rls_HR']).nunique()
    cities = cities.filter(['City'])
    
    cities_max_list = []
    for desk in cities.groupby(level=0):
        hrs = pd.DataFrame([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],columns=['Hours'])
        desk_subset = desk[1].merge(hrs, how= 'right',left_on ='Rls_HR' , right_on='Hours').fillna(0)
        desk_subset = desk_subset.sort_values(by= 'Hours')
        num_cities = desk_subset['City'].tolist()
        
        cities_max_list.append((desk[0],max(num_cities)))
    return cities_max_list

cities_max(day_filter)

def cities_dist(df): 
    '''
    Def: Graphs cities per hour over course of desk
    Inputs:
        df: desk_filter df
    Return: plot of cities per hour with conditional coloring
    '''
    org_cities = df.filter(['Org','Desk','Rls_HR'])
    org_cities = org_cities.filter(['Org','Desk','Rls_HR']).rename(columns={"Org": "City"})

    dst_cities = df.filter(['Dst','Desk','Rls_HR'])
    dst_cities = dst_cities.filter(['Dst','Desk','Rls_HR']).rename(columns={"Dst": "City"})

    cities = org_cities.append(dst_cities).groupby(['Desk','Rls_HR']).nunique()
    cities = cities.filter(['City'])
    cities = cities.droplevel('Desk')
    hrs = pd.DataFrame([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],columns=['Hours'])
    cities = cities.merge(hrs, how= 'right',left_on ='Rls_HR' , right_on='Hours').fillna(0)
    cities = cities.sort_values(by= 'Hours')
    num_cities = cities['City'].tolist()

    if all((x <= 10 for x in num_cities)) == True:
        city_color = 'green'
    else:
        city_color = 'red'

    cities.plot.bar(x='Hours', y='City', color = city_color)
    plt.plot(hrs,[10 for i in range(24)], color='blue')
    plt.show()

cities_dist(desk_filter)