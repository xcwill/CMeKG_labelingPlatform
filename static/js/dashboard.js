(function($) {
  'use strict';
  $(function() {
    if ($("#dashboard-monthly-analytics").length) {
      var ctx = document.getElementById('dashboard-monthly-analytics').getContext("2d");
      var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Arl', 'May', 'Jun', 'Jul', 'Aug'],
          datasets: [{
              label: "Quality of Service",
              borderColor: 'rgba(255, 166 ,36, 0.8)',
              backgroundColor: 'rgba(255, 166 ,36, 0.8)',
              pointRadius: 0,
              fill: true,
              borderWidth: 1,
              fill: 'origin',
              data: [2, 2, 20, 40, 20, 50, 40, 10, 30]
            },
            {
              label: "Service Recommendations",
              borderColor: 'rgba(255, 166 ,36, 0.8)',
              backgroundColor: 'rgba(255, 166 ,36, 0.8)',
              pointRadius: 0,
              fill: true,
              borderWidth: 1,
              fill: 'origin',
              data: [0, 35, 0, 60, 30, 20, 10, 40, 20]
            }
          ]
        },
        options: {
          legend: {
            display: false,
            position: "top"
          },
          scales: {
            xAxes: [{
              ticks: {
                display: true,
                beginAtZero: true,
                fontColor: 'rgba(0, 0, 0, 1)'
              },
              gridLines: {
                display: false,
                drawBorder: false,
                color: 'transparent',
                zeroLineColor: '#eeeeee'
              }
            }],
            yAxes: [{
              gridLines: {
                drawBorder: true,
                display: true,
                color: '#eeeeee',
              },
              categoryPercentage: 0.5,
              ticks: {
                display: true,
                beginAtZero: true,
                stepSize: 20,
                max: 80,
                fontColor: 'rgba(0, 0, 0, 0.3)'
              }
            }]
          },
        },
        elements: {
          point: {
            radius: 0
          }
        }
      });
      document.getElementById('js-legend').innerHTML = myChart.generateLegend();
    }
    if ($("#currentBalanceCircle").length) {
      var bar = new ProgressBar.Circle(currentBalanceCircle, {
        color: '#000',
        strokeWidth: 12,
        trailWidth: 12,
        trailColor: '#eee',
        easing: 'easeInOut',
        lineCap: 'round',
        duration: 1400,
        from: {
          color: '#ec3432',
          width: 12
        },
        to: {
          color: '#ec3432',
          width: 12
        },
        step: function(state, circle) {
          circle.path.setAttribute('stroke', state.color);
          circle.path.setAttribute('stroke-width', state.width);

          var value = Math.round(circle.value() * 100);
          if (value === 0) {
            circle.setText('');
          } else {
            circle.setText(value);
          }

        }
      });

      bar.text.style.fontSize = '1.5rem';
      bar.animate(0.4);
    }
  });
})(jQuery);