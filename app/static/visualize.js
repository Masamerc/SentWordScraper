const chartOptions = {
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true
            }
        }]
    }
}

const generateBarChart = (chartCanvas, chartData) => {
    return new Chart(chartCanvas, {
        type: 'bar',
    
        data: {
            labels: chartData.map(tuple => tuple[0]),
            datasets: [{
                label: 'Count',
                backgroundColor: "rgba(86, 16, 151, 0.6)",
                borderColor: 'rgba(106, 103, 110, 1)',
                borderWidth: 2,
                data: chartData.map(tuple => tuple[1])
            }]
        },
    
        options: chartOptions
        });
};


const generatePieChart = (chartCanvas, pos_length, neg_length) => {
    return new Chart(chartCanvas, {
        type: "pie",
        data: {
            datasets: [{
                data: [
                    pos_length,
                    neg_length
                ],
                backgroundColor: [  
                'rgb(90, 214, 100, 0.6)',
                'rgb(235, 92, 82, 0.6)'
            ],
            borderColor: '#6B6B6B',
            borderWidth: 1
            }],
    
            labels: [
                'Positve Sentiments',
                'Negative Sentiments'
            ]
        },
        options: []
    });
};


const generateTop10Chart = (chartCanvas, data, labels, colors) => {
    return new Chart(chartCanvas, {
        type: 'bar',
    
        data: {
            labels:labels,
            datasets: [{
                label: 'Sentiment Score',
                backgroundColor: colors,
                borderColor: '#6B6B6B',
                borderWidth: 1,
                data: data
            }]
        },
        options: chartOptions
        });
};