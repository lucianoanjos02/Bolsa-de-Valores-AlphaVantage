var chartInfo = document.getElementById('myChart').getContext('2d');
        var chart = new Chart(chartInfo, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: '',
                    borderColor: 'rgb(50,205,50)',
                    data: []
                }]
            },
            options: {}
        })