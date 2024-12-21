// 定义档位值
const rangeValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, 400, 500, 750, 1000];

// 更新滑块显示的档位值
function updateActualCountDisplay(sliderId, displayId) {
    const slider = document.getElementById(sliderId);
    const display = document.getElementById(displayId);

    if (slider && display) {
        // 获取当前索引并更新显示值
        const index = slider.value; // 滑块的值对应索引
        display.innerText = rangeValues[index];
    }
}

// 初始化所有滑块的最大值和默认值
document.addEventListener('DOMContentLoaded', () => {
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        // 设置滑块的范围和初始值
        slider.max = rangeValues.length - 1;
        const display = document.getElementById(slider.getAttribute('data-display-id'));
        const valueIndex = rangeValues.indexOf(parseInt(slider.getAttribute('data-initial-value'), 10));
        slider.value = valueIndex >= 0 ? valueIndex : 0;

        if (display) {
            display.innerText = rangeValues[slider.value];
        }
    });
});
