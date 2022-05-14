        var options = {
          series: [{
            name: "Pollution Forecast",
            data: [80, 95, 49, 50]
        }],
          chart: {
          height: 350,
          type: 'line',
          zoom: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'straight'
        },
        title: {
          text: 'Pollution Forecast',
          align: 'left'
        },
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        xaxis: {
          categories: ['18/04/2022', '18/04/2022', '18/04/2022', '18/04/2022'],
        }
        yaxis: {
          categories: ['18/04/2022', '18/04/2022', '18/04/2022', '18/04/2022'],
        }
        };

        var chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();