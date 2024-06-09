function updateSliderValue(value) {
    document.getElementById('sliderValue').textContent = value;
}

document.getElementById('surveyForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const satisfaction = document.getElementById('satisfaction').value;
    document.getElementById('result').textContent = `You rated your satisfaction as ${satisfaction}%`;
});