/*JavaScript for results charts
After a user completes their mock interview they will be given a page of their results 
*/

//Bar Graph
const xValues = ["Coherence", "Clarity", "Correctness", "Politeness"];
const yValues = [55, 49, 44, 50];
const barColors = ["red", "green","blue","orange"];

const BarChart = new Chart("BarChart", {
    type: "bar",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: barColors,
        data: yValues,
      }]
    },
    options: {
        title: {
          display: true,
          text: "Category scores (out of 100)",
        }
    }
  });