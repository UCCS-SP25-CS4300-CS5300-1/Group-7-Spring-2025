/*JavaScript for results charts
After a user completes their mock interview they will be given a page of their results 
*/

const inputData = JSON.parse('{{ scores|safe|escapejs }}');


//Bar Graph
const xValues = ["Professionalism", "Subject Knowledge", "Clarity", "Overall"];
const yValues = [];
const barColors = ["#4482A6", "#F5F9E9","#96A13A","#564256"];

Chart.defaults.backgroundColor = '#9BD0F5';
Chart.defaults.borderColor = '#36A2EB';
Chart.defaults.color = '#000';

const BarChart = document.getElementById('BarChart').getContext('2d');
const chart1 = new Chart(BarChart, {
    type: "bar",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: barColors,
        data: Object.values(inputData),
      }]
    },
    options: {
        font: {
          family: "Verdana, Geneva, Tahoma, sans-serif",
          size: 15,
          color: "blue",
        },
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: "Category scores (out of 100)",
        },
        scales: {
          y: [{
            ticks: {
                beginAtZero: true,
                max: 100,
                min: 0
            }
        }],
      }  
    } 
  });

const dataSplits = [200,50,100];
const DonutChart = document.getElementById("DonutChart").getContext('2d');
const chart2 = new Chart(DonutChart, {
  type: 'doughnut',

  data: {
    labels: [
      'Professionalism',
      'Speed',
      'Grammar'
    ],
    datasets: [{
      data: dataSplits,
      backgroundColor: barColors,
      hoverOffset: 4
    }],
  },
  options: {
    title:{
      display: true,
      text: 'Categories',
    },
  },
});

