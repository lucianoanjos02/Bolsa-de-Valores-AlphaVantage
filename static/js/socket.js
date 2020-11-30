var socket = io.connect('http://localhost:5000')
        socket.on('connect', function(){
            socket.emit('request', {
                data: 'ready'
            })
            socket.emit('request_chart_update',{
                data: document.querySelector('.jumbotron-heading').innerHTML
            })
        socket.on('response', function(message){
            var count = 1
            message.forEach(element => {
                var index = 0
                $('td.price_close' + count.toString()).text(element[index]);
                $('td.price_high' + count.toString()).text(element[index + 1]);
                $('td.price_low' + count.toString()).text(element[index + 2]);
                $('td.price_date' + count.toString()).text(element[index + 3]);
                count += 1
            });
            socket.emit('request', {
                data: 'table update'
            })
        })
        socket.on('response_chart_update', function(message){
            message[0].forEach(element => {
                if(chart.data.labels.length == 7) {
                    chart.data.labels.pop();
                } 
                chart.data.labels.push(element);      
            });
            message[1].forEach(element => {
                chart.data.datasets.forEach((dataset) => {
                    if(dataset.data.length == 7) {
                        dataset.data.pop();
                    } 
                    dataset.data.push(element); 
                });
            });
            document.querySelector('.price1').innerHTML = message[1][5];
            document.querySelector('.price2').innerHTML = message[1][6];
            chart.update();
            socket.emit('request_chart_update', {
                data: document.querySelector('.jumbotron-heading').innerHTML
            })
        })

        })
        function showData(buttonId){
            event.preventDefault();
            var buttonIdString = buttonId.toString();
            var companySymbol = document.querySelector(`.company_symbol${buttonIdString}`).innerHTML;
            document.querySelector('.jumbotron-heading').innerHTML = companySymbol;
            socket.emit('request_company_data', {
                data: companySymbol
            })
        }    

        socket.on('response_company_data', function(message) {
            message[0].forEach(element => {
                if(chart.data.labels.length == 7) {
                    chart.data.labels = [];
                } 
                chart.data.labels.push(element);      
            });
            message[1].forEach(element => {
                chart.data.datasets.forEach((dataset) => {
                    if(dataset.data.length == 7) {
                        dataset.data = [];
                    } 
                    dataset.data.push(element); 
                    document.querySelector('.price1').innerHTML = message[1][5];
                    document.querySelector('.price2').innerHTML = message[1][6];
                });
            });
            chart.update();
        })