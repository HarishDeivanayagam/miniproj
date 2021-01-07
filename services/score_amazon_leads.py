from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import json


def score_from_amazon(json_file):
    d = {}
    nd = {}
    drating = {}
    html = '<html><head><title>Results</title><link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet"><script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js" integrity="sha256-R4pqcOYV8lt7snxMQO/HSbVCFRPMdrhAFMH+vr9giYI=" crossorigin="anonymous"></script></head><body>'
    html = html + '<table style="width:100%;border-collapse: collapse;"><tr><th>Position</th><th>Name</th><th>Score</th><th>Rating</th></tr>'
    sid_obj = SentimentIntensityAnalyzer()
    json_file = json.loads(json_file)
    

    for l in json_file:
        sentiment_dict = sid_obj.polarity_scores(l['title'])
        upd = {l['name'] : (sentiment_dict['neg']*100)}
        upd1 = {l['name'] : l['rating']}
        d.update(upd)
        drating.update(upd1)


    for w in sorted(d, key=d.get, reverse=True):
        nd[w] = d[w]

    data_for_charts = []
    label_for_charts = []
    count_leads = [0,0,0]

    count = 1
    for e in nd.keys():
        if d[e] > 35:
            html = html + ('<tr class="pass"><td>' + str(count) + '</td><td>' + str(e) + '</td><td>' +  str(d[e])  + '</td><td>' + str(drating[e]) +  '</td></tr>') 
            data_for_charts.append(d[e])
            label_for_charts.append(e)
            count_leads[0] += 1
        elif d[e] <= 35 and d[e] > 1:
            html = html + ('<tr class="warn"><td>' + str(count) + '</td><td>' + str(e) + '</td><td>' +  str(d[e])  + '</td><td>' + str(drating[e]) +  '</td></tr>') 
            data_for_charts.append(d[e])
            label_for_charts.append(e)
            count_leads[1] += 1
        else:
            html = html + ('<tr class="fail"><td>' + str(count) + '</td><td>' + str(e) + '</td><td>' +  str(d[e])  + '</td><td>' + str(drating[e]) +  '</td></tr>') 
            data_for_charts.append(d[e]-1)
            label_for_charts.append(e)
            count_leads[2] += 1
        count += 1

    
    html = html + '</table><style>table, th, td {border: 1px solid #ddd;} th, td {padding: 15px;} th{background:#26265c;color:white;} td{background:#e2e2ff;} .pass{color:green;} .fail{color:red; } .warn{color:#999900;} body{font-family:"Inter";}</style>'
    

    html = html + '<div class="analytics"><h1>Analytics</h1>'

    html = html + '<canvas id="myChart"></canvas>'

    html = html + '<canvas id="myChartpie"></canvas> '

    html = html + '</div>'

    html = html + " <script> var ctx = document.getElementById('myChart').getContext('2d'); var ctxpie = document.getElementById('myChartpie').getContext('2d');"

    html = html + "var myChart = new Chart(ctx, { type: 'bar', data: { labels: "  + str(label_for_charts) + ", datasets: [{ label: '# of Scores', "

    html = html + "data: " + str(data_for_charts) + " ,"

    html = html + "backgroundColor: [ 'rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)','rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'], "

    html = html + " borderColor: ['rgba(255, 99, 132, 1)','rgba(54, 162, 235, 1)','rgba(255, 206, 86, 1)','rgba(75, 192, 192, 1)','rgba(153, 102, 255, 1)','rgba(255, 159, 64, 1)'],borderWidth: 1 }] },options: {scales: { yAxes: [{ ticks: {beginAtZero: true}}]}}});"
    
    html = html + "var myPieChart = new Chart(ctxpie, {type: 'pie',data: { datasets: [{ backgroundColor: ['#09ad00','#e6d200','#ff3700'], data: " + str(count_leads) + " }],labels: ['Qualified','Medium','Failed'] } });</script>"

    html = html + '<style>.analytics {height:1800px;width:1800px;} .analytics-pie {height:1000px;width:1000px;}</style>'

    html = html + '</body></html>'


    return html
