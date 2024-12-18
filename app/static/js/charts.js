document.addEventListener("DOMContentLoaded", function () {
    // 检查数据是否存在
    if (!datacenterCounts || !supplierCounts) {
        console.error("统计数据未定义，请检查后端传递数据！");
        return;
    }



    // 图表 1: 数据中心占比
    const ctxDatacenter = document.getElementById("datacenterChart").getContext("2d");
    new Chart(ctxDatacenter, {
        type: "pie",
        data: {
            labels: Object.keys(datacenterCounts),
            datasets: [{
                data: Object.values(datacenterCounts),
                backgroundColor: ["#ADFF2F", "#1E90FF"]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "top" },
                title: { display: true, text: "数据中心占比" }
            }
        }
    });

    // 对供应商占比数据按数量从多到少排序
    const sortedSuppliers = Object.entries(supplierCounts)
        .sort((a, b) => b[1] - a[1]); // 按值降序排列
    const sortedLabels = sortedSuppliers.map(item => item[0]); // 供应商名称
    const sortedData = sortedSuppliers.map(item => item[1]);   // 对应数量

    // 为每个供应商分配不同的颜色（随机生成颜色）
    const backgroundColors = sortedLabels.map((_, i) =>
        `hsl(${(i * 45) % 360}, 70%, 50%)` // HSL 色值生成不同色块
    );

    // 图表 2: 供应商占比
    const ctxSupplier = document.getElementById("supplierChart").getContext("2d");
    new Chart(ctxSupplier, {
        type: "bar",
        data: {
            labels: sortedLabels,
            datasets: [{
                label: "供应商占比",
                data: sortedData,
                backgroundColor: backgroundColors
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: { display: true, text: "供应商占比 (排序: 数量从多到少)" }
            },
            scales: {
                x: { title: { display: true, text: "供应商" } },
                y: { title: { display: true, text: "数量" } }
            }
        }
    });});