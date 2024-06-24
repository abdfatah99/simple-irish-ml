document.getElementById('sepalForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const sepalLength = document.getElementById('sepalLength').value;
    const sepalWidth = document.getElementById('sepalWidth').value;

    fetch('http://127.0.0.1:8000/predict-iris', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sepal_length_cm: parseFloat(sepalLength),
            sepal_width_cm: parseFloat(sepalWidth)
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').textContent = 'Prediction: ' + JSON.stringify(data['classification name']);
    })
    .catch((error) => {
        document.getElementById('response').textContent = 'Error: ' + error;
    });
});