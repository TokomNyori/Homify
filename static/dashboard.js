var bhk_data = [];
var bhk_data_types = [];

const d_types = document.querySelectorAll('#datas_hidden_type');
d_types.forEach((e) => {
    bhk_data_types.push(e.value);
});

for (let i = 0; i < 5; i++) {
    bhk_data.push(0)
}

for (let j = 0; j < bhk_data_types.length; j++) {
    if (bhk_data_types[j] == '1 BHK') {
        bhk_data[0] += 1;
    }
    else if (bhk_data_types[j] == '2 BHK') {
        bhk_data[1] += 1;
    }
    else if (bhk_data_types[j] == '3 BHK') {
        bhk_data[2] += 1;
    }
    else if (bhk_data_types[j] == '4 BHK') {
        bhk_data[3] += 1;
    }
    else if (bhk_data_types[j] == '4+ BHK') {
        bhk_data[4] += 1;
    }
}


let category_options = {
    series: bhk_data,
    labels: ['1 BHK', '2 BHK', '3 BHK', '4 BHK', '4+ BHK'],
    title: {
        text: 'Percentage of tenants (according to BHK types)',
        align: 'left',
        margin: 10,
        offsetX: 0,
        offsetY: 0,
        floating: false,
        style: {
          fontSize:  '15px',
          fontWeight:  '400',
          fontFamily:  'Lato',
          color:  '#555',
        },
    },
    chart: {
        height: 350,
        type: "donut",
    },
    colors: ['#6ab04c', '#2980b9', '#f39c12', '#775DD0', '#d35400']
};

let category_chart = new ApexCharts(document.querySelector("#category-chart"), category_options);
category_chart.render();


//Taking care of Tenants line chart

var property_lists = [];
var property_datas = [];
var property_types = [];
var data_in_num = [];
const property_names = document.querySelectorAll('#property_names_hidden');
property_names.forEach((e) => {
    property_lists.push(e.value.toUpperCase());
});

for (let d = 0; d < property_lists.length; d++) {
    data_in_num.push([0, 0, 0, 0, 0]);
}

const datas_types = document.querySelectorAll('#datas_hidden_type');
datas_types.forEach((e) => {
    property_types.push(e.value);
});
const datas = document.querySelectorAll('#datas_hidden');
datas.forEach((e) => {
    property_datas.push(e.value.toUpperCase());
});


for (let i = 0; i < property_datas.length; i++) {
    for (let j = 0; j < property_lists.length; j++) {
        if (property_datas[i] == property_lists[j]) {
            if (property_types[i] == '1 BHK') {
                data_in_num[j][0] += 1;
            }
            else if (property_types[i] == '2 BHK') {
                data_in_num[j][1] += 1;
            }
            else if (property_types[i] == '3 BHK') {
                data_in_num[j][2] += 1;
            }
            else if (property_types[i] == '4 BHK') {
                data_in_num[j][3] += 1;
            }
            else if (property_types[i] == '4+ BHK') {
                data_in_num[j][4] += 1;
            }
        }
    }
}

max_bhk = []

for (let t = 0; t < 5; t++) {
    for (let t1 = 0; t1 < 5; t1++) {
        max_bhk.push(data_in_num[t][t1]);
    }
}

var holder = max_bhk[0];
for (let n = 0; n < max_bhk.length; n++) {
    if (holder < max_bhk[n]) {
        holder = max_bhk[n];
    }
}

var line_chartY = holder + 2;
if (line_chartY % 2 != 0){
    line_chartY += 1;
}
var lineY_tick = Math.round(line_chartY / 2);


crayon = ['#6ab04c', '#2980b9', '#f39c12', '#775DD0', '#d35400', '#ef476f', '#43aa8b', '#00b4d8', '#e71d36', '#7209b7', '#007f5f', '#e07a5f', '#343a40', '#8ac926', '#db3a34']
var series = [];
var colors = [];
for (i = 0; i < property_lists.length; i++) {
    series.push({
        name: property_lists[i],
        data: data_in_num[i],
    });
}

for (i = 0; i < property_lists.length; i++) {
   colors.push(crayon[i]);
}

let customer_options = {
    series: series,
    colors: colors,
    title: {
        text: 'Tenants (in each property)',
        align: 'left',
        margin: 10,
        offsetX: 0,
        offsetY: 0,
        floating: false,
        style: {
          fontSize:  '15px',
          fontWeight:  '400',
          fontFamily:  'Lato',
          color:  '#555',
        },
    },
    chart: {
        height: 350,
        type: 'line',
        zoom: {
            enabled: true
        }
    },
    yaxis: {
        min: 0,
        max: line_chartY,
        tickAmount: lineY_tick,
    },
    dataLabels: {
        enabled: true,
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    xaxis: {
        categories: ['1 BHK', '2 BHK', '3 BHK', '4 BHK', '4+ BHK'],
    },
    legend: {
        position: 'bottom',
        show: true,
        onItemHover: {
            highlightDataSeries: true
        },
    }
};

let customer_chart = new ApexCharts(document.querySelector("#customer-chart"), customer_options);
customer_chart.render();


// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated')
            }, false)
        })
})()