const form = document.getElementById('uploadForm');
const loader = document.getElementById('loader');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    loader.style.display = 'block';
    resultDiv.style.display = 'none';

    const response = await fetch('https://traffictracer.onrender.com/predict', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    loader.style.display = 'none';
    resultDiv.style.display = 'block';

    document.getElementById('threshold').textContent = data.threshold;
    document.getElementById('botnetRatio').textContent = data.botnet_ratio;
    const verdict = document.getElementById('verdict');
    verdict.textContent = data.verdict;
    verdict.className = 'verdict ' + (data.botnet_ratio < data.threshold ? 'safe' : 'threat');

    const ctx1 = document.getElementById('barChart').getContext('2d');
    const ctx2 = document.getElementById('doughnutChart').getContext('2d');
    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: ['Normal', 'Botnet'],
            datasets: [{
                label: '# of Flows',
                data: [data.normal_count, data.botnet_count],
                backgroundColor: ['green', 'red']
            }]
        }
    });
    new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['Normal', 'Botnet'],
            datasets: [{
                data: [data.normal_count, data.botnet_count],
                backgroundColor: ['green', 'red']
            }]
        }
    });
});
