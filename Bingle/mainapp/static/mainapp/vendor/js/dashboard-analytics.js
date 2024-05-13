new ApexCharts(document.querySelector("#total-income-graph"),{
        chart: {
            height: 320,
            type: "donut"
        },
        series: [27, 23, 20, 17],
        colors: ["#4680FF", "#E58A00", "#2CA87F", "#4680FF"],
        labels: ["Total income", "Total rent", "Download", "Views"],
        fill: {
            opacity: [1, 1, 1, .3]
        },
        legend: {
            show: !1
        },
        plotOptions: {
            pie: {
                donut: {
                    size: "65%",
                    labels: {
                        show: !0,
                        name: {
                            show: !0
                        },
                        value: {
                            show: !0
                        }
                    }
                }
            }
        },
        dataLabels: {
            enabled: !1
        },
        responsive: [{
            breakpoint: 575,
            options: {
                chart: {
                    height: 250
                },
                plotOptions: {
                    pie: {
                        donut: {
                            size: "65%",
                            labels: {
                                show: !1
                            }
                        }
                    }
                }
            }
        }]
    }).render(),