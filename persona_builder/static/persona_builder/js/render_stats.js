            $(function() {
                function getRandomColors(n) {
                    var colors = [];
                    for (var c = 0; c < n; c++) {
                        var letters = '0123456789ABCDEF'.split('');
                        var color = '#';
                        for (var i = 0; i < 6; i++ ) {
                            color += letters[Math.floor(Math.random() * 16)];
                        }

                        colors.push(color);
                    }

                    return colors;
                }

                var p = new PersonaStats();
                for (prop in p.property_values) {
                    var keys = [];
                    var values = [];
                    for (var key in p.property_values[prop]) {
                        var label = key;
                        if ((typeof(label) == 'undefined') || (label == 'null') || (label == '')) {
                            label = 'Unknown';
                        }
                        keys.push(label);
                        values.push(p.property_values[prop][key]);
                    }

                    var ctx = document.getElementById("cnv-" + prop);
                    var propChart = new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: keys,
                            datasets: [{
                                backgroundColor: getRandomColors(values.length),
                                data: values
                            }]
                        }
                    });
                }
            });