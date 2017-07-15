from iothealthresources import mysql,session,notificationUpdate,logging,average,json
from graphCharts import Chart

def output_json(dp, resource, datasequence_color, graph_type):
    """ Return a properly formatted JSON file for Statusboard """
    graph_title = ''
    datapoints = list()
    for x in dp:
        datapoints.append(
            {'title': x['dateTime'], 'value': float(x['value'])})
    datasequences = []
    datasequences.append({
        "title": resource,
        # "color":        datasequence_color,
        "datapoints": datapoints,
    })

    graph = dict(graph={
        'title': graph_title,
        'yAxis': {'hide': False},
        'xAxis': {'hide': False},
        'refreshEveryNSeconds': 600,
        'type': graph_type,
        'datasequences': datasequences,
    })

    return graph

def cycleDay(data, attr):
    colaborated = []
    days = {}
    for point in data:
        days.setdefault(point['date'], []).append(point[attr])
    for key in sorted(days):
        mv = min(days[key])
        mxv = max(days[key])
        av = sum(days[key]) / len(days[key])
        colaborated.append({"day": key, attr: av, "error": [mv, mxv]})
    return colaborated


def cycleMonth(data):
    try:
        i = 0
        colaborated = []
        months = {}
        for point in data:
            year, month, day = point['dateTime'].split('-')
            yearmonth = "{0}-{1}".format(year, month)
            months.setdefault(yearmonth, []).append(point['value'])
        for key in sorted(months):
            outliers = []
            weights = sorted(months[key])
            plot = calculate_boxplot(weights)
            low, _, _, _, upr = plot
            for w in weights:
                if float(w) > upr or float(w) < low:
                    outliers.append(w)
            colaborated.append({"month": key, "plot": plot, "outliers": outliers, "index": i})
            i += 1
        return colaborated
    except Exception as error : 
	logging.exception("message")

def cycleYear(data, return_as="json"):
    y = {}
    output = []
    for point in data:
        year, month, day = point['dateTime'].split('-')
        if int(year) not in y:
            y[int(year)] = {}
        if int(month) not in y[int(year)]:
            y[int(year)][int(month)] = []
        y[int(year)][int(month)].append(flt(point['value']))
    for ye in y:
        months = []
        for m in range(1, 13):
            if y[ye].get(m, False):
                months.append(flt(sum(y[ye][m]) / len(y[ye][m])))
            else:
                months.append(None)
        output.append({
            "name": ye,
            "data": months
        })
    if return_as is "json":
        return json.dumps(output)
    elif return_as is "raw":
        return output
    else:
        return output


def medianCal(n):
    num = sorted(n)
    if len(num) % 2 == 0:
        median = (flt(num[len(num) / 2]) + flt(num[(len(num) / 2) - 1])) / 2
    else:
        median = num[len(num) / 2]
    return flt(median)


def cal_quar(n):
    nums = sorted(n)
    if len(nums) % 2 == 0:
        lq = medianCal(nums[:(len(nums) / 2)])
        uq = medianCal(nums[len(nums) / 2:])
    else:
        lq = medianCal(nums[:(len(nums) / 2)])
        uq = medianCal(nums[(len(nums) / 2) + 1:])
    return (flt(lq), flt(uq))


def calculate_boxplot(num):
    n = sorted(num)
    m = medianCal(n)
    l, uq = cal_quar(n)
    i = uq - l
    u = flt(uq + (1.5 * i))
    lw = flt(l - (1.5 * i))
    if lw < 0:
        lw = 0
    return [lw, l, m, uq, u]


def periodsIntervals(all, year, month, week, day=None):
    completeList = [flt(d.get('value')) for d in all]
    listYear = [flt(d.get('value')) for d in year]
    listMonth = [flt(d.get('value')) for d in month]
    listWeek = [flt(d.get('value')) for d in week]
    graphPeriods = []
    graphPeriods.append({
        "name": "Averages",
        "type": "line",
        "data": [flt(average(completeList)), flt(average(listYear)), flt(average(listMonth)), flt(average(listWeek))]
    })
    graphPeriods.append({
        "name": "Stats",
        "type": "boxplot",
        "data": [calculate_boxplot(completeList), calculate_boxplot(listYear), calculate_boxplot(listMonth),
                 calculate_boxplot(listWeek)]
    })
    return graphPeriods


def flt(arg):
    return float("{0:.1f}".format(float(arg)))


def dataClean(d):
    while d[0]['value'] == d[1]['value']:
        d.pop(0)
    return d

def getEstimationForCalorie(burnedCal):
    try:
        query = "SELECT SUM(calorieEst) from FoodEntry where UserId = :userId and timestamp LIKE CONCAT(CURDATE(),'%')"
        data = {
            "userId" : session['user_Id']
        }
	dataOfCalorie= mysql.query_db(query, data)[0]['SUM(calorieEst)']
	if dataOfCalorie is not None:
		calorieConsumed=int(dataOfCalorie)
	else:
        	calorieConsumed = 0
        session['caloriesConsumed'] = calorieConsumed
        goalWeight = (int(session['goal'])/2.2)
	gender = 'Male'
	if 'gender' in session:
        	gender=session['gender']
        personAge = int(session['age'])
        if gender=="Female":
            if personAge<10:
                goalForCalorie=(22.5 * goalWeight) + 499
            elif personAge < 18:
                goalForCalorie=(12.2 * goalWeight) + 746
            elif personAge < 30:
                goalForCalorie=(14.7 * goalWeight) + 496
            elif personAge < 61:
                goalForCalorie=(8.7 * goalWeight) + 829
            else:
                goalForCalorie=(10.5 * goalWeight) + 596
        else:
            if personAge<10:
                goalForCalorie=(22.5 * goalWeight) + 495
            elif personAge < 18:
                goalForCalorie=(17.5 * goalWeight) + 651
            elif personAge < 30:
                goalForCalorie=(15.3 * goalWeight) + 679
            elif personAge < 61:
                goalForCalorie=(11.6 * goalWeight) + 879
            else:
                goalForCalorie=(13.5 * goalWeight) + 487

        availableCalorie=int((int(goalForCalorie)+int(burnedCal))-int(calorieConsumed))
        session['availableCalorie'] = availableCalorie
        session['goalForCalorie'] = goalForCalorie
	pcp=int((float(session['goal'])/float(session['weight']))*100)
	if pcp>100:
		pcp=pcp-100
	session['progressCaloriePercentage'] = pcp
	session['distanceLeft'] = abs((int(session['weight'])-int(session['goal'])))
	notificationUpdates()
    except (Exception) as error : 
	logging.exception("message")

def notificationUpdates():
    try:
	if session['functionName']=='OnLogin':
		notificationUpdate['availableCalorieValue'] = session['availableCalorie']
		if int(session['availableCalorie'])>0:
			notificationUpdate['recommedation']='New Recommendation Available'
			notificationUpdate['calorieExceeds']=''
			notificationUpdate['calorieAvailable']='Calorie Goal not Reached. Add Food Items to reach calorie goal and see recommendations.'
		else:
			notificationUpdate['recommedation']=''
			notificationUpdate['calorieAvailable']=''
			notificationUpdate['calorieExceeds']='Calorie Goal Exceeded'
	elif notificationUpdate['availableCalorieValue']!= session['availableCalorie']:
		if session['functionName']=='FoodEntry':
			if session['availableCalorie']>0:
				notificationUpdate['recommedation']='New Recommendation Available'
				notificationUpdate['calorieExceeds']=''
				notificationUpdate['calorieAvailable']=''
			else:
				notificationUpdate['recommedation']=''
				notificationUpdate['calorieAvailable']=''
				notificationUpdate['calorieExceeds']='Calorie Goal Exceeded'
		if session['functionName']=='OnDashboard':
			if session['availableCalorie']>0:
				notificationUpdate['recommedation']='New Recommendation Available'
				notificationUpdate['calorieExceeds']=''
				notificationUpdate['calorieAvailable']='Calorie Goal not Reached. Add Food Items to reach calorie goal and see recommendations.'
			else:
				notificationUpdate['recommedation']=''
				notificationUpdate['calorieAvailable']=''
				notificationUpdate['calorieExceeds']='Calorie Goal Exceeded'
    except (Exception) as error : 
	logging.exception("message")

def getStatsBar(all_steps,month_steps,day_steps):
	statsbar = [
            {
                'icon': "fa-step-forward fa-rotate-270",
                'title': "All Time Max Steps",
                'value': max([int(d.get('value')) for d in all_steps]) 
            },
            {
                'icon': "fa-step-forward fa-rotate-90",
                'title': "Average Daily Steps",
                'value': int(average([int(d.get('value')) for d in all_steps]))
            },
            {
                'icon': "fa-calendar",
                'title': "Month Max Steps",
                'value': max([int(d.get('value')) for d in month_steps])
            },
            {
                'icon': "fa-balance-scale",
                'title': "Steps Today",
                'value': max([int(d.get('value')) for d in day_steps])
            }
        ]
	return statsbar

def getChartsData(all_steps,year_steps,month_steps,week_steps,boxplot_data):
        charts = [
            {
                "title": "Average for Time Period",
                "id": "time-period",
                "chart": Chart(
                    "Average Steps For Different Time Periods",
                    xCategories=["All Time", "Year", "Month", "Week"]
                ).add_raw_series(periodsIntervals(dataClean(all_steps), year_steps, month_steps, week_steps))
            },
            {
                "title": "Monthly Average Yearcycle",
                "id": "yearcycle",
                "chart": Chart(
                    "Monthly Average Yearcycle",
                    xCategories=['Jan', 'Feb', 'Mar', "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                ).add_raw_series(cycleYear(dataClean(all_steps), return_as="raw"))
            },
            {
                "title": "Steps for Past Month",
                "id": "month-steps",
                "chart": Chart("Steps for Past Month",
                               xType="datetime",
                               xCategories=[d.get('dateTime') for d in month_steps]
                               ).add_series("Steps",
                                            data=[d.get('value') for d in month_steps],
                                            type="column")

            },
            {
                "title": "Average Steps per Month",
                "id": "month-average",
                "chart": Chart(
                    "Average Steps Per Month",
                    xtype="datetime",
                    xCategories=[d.get('month') for d in boxplot_data]
                ).add_series(
                    "Steps",
                    data=[d.get('plot') for d in boxplot_data],
                    type="boxplot"
                ).add_series(
                    "Outliers",
                    data=[[d.get('index'), ] + d.get('outliers') for d in boxplot_data if d.get('outliers', False)],
                    type="scatter"
                )
            }
        ]
        return charts

def getWeightCharts():
    charts = [
	{
	    "title": "Weight Fluctuations for Past Month",
	    "id": "weight",
	},
	{
	    "title": "Average Weight All Time",
	    "id": "allweight",
	},
	{
	    "title": "Monthly Boxplot",
	    "id": "boxplot",
	},
	{
	    "title": "Yearly Cycle",
	    "id": "yearcycle",
	},
	{
	    "title": "Averages for Periods",
	    "id": "period",
	},
	]
    return charts

def getWeightStatsBar(weight_max,weight_min,month_max,weight_last):
    statsbar = [
	{
	    'icon': "fa-step-forward fa-rotate-270",
	    'title': "All Time Max Weight",
	    'value': weight_max
	},
	{
	    'icon': "fa-step-forward fa-rotate-90",
	    'title': "All Time Min Weight",
	    'value': weight_min
	},
	{
	    'icon': "fa-calendar",
	    'title': "Month Max Weight",
	    'value': month_max
	},
	{
	    'icon': "fa-balance-scale",
	    'title': "Last Weight",
	    'value': weight_last
	}
	]
    return statsbar

