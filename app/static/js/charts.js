document.addEventListener("DOMContentLoaded", function () {
    if (!datacenterCounts || !supplierCounts) {
        console.error("统计数据未定义，请检查后端传递数据！");
        return;
    }

    // 1. 数据中心占比饼图
    const ctxDatacenter = document.getElementById("datacenterChart").getContext("2d");
    new Chart(ctxDatacenter, {
        type: "pie",
        data: {
            labels: Object.keys(datacenterCounts),
            datasets: [{
                data: Object.values(datacenterCounts),
                backgroundColor: ["#4CAF50", "#2196F3"],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "top" },
                title: { 
                    display: true, 
                    text: "数据中心分布",
                    padding: 20
                }
            }
        }
    });

    // 2. 供应商分布柱状图
    const sortedSuppliers = Object.entries(supplierCounts)
        .sort((a, b) => b[1] - a[1]);
    const ctxSupplier = document.getElementById("supplierChart").getContext("2d");
    new Chart(ctxSupplier, {
        type: "bar",
        data: {
            labels: sortedSuppliers.map(item => item[0]),
            datasets: [{
                label: "代理数量",
                data: sortedSuppliers.map(item => item[1]),
                backgroundColor: "#2196F3",
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: { 
                    display: true, 
                    text: "供应商代理数量分布",
                    padding: 20
                }
            },
            scales: {
                x: {
                    grid: { display: false }
                },
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                }
            }
        }
    });

    // 3. FRPS 容量使用趋势图
    const ctxCapacity = document.getElementById("capacityChart").getContext("2d");
    const capacityChart = new Chart(ctxCapacity, {
        type: "line",
        data: {
            labels: capacity_data.map(item => item.vms_id),
            datasets: [{
                label: "已用容量",
                data: capacity_data.map(item => item.usage_percent),
                borderColor: "#FF9800",
                backgroundColor: "rgba(255, 152, 0, 0.1)",
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { 
                    display: true, 
                    text: "FRPS 容量使用率",
                    padding: 20
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            return `使用率: ${value}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: value => value + '%'
                    }
                }
            }
        }
    });

    // 4. ISP 线路分布图
    const ctxIsp = document.getElementById("ispChart").getContext("2d");
    const ispChart = new Chart(ctxIsp, {
        type: "doughnut",
        data: {
            labels: Object.keys(isp_counts),
            datasets: [{
                data: Object.values(isp_counts),
                backgroundColor: [
                    "#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336",
                    "#03A9F4", "#8BC34A", "#FFC107", "#E91E63", "#795548"
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { 
                    position: "right",
                    labels: {
                        padding: 20
                    }
                },
                title: { 
                    display: true, 
                    text: "ISP 线路分布",
                    padding: 20
                }
            }
        }
    });
});